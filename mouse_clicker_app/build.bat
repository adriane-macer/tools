@echo off
REM Build MouseClicker.exe with PyInstaller. Double-click or run from a shell.
REM Uses "python -m PyInstaller" so it works even when the Scripts dir
REM (where pyinstaller.exe lives) is not on PATH.
setlocal
cd /d "%~dp0"

echo ============================================
echo   Building MouseClicker.exe
echo ============================================

REM Ensure PyInstaller + runtime deps are importable (build-only for PyInstaller).
python -c "import PyInstaller" >nul 2>nul
if errorlevel 1 (
    echo [build] Installing build/runtime dependencies...
    python -m pip install -r requirements.txt pyinstaller
    if errorlevel 1 (
        echo [build] Failed to install build dependencies.
        exit /b 1
    )
)

echo [build] Running PyInstaller ^(--onefile, console^)...
python -m PyInstaller --noconfirm --clean --onefile --console --name MouseClicker ^
    --collect-submodules pynput --collect-submodules pyautogui main.py
if errorlevel 1 (
    echo [build] BUILD FAILED.
    exit /b 1
)

echo [build] Placing an editable config.json next to the exe...
copy /y config.json dist\config.json >nul

echo.
echo [build] Done.
echo [build]   Executable : dist\MouseClicker.exe
echo [build]   Config     : dist\config.json  ^(edit this to configure^)
echo.
echo [build] Note: Windows SmartScreen/antivirus may flag a fresh unsigned exe.
echo [build] This is a common false positive for input-automation tools.
endlocal
