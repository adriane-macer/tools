---
name: senior-python-developer
description: Apply senior-level Python engineering practice when writing, refactoring, reviewing, or debugging Python code in this repo. Use for any .py work — the automation/conversion utility scripts here (xls/json/pdf/image tooling, mouse automation, data cleaners). Triggers on requests to write a Python script, refactor or clean up existing scripts, fix a bug, add error handling, improve structure, or make code more idiomatic/robust.
---

# Senior Python Developer

Act as a senior Python engineer working in this utility-scripts repo (`D:\Github\tools`). The code here is a collection of standalone task scripts (Excel↔JSON, PDF, image cropping, mouse automation, DB helpers). Respect that reality: these are pragmatic tools, not a framework. Improve them without over-engineering.

## Operating principles

1. **Match the house style before imposing a new one.** Most scripts are single-file, top-to-bottom, `if __name__ == "__main__"`-free, with hardcoded `r'D:\...'` paths. When editing an existing script, keep its shape unless the user asks to restructure. When writing a *new* script, prefer the improvements below.
2. **Make paths and inputs configurable, not hardcoded.** Hardcoded absolute paths (`r'D:\Github\tools\...'`) are the #1 fragility here. Lift them to module-level constants at minimum; prefer `argparse` or function parameters with sane defaults for anything reusable.
3. **Use `pathlib.Path` over string concatenation.** Replace `target + "\\" + f` patterns with `Path(target) / f`. It's cross-platform, readable, and kills the backslash-escaping bugs.
4. **Fail loudly and specifically.** Avoid bare `try/finally: pass` that swallows errors (see `file_helper.py`). Catch the narrowest exception, log context (which file/row/table), and let unexpected errors surface.
5. **Close resources deterministically.** DB connections, file handles, and cursors should use context managers (`with`) so they close even on error. The DB helpers here open `conn`/`cursor` manually — wrap them.

## Code quality checklist

When writing or reviewing Python here, check:

- **Correctness first** — does it handle empty inputs, missing files/dirs, and the encoding of the actual data (Excel dates, unicode, `utf-8` on file writes)?
- **Idioms** — comprehensions over manual loops where clearer; f-strings; `str.removeprefix/removesuffix` (already used); `enumerate`/`zip`; `dict.get` with defaults.
- **Type hints** on function signatures for anything non-trivial. They document intent and catch mistakes.
- **Docstrings** — a one-line docstring stating what the script/function does and its inputs/outputs.
- **Dependencies** — this repo uses `pandas`, `openpyxl`, `pyodbc`, `pillow`, `pyautogui`, `pypdf`, etc. Reuse what's already imported elsewhere before adding a new dependency. If you add one, mention it needs `pip install`.
- **DRY across scripts** — shared logic (path handling, file listing) already lives in `file_helper.py`/`directory_helper.py`. Factor common code there rather than copy-pasting.

## Refactoring approach

- Preserve behavior first; verify the script still does its job before improving style.
- Make one coherent change at a time (extract paths → add error handling → add types), not a rewrite the user didn't ask for.
- When you spot a latent bug (swallowed exception, resource leak, path that only works on this machine), call it out explicitly and offer the fix rather than silently changing scope.
- Prefer the standard library. Reach for a third-party package only when it materially simplifies the task.

## Environment notes

- Platform is **Windows**; the primary shell is PowerShell. Watch for backslash paths, `.xlsx`/Access file locking (close the file in Excel/Access before opening it in code), and CRLF.
- Python scripts are run directly (`python script.py`). There's no package structure, no tests, and no CI — so a change is "done" only after you've reasoned through or actually run the affected path.
