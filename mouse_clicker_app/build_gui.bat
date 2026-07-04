@echo off
REM Build a windowed (no-console) GUI exe: MouseClickerGUI.exe
REM Uses "python -m PyInstaller" so it works regardless of PATH.
setlocal
cd /d "%~dp0"

echo ============================================
echo   Building MouseClickerGUI.exe (windowed)
echo ============================================

python -c "import PyInstaller" >nul 2>nul
if errorlevel 1 (
    echo [build] Installing build/runtime dependencies...
    python -m pip install -r requirements.txt pyinstaller
    if errorlevel 1 (
        echo [build] Failed to install build dependencies.
        exit /b 1
    )
)

echo [build] Running PyInstaller ^(--onefile, --windowed^)...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name MouseClickerGUI ^
    --collect-submodules pynput --collect-submodules pyautogui gui.py
if errorlevel 1 (
    echo [build] BUILD FAILED.
    exit /b 1
)

echo [build] Placing an editable config.json next to the exe...
copy /y config.json dist\config.json >nul

echo.
echo [build] Done.
echo [build]   Executable : dist\MouseClickerGUI.exe
echo [build]   Config     : dist\config.json  ^(loaded on startup^)
echo.
echo [build] Note: Windows SmartScreen/antivirus may flag a fresh unsigned exe.
endlocal
