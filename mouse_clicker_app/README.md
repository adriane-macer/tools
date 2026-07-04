# Mouse Clicker App

Configurable console mouse clicker. Phase 1 of the plan in
[`../docs/mouse_clicker_app_design.md`](../docs/mouse_clicker_app_design.md).
Task tracker: [`../docs/mouse_clicker_app_tasks.md`](../docs/mouse_clicker_app_tasks.md).

## Install
```powershell
pip install -r requirements.txt
```

## Run
```powershell
python main.py                          # uses config.json in this folder
python main.py --mode click_here --duration 30
python main.py --config myconfig.json
python main.py --record                 # capture target coordinates (see below)
python main.py --gui                     # launch the graphical UI (see below)
```

Press **any key** to stop. As a hardware backup, slam the mouse into a screen
corner to trigger PyAutoGUI's FAILSAFE abort.

## Configuration (`config.json`)
| Key | Meaning |
|-----|---------|
| `mode` | `click_here`, `click_fixed`, `move_only`, or `move_and_click` |
| `start_delay_seconds` | Countdown before clicking starts (time to focus the target window) |
| `run_duration_seconds` | Auto-stop after this many seconds; `0` = run until stopped |
| `click_type` | `left`, `right`, or `double` |
| `click_interval_seconds` | Pause between clicks / moves |
| `stop_on_any_key` | `true` to enable the any-key stop listener |
| `targets` | List of `{ "x": ..., "y": ... }` used by all modes except `click_here` |

### Modes
- **click_here** — clicks repeatedly at the current cursor position.
- **click_fixed** — clicks repeatedly at `targets[0]`.
- **move_only** — moves through each target in order without clicking.
- **move_and_click** — moves to each target and clicks it, looping.

## Recording target coordinates (`--record`)
Instead of hand-copying coordinates, capture them live:
```powershell
python main.py --record          # or: MouseClicker.exe --record
```
- **F8** — capture the current cursor position
- **Backspace** — remove the last captured point
- **Esc** — finish and save

Captured points **replace** the `targets` in `config.json` (all other settings
are preserved). Afterwards set `mode` to `move_and_click` or `click_fixed` to use
them. Nothing is clicked while recording.

## Graphical UI (`--gui`)
```powershell
python main.py --gui         # or: python gui.py
```
The window has dropdowns for **mode** and **click type**, entry fields for
**delay / duration / interval**, a **stop-on-any-key** toggle, a **targets** list
with **Add current** (append the live mouse position), **Record (F8)**, **Remove**
and **Clear** buttons, plus **Start / Stop / Save config** buttons. It reuses the same `engine.run()` as the console app; the engine runs on
a background thread so the window stays responsive, and **Stop** halts it. Status
(clicks / cycles / elapsed) is shown at the bottom when a run ends.

## Build standalone .exe(s)
```powershell
.\build.bat        # dist\MouseClicker.exe     (console app)
.\build_gui.bat    # dist\MouseClickerGUI.exe  (windowed GUI app)
```
Each runs PyInstaller (installing it on first use) and produces:
- the `.exe` — standalone, no Python needed to run it
- `dist\config.json` — an editable copy read from **beside the exe**

Ship the `dist\` folder; edit `dist\config.json` to configure the packaged app.

## Notes
- Coordinates assume the display scaling used when they were recorded. If Windows
  scaling isn't 100%, offsets can appear.
- To click into an app running **as administrator**, run this elevated too.
- A fresh unsigned `.exe` may be flagged by **Windows SmartScreen / antivirus** —
  a common false positive for input-automation tools. Keep the source `.py` as a
  fallback, or code-sign the exe for wider distribution.
