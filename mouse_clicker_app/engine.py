"""The click/move engine.

A single loop drives all four modes. It is unaware of *how* it was told to
stop — it only polls a shared `threading.Event`. Duration is measured with
`time.monotonic()` so it is immune to system clock changes.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass

import pyautogui

from config import Config, Target

# Slam the mouse into a screen corner to hard-abort a runaway loop.
pyautogui.FAILSAFE = True


@dataclass
class RunStats:
    clicks: int = 0
    cycles: int = 0
    stopped_by: str = "unknown"  # "key", "duration", "failsafe", or "error"


def _do_click(target: Target | None, click_type: str) -> None:
    """Perform one click of the configured type. None target == current position."""
    x = target.x if target else None
    y = target.y if target else None
    if click_type == "double":
        pyautogui.doubleClick(x, y)
    elif click_type == "right":
        pyautogui.click(x, y, button="right")
    else:  # "left"
        pyautogui.click(x, y)


def run(config: Config, stop_event: threading.Event) -> RunStats:
    """Run the configured action until the key is pressed or the duration elapses.

    `stop_event.wait(timeout)` is used for pacing so the loop stays responsive
    to the stop key even during the inter-click interval.
    """
    stats = RunStats()
    start = time.monotonic()

    def time_left() -> bool:
        if not config.has_duration:
            return True
        return (time.monotonic() - start) < config.run_duration_seconds

    try:
        while not stop_event.is_set() and time_left():
            _run_one_cycle(config, stop_event, stats)
            stats.cycles += 1
            # Responsive pacing: returns True immediately if stop was requested.
            if stop_event.wait(config.click_interval_seconds):
                break
    except pyautogui.FailSafeException:
        stats.stopped_by = "failsafe"
        return stats

    if stop_event.is_set():
        stats.stopped_by = "key"
    elif not time_left():
        stats.stopped_by = "duration"
    return stats


def _run_one_cycle(config: Config, stop_event: threading.Event, stats: RunStats) -> None:
    """Execute a single pass of the current mode."""
    if config.mode == "click_here":
        _do_click(None, config.click_type)
        stats.clicks += 1
        return

    if config.mode == "click_fixed":
        _do_click(config.targets[0], config.click_type)
        stats.clicks += 1
        return

    # move_only / move_and_click: walk the target list, checking stop between each.
    for target in config.targets:
        if stop_event.is_set():
            return
        pyautogui.moveTo(target.x, target.y)
        if config.mode == "move_and_click":
            _do_click(target, config.click_type)
            stats.clicks += 1
        if stop_event.wait(config.click_interval_seconds):
            return
