import subprocess
from flask import Flask

app = Flask(__name__)

@app.route('/start-camera', methods=['POST'])
def start_camera():
    try:
        # Use venv python executable
        venv_python = './cam-venv/bin/python'  # Linux/Mac
        # venv_python = '.\\cam-venv\\Scripts\\python.exe'  # Windows
        
        subprocess.Popen([venv_python, 'camera_client.py'])
        return "Camera client started in venv!", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)