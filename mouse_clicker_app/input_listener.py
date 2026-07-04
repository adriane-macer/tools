"""Global keyboard listener that signals the engine to stop.

Runs on a background thread. On the first key press it sets the shared
`stop_event`, which the engine loop polls to exit cleanly. This replaces the
old "drag the mouse off-screen" stop mechanism with a real any-key stop.
"""

from __future__ import annotations

import threading

from pynput import keyboard


def start_stop_listener(stop_event: threading.Event) -> keyboard.Listener:
    """Start a listener that sets `stop_event` on any key press.

    Returns the running Listener so the caller can stop() it during cleanup.
    """

    def on_press(_key) -> bool:
        stop_event.set()
        return False  # returning False stops the listener after the first press

    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()
    return listener
