# app.py
import subprocess
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def start_camera():
    try:
        # Run the camera_client.py script
        subprocess.Popen(["python", "client_camera.py"])  # Use Popen to run it asynchronously
        return "Camera client started successfully!", 200
    except Exception as e:
        return f"Error starting the camera client: {str(e)}", 500
@app.route('/start-camera', methods=['POST'])
def start_camera():
    try:
        # Run the camera_client.py script
        subprocess.Popen(["python", "client_camera.py"])  # Use Popen to run it asynchronously
        return "Camera client started successfully!", 200
    except Exception as e:
        return f"Error starting the camera client: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
