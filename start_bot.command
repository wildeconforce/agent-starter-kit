#!/bin/bash
# ========================================
# AI Agent Auto-Start Script (Mac, FINAL)
# Double-click this file in Finder to run
# ========================================

cd ~/Desktop

if [ ! -f "bot.py" ]; then
    echo
    echo "[ERROR] bot.py not found at ~/Desktop/bot.py"
    echo "Please complete STEP 4 of the guide first."
    echo
    read -p "Press Enter to close..."
    exit 1
fi

echo "[INFO] Waiting 10 seconds for network..."
sleep 10

# Prefer python3 (default on macOS), fallback to python
if command -v python3 &> /dev/null; then
    PYBIN=python3
elif command -v python &> /dev/null; then
    PYBIN=python
else
    echo
    echo "[ERROR] python not found."
    echo "Install Python 3 from https://python.org/downloads"
    echo
    read -p "Press Enter to close..."
    exit 1
fi

echo "[INFO] Using $PYBIN"

RESTART_COUNT=0
MAX_RESTART=5

while true; do
    echo
    echo "========================================"
    echo "[$(date)] Starting AI Agent (attempt #$RESTART_COUNT)"
    echo "========================================"

    $PYBIN ~/Desktop/bot.py
    EXIT_CODE=$?

    echo
    echo "[$(date)] Bot exited (code: $EXIT_CODE)"

    if [ "$EXIT_CODE" -eq "0" ]; then
        echo "Normal exit. Run this file again to restart."
        read -p "Press Enter to close..."
        exit 0
    fi

    RESTART_COUNT=$((RESTART_COUNT + 1))
    if [ "$RESTART_COUNT" -ge "$MAX_RESTART" ]; then
        echo
        echo "[WARN] $MAX_RESTART consecutive failures. Auto-restart stopped."
        echo "Check:"
        echo "  1. GOOGLE_API_KEY in bot.py"
        echo "  2. TELEGRAM_BOT_TOKEN in bot.py"
        echo "  3. ALLOWED_USER_IDS contains your Telegram user id"
        echo "  4. Internet connection"
        echo
        read -p "Press Enter to close..."
        exit 1
    fi

    echo "Restarting in 5 seconds..."
    sleep 5
done
