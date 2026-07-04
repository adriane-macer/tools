"""Interactive coordinate recorder.

Move the mouse over a spot in the target window and press F8 to capture its
(x, y). Backspace removes the last capture; Esc finishes. The captured list
replaces the `targets` in config.json.

This replaces the old copy-paste workflow of running check_position.py and
pasting coordinates in as comments.
"""

from __future__ import annotations

from pynput import keyboard, mouse

import config as cfg


class Recorder:
    """Captures cursor positions via keypresses.

    Key handling lives in `handle_key` (separate from the listener) so it can be
    unit-tested without synthesizing real keyboard events.
    """

    def __init__(self, controller: mouse.Controller | None = None) -> None:
        self._controller = controller or mouse.Controller()
        self.points: list[tuple[int, int]] = []

    def _position(self) -> tuple[int, int]:
        x, y = self._controller.position
        return int(x), int(y)

    def handle_key(self, key) -> bool | None:
        """Handle one key press. Return False to stop the listener (Esc)."""
        if key == keyboard.Key.f8:
            point = self._position()
            self.points.append(point)
            print(f"  [{len(self.points)}] captured {point}")
        elif key == keyboard.Key.backspace:
            if self.points:
                removed = self.points.pop()
                print(f"  removed {removed}  ({len(self.points)} left)")
            else:
                print("  (nothing to remove)")
        elif key == keyboard.Key.esc:
            return False
        return None

    def run(self) -> list[cfg.Target]:
        """Block until Esc, then return the captured targets."""
        _print_instructions()
        with keyboard.Listener(on_press=self.handle_key) as listener:
            listener.join()
        return [cfg.Target(x, y) for x, y in self.points]


def _print_instructions() -> None:
    print("=" * 52)
    print("  COORDINATE RECORDER")
    print("=" * 52)
    print("  F8         capture the current cursor position")
    print("  Backspace  remove the last captured point")
    print("  Esc        finish and save")
    print("-" * 52)
    print("  Hover over each target, press F8. Nothing is clicked.")
    print("=" * 52)


def record_and_save(config_path: str | None = None) -> list[cfg.Target]:
    """Run a recording session and persist the result to the config file."""
    targets = Recorder().run()
    if targets:
        saved_path = cfg.save_targets(targets, config_path)
        print(f"\nSaved {len(targets)} target(s) to {saved_path}")
        print("Tip: set \"mode\" to \"move_and_click\" (or \"click_fixed\") to use them.")
    else:
        print("\nNo targets captured; config left unchanged.")
    return targets
