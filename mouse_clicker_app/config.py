"""Load and validate the mouse clicker configuration from a JSON file.

Keeps all settings in one place so the engine stays unaware of *where* its
configuration came from. Provides sane defaults so a missing/partial config
still runs.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

VALID_MODES = {"click_here", "click_fixed", "move_only", "move_and_click"}
VALID_CLICK_TYPES = {"left", "right", "double"}

# Modes that walk through the configured target list.
MODES_NEEDING_TARGETS = {"click_fixed", "move_only", "move_and_click"}


@dataclass
class Target:
    x: int
    y: int


@dataclass
class Config:
    mode: str = "click_here"
    start_delay_seconds: float = 5.0
    run_duration_seconds: float = 0.0  # 0 == run until stopped
    click_type: str = "left"
    click_interval_seconds: float = 0.5
    stop_on_any_key: bool = True
    targets: list[Target] = field(default_factory=list)

    @property
    def has_duration(self) -> bool:
        return self.run_duration_seconds > 0


def default_config_path() -> Path:
    """config.json living next to the app (works from source and a frozen exe).

    When packaged with PyInstaller (`--onefile`), `__file__` points inside a
    temp extraction dir, so we resolve relative to the exe (`sys.executable`)
    instead — that lets users edit config.json beside MouseClicker.exe.
    """
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).resolve().parent
    else:
        base = Path(__file__).resolve().parent
    return base / "config.json"


def load_config(path: str | Path | None = None) -> Config:
    """Read config.json into a validated Config. Falls back to defaults if absent."""
    config_path = Path(path) if path else default_config_path()

    if not config_path.exists():
        print(f"[config] {config_path.name} not found — using built-in defaults.")
        return Config()

    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{config_path} is not valid JSON: {exc}") from exc

    targets = [Target(int(t["x"]), int(t["y"])) for t in raw.get("targets", [])]

    config = Config(
        mode=raw.get("mode", Config.mode),
        start_delay_seconds=float(raw.get("start_delay_seconds", Config.start_delay_seconds)),
        run_duration_seconds=float(raw.get("run_duration_seconds", Config.run_duration_seconds)),
        click_type=raw.get("click_type", Config.click_type),
        click_interval_seconds=float(raw.get("click_interval_seconds", Config.click_interval_seconds)),
        stop_on_any_key=bool(raw.get("stop_on_any_key", Config.stop_on_any_key)),
        targets=targets,
    )
    _validate(config)
    return config


def validate_config(config: Config) -> Config:
    """Public wrapper around validation; raises ValueError on bad settings."""
    _validate(config)
    return config


def save_config(config: Config, path: str | Path | None = None) -> Path:
    """Write every setting of `config` to the JSON file. Returns the path."""
    config_path = Path(path) if path else default_config_path()
    data = {
        "mode": config.mode,
        "start_delay_seconds": config.start_delay_seconds,
        "run_duration_seconds": config.run_duration_seconds,
        "click_type": config.click_type,
        "click_interval_seconds": config.click_interval_seconds,
        "stop_on_any_key": config.stop_on_any_key,
        "targets": [{"x": t.x, "y": t.y} for t in config.targets],
    }
    config_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return config_path


def save_targets(targets: list[Target], path: str | Path | None = None) -> Path:
    """Write `targets` into the config file, preserving all other settings.

    If the file is missing, a complete config with defaults is created. Returns
    the path written to.
    """
    config_path = Path(path) if path else default_config_path()

    raw: dict = {}
    if config_path.exists():
        try:
            raw = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            raw = {}  # corrupt/empty file: rebuild from defaults rather than fail

    defaults = Config()
    merged = {
        "mode": raw.get("mode", defaults.mode),
        "start_delay_seconds": raw.get("start_delay_seconds", defaults.start_delay_seconds),
        "run_duration_seconds": raw.get("run_duration_seconds", defaults.run_duration_seconds),
        "click_type": raw.get("click_type", defaults.click_type),
        "click_interval_seconds": raw.get("click_interval_seconds", defaults.click_interval_seconds),
        "stop_on_any_key": raw.get("stop_on_any_key", defaults.stop_on_any_key),
        "targets": [{"x": t.x, "y": t.y} for t in targets],
    }
    config_path.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
    return config_path


def _validate(config: Config) -> None:
    """Raise ValueError on any setting that would make the run fail or misbehave."""
    if config.mode not in VALID_MODES:
        raise ValueError(f"mode must be one of {sorted(VALID_MODES)}, got {config.mode!r}")
    if config.click_type not in VALID_CLICK_TYPES:
        raise ValueError(f"click_type must be one of {sorted(VALID_CLICK_TYPES)}, got {config.click_type!r}")
    if config.click_interval_seconds < 0:
        raise ValueError("click_interval_seconds cannot be negative")
    if config.start_delay_seconds < 0:
        raise ValueError("start_delay_seconds cannot be negative")
    if config.run_duration_seconds < 0:
        raise ValueError("run_duration_seconds cannot be negative (use 0 for no limit)")
    if config.mode in MODES_NEEDING_TARGETS and not config.targets:
        raise ValueError(f"mode {config.mode!r} requires at least one entry in 'targets'")
