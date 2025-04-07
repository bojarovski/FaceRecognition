#!/bin/bash
echo "📷 Starting Flask backend..."

BASE_DIR=$(cd "$(dirname "$0")/.."; pwd)

if [[ "$OS" == "Windows_NT" ]]; then
  "$BASE_DIR/AI_Control/app-venv/Scripts/python.exe" "$BASE_DIR/AI_Control/app.py"
else
  "$BASE_DIR/AI_Control/app-venv/bin/python" "$BASE_DIR/AI_Control/app.py"
fi
