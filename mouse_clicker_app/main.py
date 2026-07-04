"""Mouse Clicker — console entry point (phase 1).

Loads config.json, counts down the start delay, wires up the any-key stop
listener, runs the engine, and prints a summary. Run with:

    python main.py                 # uses config.json next to this file
    python main.py --config x.json # use a different config
    python main.py --mode click_here --duration 30   # quick overrides
"""

from __future__ import annotations

import argparse
import threading
import time
from datetime import datetime

from config import Config, load_config
from engine import run
from input_listener import start_stop_listener


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Configurable mouse clicker (console).")
    parser.add_argument("--config", help="Path to a config.json file.")
    parser.add_argument("--gui", action="store_true", help="Launch the Tkinter GUI.")
    parser.add_argument(
        "--record",
        action="store_true",
        help="Record target coordinates (F8 to capture, Esc to save), then exit.",
    )
    parser.add_argument("--mode", help="Override the configured mode.")
    parser.add_argument("--duration", type=float, help="Override run_duration_seconds.")
    parser.add_argument("--delay", type=float, help="Override start_delay_seconds.")
    return parser.parse_args()


def _apply_overrides(config: Config, args: argparse.Namespace) -> None:
    if args.mode:
        config.mode = args.mode
    if args.duration is not None:
        config.run_duration_seconds = args.duration
    if args.delay is not None:
        config.start_delay_seconds = args.delay


def _countdown(seconds: float, stop_event: threading.Event) -> None:
    """Print a whole-second countdown, abortable with the stop key."""
    remaining = int(seconds)
    while remaining > 0 and not stop_event.is_set():
        print(f"  starting in {remaining}...  (press any key to cancel)", end="\r")
        if stop_event.wait(1):
            break
        remaining -= 1
    # Handle fractional remainder so the total delay is honored.
    frac = seconds - int(seconds)
    if frac > 0 and not stop_event.is_set():
        stop_event.wait(frac)
    print(" " * 60, end="\r")  # clear the countdown line


def _banner(config: Config) -> None:
    duration = "until stopped" if not config.has_duration else f"{config.run_duration_seconds:g}s"
    print("=" * 52)
    print("  MOUSE CLICKER")
    print("=" * 52)
    print(f"  mode        : {config.mode}")
    print(f"  click type  : {config.click_type}")
    print(f"  interval    : {config.click_interval_seconds:g}s")
    print(f"  start delay : {config.start_delay_seconds:g}s")
    print(f"  duration    : {duration}")
    print(f"  targets     : {len(config.targets)}")
    print("-" * 52)
    print("  Press ANY key to stop. FAILSAFE: slam mouse to a corner.")
    print("=" * 52)


def main() -> None:
    args = _parse_args()

    if args.gui:
        from gui import launch

        launch(args.config)
        return

    if args.record:
        # Recording writes targets and exits; no full-config validation needed.
        from recorder import record_and_save

        record_and_save(args.config)
        return

    try:
        config = load_config(args.config)
    except ValueError as exc:
        print(f"[error] {exc}")
        return
    _apply_overrides(config, args)

    _banner(config)

    stop_event = threading.Event()
    listener = start_stop_listener(stop_event) if config.stop_on_any_key else None

    try:
        _countdown(config.start_delay_seconds, stop_event)
        if stop_event.is_set():
            print("Cancelled before start.")
            return

        started = datetime.now()
        print(f"Running... started {started.strftime('%H:%M:%S')}")
        run_start = time.monotonic()

        stats = run(config, stop_event)

        elapsed = time.monotonic() - run_start
        ended = datetime.now()
        print("-" * 52)
        print(f"Stopped by  : {stats.stopped_by}")
        print(f"Clicks      : {stats.clicks}")
        print(f"Cycles      : {stats.cycles}")
        print(f"Elapsed     : {elapsed:.1f}s")
        print(f"Started     : {started.strftime('%H:%M:%S')}   Ended: {ended.strftime('%H:%M:%S')}")
    finally:
        if listener is not None:
            listener.stop()


if __name__ == "__main__":
    main()
