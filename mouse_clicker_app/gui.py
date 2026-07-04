"""Tkinter front-end for the mouse clicker.

The GUI only replaces *config input* — the actual clicking is done by the
unchanged `engine.run()`. The engine runs on a background thread (Tkinter is
not thread-safe), and thread -> UI communication goes through a Queue that the
main thread drains via `root.after`.
"""

from __future__ import annotations

import queue
import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk

from pynput import mouse

import config as cfg
from config import VALID_CLICK_TYPES, VALID_MODES, Config, Target
from engine import RunStats, run
from input_listener import start_stop_listener


def build_config(
    mode: str,
    start_delay: str | float,
    duration: str | float,
    click_type: str,
    interval: str | float,
    stop_on_any_key: bool,
    targets: list[tuple[int, int]],
) -> Config:
    """Build and validate a Config from raw field values (no Tk dependency).

    Raises ValueError on any unparseable number or invalid setting, so both the
    GUI and tests can rely on the same checks.
    """
    try:
        config = Config(
            mode=mode,
            start_delay_seconds=float(start_delay),
            run_duration_seconds=float(duration),
            click_type=click_type,
            click_interval_seconds=float(interval),
            stop_on_any_key=bool(stop_on_any_key),
            targets=[Target(int(x), int(y)) for x, y in targets],
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid numeric field: {exc}") from exc
    return cfg.validate_config(config)


class ClickerGUI:
    def __init__(self, root: tk.Tk, config_path: str | None = None) -> None:
        self.root = root
        self.config_path = config_path
        self.stop_event = threading.Event()
        self.listener = None
        self.worker: threading.Thread | None = None
        self.msgq: queue.Queue = queue.Queue()
        self._pos_controller = mouse.Controller()

        root.title("Mouse Clicker")
        root.resizable(False, False)
        self._build_widgets()
        self._load_initial()
        self.root.after(100, self._poll_queue)

    # ---------- layout ----------
    def _build_widgets(self) -> None:
        pad = {"padx": 6, "pady": 4}
        frm = ttk.Frame(self.root, padding=10)
        frm.grid(row=0, column=0, sticky="nsew")

        self.mode_var = tk.StringVar()
        self.click_type_var = tk.StringVar()
        self.delay_var = tk.StringVar()
        self.duration_var = tk.StringVar()
        self.interval_var = tk.StringVar()
        self.stopkey_var = tk.BooleanVar()

        ttk.Label(frm, text="Mode").grid(row=0, column=0, sticky="w", **pad)
        ttk.Combobox(frm, textvariable=self.mode_var, values=sorted(VALID_MODES),
                     state="readonly", width=18).grid(row=0, column=1, **pad)

        ttk.Label(frm, text="Click type").grid(row=1, column=0, sticky="w", **pad)
        ttk.Combobox(frm, textvariable=self.click_type_var, values=sorted(VALID_CLICK_TYPES),
                     state="readonly", width=18).grid(row=1, column=1, **pad)

        ttk.Label(frm, text="Start delay (s)").grid(row=2, column=0, sticky="w", **pad)
        ttk.Entry(frm, textvariable=self.delay_var, width=20).grid(row=2, column=1, **pad)

        ttk.Label(frm, text="Duration (s, 0=forever)").grid(row=3, column=0, sticky="w", **pad)
        ttk.Entry(frm, textvariable=self.duration_var, width=20).grid(row=3, column=1, **pad)

        ttk.Label(frm, text="Interval (s)").grid(row=4, column=0, sticky="w", **pad)
        ttk.Entry(frm, textvariable=self.interval_var, width=20).grid(row=4, column=1, **pad)

        ttk.Checkbutton(frm, text="Stop on any key", variable=self.stopkey_var).grid(
            row=5, column=0, columnspan=2, sticky="w", **pad)

        # Targets
        ttk.Label(frm, text="Targets").grid(row=6, column=0, sticky="nw", **pad)
        tgt_frame = ttk.Frame(frm)
        tgt_frame.grid(row=6, column=1, sticky="w", **pad)
        self.targets_list = tk.Listbox(tgt_frame, height=5, width=18)
        self.targets_list.grid(row=0, column=0, rowspan=4)
        ttk.Button(tgt_frame, text="Add current", command=self._add_current_position).grid(row=0, column=1, sticky="ew", padx=4)
        ttk.Button(tgt_frame, text="Record (F8)", command=self._record).grid(row=1, column=1, sticky="ew", padx=4)
        ttk.Button(tgt_frame, text="Remove", command=self._remove_target).grid(row=2, column=1, sticky="ew", padx=4)
        ttk.Button(tgt_frame, text="Clear", command=self._clear_targets).grid(row=3, column=1, sticky="ew", padx=4)

        # Actions
        btns = ttk.Frame(frm)
        btns.grid(row=7, column=0, columnspan=2, pady=(10, 4))
        self.start_btn = ttk.Button(btns, text="Start", command=self._start)
        self.start_btn.grid(row=0, column=0, padx=4)
        self.stop_btn = ttk.Button(btns, text="Stop", command=self._stop, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Save config", command=self._save).grid(row=0, column=2, padx=4)

        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(frm, textvariable=self.status_var, foreground="#2a6").grid(
            row=8, column=0, columnspan=2, sticky="w", **pad)

    # ---------- state helpers ----------
    def _load_initial(self) -> None:
        try:
            c = cfg.load_config(self.config_path)
        except ValueError:
            c = Config()  # fall back to defaults if the file is invalid
        self.mode_var.set(c.mode)
        self.click_type_var.set(c.click_type)
        self.delay_var.set(f"{c.start_delay_seconds:g}")
        self.duration_var.set(f"{c.run_duration_seconds:g}")
        self.interval_var.set(f"{c.click_interval_seconds:g}")
        self.stopkey_var.set(c.stop_on_any_key)
        for t in c.targets:
            self.targets_list.insert(tk.END, f"{t.x}, {t.y}")

    def _targets_from_list(self) -> list[tuple[int, int]]:
        out = []
        for line in self.targets_list.get(0, tk.END):
            x, y = (part.strip() for part in line.split(","))
            out.append((int(x), int(y)))
        return out

    def _config_from_fields(self) -> Config:
        return build_config(
            self.mode_var.get(),
            self.delay_var.get(),
            self.duration_var.get(),
            self.click_type_var.get(),
            self.interval_var.get(),
            self.stopkey_var.get(),
            self._targets_from_list(),
        )

    # ---------- target buttons ----------
    def _add_current_position(self) -> None:
        """Append the current mouse cursor position to the targets list."""
        time.sleep(5)
        x, y = self._pos_controller.position
        self.targets_list.insert(tk.END, f"{int(x)}, {int(y)}")
        self.status_var.set(f"Added ({int(x)}, {int(y)})")

    def _remove_target(self) -> None:
        for idx in reversed(self.targets_list.curselection()):
            self.targets_list.delete(idx)

    def _clear_targets(self) -> None:
        self.targets_list.delete(0, tk.END)

    def _record(self) -> None:
        self.status_var.set("Recording: F8 to capture, Esc to finish...")
        self.start_btn.config(state="disabled")
        threading.Thread(target=self._record_worker, daemon=True).start()

    def _record_worker(self) -> None:
        from recorder import Recorder

        try:
            targets = Recorder().run()  # blocks until Esc
        except Exception as exc:  # never leave Start disabled if recording fails
            self.msgq.put(("record_error", str(exc)))
            return
        self.msgq.put(("targets", targets))

    # ---------- run / stop ----------
    def _start(self) -> None:
        try:
            config = self._config_from_fields()
        except ValueError as exc:
            messagebox.showerror("Invalid settings", str(exc))
            return

        self.stop_event.clear()
        if config.stop_on_any_key:
            self.listener = start_stop_listener(self.stop_event)
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.worker = threading.Thread(target=self._run_worker, args=(config,), daemon=True)
        self.worker.start()

    def _stop(self) -> None:
        self.stop_event.set()

    def _save(self) -> None:
        try:
            config = self._config_from_fields()
        except ValueError as exc:
            messagebox.showerror("Invalid settings", str(exc))
            return
        path = cfg.save_config(config, self.config_path)
        self.status_var.set(f"Saved to {path}")

    def _run_worker(self, config: Config) -> None:
        # Start delay (abortable via stop_event / Stop button).
        remaining = int(config.start_delay_seconds)
        while remaining > 0 and not self.stop_event.is_set():
            self.msgq.put(("status", f"Starting in {remaining}..."))
            if self.stop_event.wait(1):
                break
            remaining -= 1
        if self.stop_event.is_set():
            self.msgq.put(("done", RunStats(stopped_by="cancelled"), 0.0))
            return

        self.msgq.put(("status", "Running... (Stop button or configured key to halt)"))
        start = time.monotonic()
        stats = run(config, self.stop_event)
        self.msgq.put(("done", stats, time.monotonic() - start))

    # ---------- queue pump ----------
    def _poll_queue(self) -> None:
        # The reschedule lives in `finally` so a handler exception can never kill
        # the pump (which would freeze all UI updates).
        try:
            while True:
                kind, *rest = self.msgq.get_nowait()
                if kind == "status":
                    self.status_var.set(rest[0])
                elif kind == "targets":
                    self._apply_recorded_targets(rest[0])
                elif kind == "record_error":
                    self.status_var.set(f"Record failed: {rest[0]}")
                    self.start_btn.config(state="normal")
                elif kind == "done":
                    stats: RunStats = rest[0]
                    elapsed: float = rest[1]
                    self._on_finished(stats, elapsed)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self._poll_queue)

    def _apply_recorded_targets(self, recorded: list[Target]) -> None:
        """Populate the listbox from a finished recording and re-enable Start."""
        if recorded:
            self._clear_targets()
            for t in recorded:
                self.targets_list.insert(tk.END, f"{t.x}, {t.y}")
            self.status_var.set(f"Recorded {len(recorded)} target(s).")
        else:
            # Nothing captured: keep any existing targets rather than wiping them.
            self.status_var.set("Recording finished (no points captured).")
        self.start_btn.config(state="normal")

    def _on_finished(self, stats: RunStats, elapsed: float) -> None:
        if self.listener is not None:
            self.listener.stop()
            self.listener = None
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_var.set(
            f"Stopped ({stats.stopped_by}) - {stats.clicks} clicks, "
            f"{stats.cycles} cycles, {elapsed:.1f}s"
        )


def launch(config_path: str | None = None) -> None:
    root = tk.Tk()
    ClickerGUI(root, config_path)
    root.mainloop()


if __name__ == "__main__":
    launch()
