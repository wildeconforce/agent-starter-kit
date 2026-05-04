@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ========================================
REM AI Agent Auto-Start Script (v4)
REM Auto-runs when PC boots
REM Korean messages come from bot.py via Python (UTF-8 safe)
REM ========================================

cd /d "%USERPROFILE%\Desktop"

if not exist "bot.py" (
    echo.
    echo [ERROR] bot.py not found at %USERPROFILE%\Desktop\bot.py
    echo Please complete STEP 4 of the guide first.
    echo.
    pause
    exit /b 1
)

echo [INFO] Waiting 10 seconds for network...
timeout /t 10 /nobreak >nul

set RESTART_COUNT=0
set MAX_RESTART=5

:run_bot
echo.
echo ========================================
echo [%date% %time%] Starting AI Agent (attempt #!RESTART_COUNT!)
echo ========================================

python "%USERPROFILE%\Desktop\bot.py"
set EXIT_CODE=!errorlevel!

echo.
echo [%date% %time%] Bot exited (code: !EXIT_CODE!)

if "!EXIT_CODE!"=="0" (
    echo Normal exit. Run this file again to restart.
    pause
    exit /b 0
)

set /a RESTART_COUNT+=1
if !RESTART_COUNT! geq !MAX_RESTART! (
    echo.
    echo [WARN] !MAX_RESTART! consecutive failures. Auto-restart stopped.
    echo Check:
    echo   1. GOOGLE_API_KEY in bot.py
    echo   2. TELEGRAM_BOT_TOKEN in bot.py
    echo   3. ALLOWED_USER_IDS contains your Telegram user id
    echo   4. Internet connection
    echo.
    pause
    exit /b 1
)

echo Restarting in 5 seconds...
timeout /t 5 /nobreak >nul
goto run_bot
