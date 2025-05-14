from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import platform

app = Flask(__name__)
CORS(app)

process = None
HERE = os.path.dirname(os.path.abspath(__file__))
@app.route("/start-camera", methods=["POST"])
def start_camera():
    global process
    if process and process.poll() is None:
        return jsonify(message="Camera is already running ❗"), 409

    event_id = request.json.get("eventId")          # ← NEW
    if not event_id:
        return jsonify(error="eventId missing"), 400

    # 1️⃣ write it to a tiny file (fallback for the script)
    with open(os.path.join(HERE, "current_event_id.txt"), "w") as fh:
        fh.write(event_id.strip())

    # 2️⃣ expose it as an env-var (primary path)
    venv_python = os.path.join(
        HERE, "cam-venv", "Scripts" if platform.system() == "Windows" else "bin",
        "python"
    )
    env = os.environ.copy()
    env["ACTIVE_EVENT_ID"] = event_id               # ← NEW
    script = os.path.join(HERE, "camera_client.py")

    print(f"▶️  Starting kiosk for event {event_id}")
    process = subprocess.Popen([venv_python, script], env=env)
    return jsonify(message="Camera client started ✅"), 200


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