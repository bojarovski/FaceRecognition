# AI_Control/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess, os, platform

app = Flask(__name__)
CORS(app)

process = None

def _python_path():
    here = os.path.dirname(os.path.abspath(__file__))
    if platform.system() == "Windows":
        return os.path.join(here, "cam-venv", "Scripts", "python.exe")
    return os.path.join(here, "cam-venv", "bin", "python")

@app.route('/start-camera', methods=['POST'])
def start_camera():
    global process
    data = request.get_json() or {}
    event_id = data.get("eventId")
    if not event_id:
        return jsonify(error="eventId is required"), 400

    if process and process.poll() is None:
        return jsonify(message="Camera is already running ❗"), 409

    # figure out paths
    script = os.path.join(os.path.dirname(__file__), "camera_client.py")
    python_exec = _python_path()
    env = os.environ.copy()
    env["EVENT_ID"] = event_id

    # ==== DEBUG LOGS ====
    print(f"[Flask] Launching camera_client.py for EVENT_ID={event_id}")
    print(f"[Flask] Python interpreter: {python_exec}")
    print(f"[Flask] Script path:      {script}")

    try:
        process = subprocess.Popen([python_exec, script], env=env)
        print(f"[Flask] Spawned camera_client, PID={process.pid}")
        return jsonify(message="Camera client started ✅"), 200
    except Exception as e:
        print(f"[Flask] ERROR spawning camera_client.py: {e}")
        return jsonify(error=str(e)), 500

@app.route('/stop-camera', methods=['POST'])
def stop_camera():
    global process
    if process and process.poll() is None:
        print(f"[Flask] Stopping camera_client, PID={process.pid}")
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            print(f"[Flask] WARNING: PID={process.pid} did not terminate")
        process = None
        return jsonify(message="Camera client stopped ✅"), 200

    return jsonify(message="Camera is not running ❗"), 409

if __name__ == '__main__':
    print("[Flask] Starting camera-control bridge on port 4000")
    app.run(host='0.0.0.0', port=4000)
