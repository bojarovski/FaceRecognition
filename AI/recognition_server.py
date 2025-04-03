from flask import Flask, request, jsonify
import face_recognition
import cv2
import numpy as np
import pickle
import base64
import os

app = Flask(__name__)

# Load known faces from pickle file
# (Must be in the same folder as recognition_server.py inside container)
if os.path.exists('known_faces.pkl'):
    with open('known_faces.pkl', 'rb') as f:
        known_face_encodings, known_face_names = pickle.load(f)
else:
    known_face_encodings, known_face_names = [], []

@app.route('/recognize', methods=['POST'])
def recognize():
    """Receive a base64-encoded image, run face recognition, return names."""
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    try:
        # Decode base64 -> np array
        img_data = base64.b64decode(data['image'])
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except Exception as e:
        return jsonify({'error': f'Failed to decode image: {e}'}), 400

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    recognized = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
        name = "Unknown"
        if True in matches:
            match_index = matches.index(True)
            name = known_face_names[match_index]
        recognized.append(name)

    return jsonify({"recognized_faces": recognized}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
