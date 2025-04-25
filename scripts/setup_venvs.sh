#!/bin/bash
echo "🔧 Setting up Python virtual environments..."

BASE_DIR=$(cd "$(dirname "$0")/.."; pwd)

if [[ "$OS" == "Windows_NT" ]]; then
  APP_PY="$BASE_DIR/AI_Control/app-venv/Scripts/python.exe"
  CAM_PY="$BASE_DIR/AI_Control/cam-venv/Scripts/python.exe"
else
  APP_PY="$BASE_DIR/AI_Control/app-venv/bin/python"
  CAM_PY="$BASE_DIR/AI_Control/cam-venv/bin/python"
fi

python3 -m venv "$BASE_DIR/AI_Control/app-venv"
"$APP_PY" -m pip install --upgrade pip
"$APP_PY" -m pip install -r "$BASE_DIR/AI_Control/req_app.py.txt"

python3 -m venv "$BASE_DIR/AI_Control/cam-venv"
"$CAM_PY" -m pip install --upgrade pip
"$CAM_PY" -m pip install -r "$BASE_DIR/AI_Control/requirements_camera_client.txt"

echo "✅ Virtual environments are ready."
