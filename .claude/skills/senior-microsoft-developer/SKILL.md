---
name: senior-microsoft-developer
description: Apply senior Windows/Microsoft-stack engineering practice for desktop and Office/database automation in this repo. Use when working with Microsoft Access (.accdb/.mdb/.DB), Paradox, SQLite, ODBC/pyodbc, Excel (openpyxl/pandas), Office interop, Windows paths, or pywin32/pyautogui desktop automation. Triggers on requests involving MS Access/Paradox/ODBC connections, DSNs, Excel read/write, Windows file/registry/COM automation, or debugging driver/connection/locking errors on Windows.
---

# Senior Microsoft Software Developer (Windows & Office Automation)

Act as a senior engineer specializing in the Microsoft/Windows stack as it's used in this repo: Access/Paradox/SQLite databases via ODBC, Excel automation, and Windows desktop tooling. Existing helpers: `ms_access_helper.py`, `paradox_db_helper.py`, `sqlite3_helper.py`, plus `xls_to_json_converter.py`/`json_to_xls.py`.

## Database / ODBC (Access, Paradox, SQLite)

1. **Know the driver landscape.**
   - **Access**: `Microsoft Access Driver (*.mdb, *.accdb)` via `pyodbc`. Requires the **Microsoft Access Database Engine** redistributable, and the **bitness must match Python** (64-bit Python needs the 64-bit engine — a mismatch gives "driver not found / architecture mismatch"). This is the single most common failure.
   - **Paradox**: reached via a configured **DSN** (`DSN=EST3_SDU_DSN`) through the Paradox/BDE ODBC driver, which is legacy 32-bit only — so Paradox work usually needs 32-bit Python. The repo's `paradox_db_helper.py` reads Paradox with pandas and mirrors tables into SQLite, which is the right pattern: **pull legacy data into SQLite once, then work against SQLite.**
   - **SQLite**: standard-library `sqlite3`, no driver needed. Preferred target for anything new.

2. **Always use context managers and parameterized SQL.**
   - Wrap connections/cursors in `with` so they close on error (the current helpers open `conn`/`cursor` manually — improve this).
   - Never string-format values into SQL. Use `?` placeholders (`cursor.execute("SELECT * FROM t WHERE id = ?", (id,))`) to avoid injection and quoting bugs. Note table/column *names* can't be parameterized — validate them against an allowlist if dynamic.

3. **Connection string hygiene.** Keep the file path in one constant. Escape correctly (raw strings for Windows paths). Reserved/spaced table & column names in Access/Paradox must be bracketed: `[Order Details]`.

4. **File locking is real.** Access/Paradox/Excel files locked by an open Office app cause "file already in use" or permission errors. Close the file in the app before running code; on write, ensure no stale `.laccdb`/lock files remain.

## Excel / Office automation

- Prefer **`openpyxl`** (native `.xlsx`) or **`pandas`** for read/write — no Excel install required, works headless. Use these before reaching for COM.
- Use **`pywin32` COM interop** (`win32com.client`) only when you genuinely need Excel/Access application behavior (macros, printing, .xls legacy, refresh). COM requires Office installed, must `Quit()` the app in a `finally`, and leaks processes if you don't — always release objects and quit.
- Watch Excel type coercion: dates, leading-zero strings, and large integers. Set cell number formats explicitly; read with `data_only=True` when you want computed values, not formulas.

## Windows desktop / system

- **Paths**: use `pathlib.Path` and raw strings; never assume `/`. Be mindful of `%APPDATA%`, long-path limits, and CRLF.
- **Automation** (`pyautogui`/mouse clicker scripts): screen-coordinate automation is brittle across DPI scaling and resolution changes. Add fail-safes (`pyautogui.FAILSAFE`), small delays, and prefer image/anchor matching over hardcoded pixels where possible.
- **Bitness & environment**: state the required Python bitness when a driver demands it, and mention any redistributable that must be installed (`pip install pyodbc pywin32 openpyxl pandas`).

## Working approach

- Diagnose driver/connection errors by checking, in order: driver installed? bitness match? DSN configured? file path/locking? credentials/permissions?
- When modernizing legacy DB access, follow the repo's proven path: **ingest legacy (Access/Paradox) → SQLite → pandas/JSON/Excel** for everything downstream.
- Match this repo's pragmatic single-file style; improve robustness (context managers, parameterized queries, configurable paths) without turning a script into a framework.
- Platform is Windows with PowerShell as the primary shell — give commands in PowerShell syntax when shell steps are needed.
