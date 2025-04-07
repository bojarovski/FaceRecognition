from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import os
import platform

app = Flask(__name__)
CORS(app)

process = None

@app.route('/start-camera', methods=['POST'])
def start_camera():
    global process
    try:
        if process and process.poll() is None:
            return jsonify(message="Camera is already running ❗"), 409  # 409 = Conflict

        current_dir = os.path.dirname(os.path.abspath(__file__))
        venv_python = os.path.join(current_dir, "cam-venv", "Scripts", "python.exe") if platform.system() == "Windows" else os.path.join(current_dir, "cam-venv", "bin", "python")
        script_path = os.path.join(current_dir, "camera_client.py")

        print(f"▶️ Starting: {venv_python} {script_path}")
        process = subprocess.Popen([venv_python, script_path])
        return jsonify(message="Camera client started ✅"), 200

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify(error=str(e)), 500

@app.route('/stop-camera', methods=['POST'])
def stop_camera():
    global process
    try:
        if process and process.poll() is None:
            process.terminate()
            process.wait(timeout=3)
            process = None
            return jsonify(message="Camera client stopped ✅"), 200
        else:
            return jsonify(message="Camera is not running ❗"), 409  # 409 = Conflict

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
