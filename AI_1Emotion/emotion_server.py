#!/usr/bin/env python3
from flask import Flask, request, jsonify
import base64, cv2, numpy as np
from deepface import DeepFace

app = Flask(__name__)

@app.route("/analyse", methods=["POST"])
def analyse():
    data = request.get_json(force=True, silent=True)
    if not data or "image" not in data:
        return jsonify({"error": "No image provided"}), 400

    try:
        img = cv2.imdecode(
            np.frombuffer(base64.b64decode(data["image"]), np.uint8),
            cv2.IMREAD_COLOR,
        )
        if img is None:
            raise ValueError("decode failed")
    except Exception as e:
        return jsonify({"error": f"bad image: {e}"}), 400

    try:
        res = DeepFace.analyze(
            img, actions=("emotion",),
            enforce_detection=False,
            detector_backend="retinaface",
        )
        faces = res if isinstance(res, list) else [res]
    except Exception as e:
        print(f"[DeepFace error] {type(e).__name__}: {e}")
        return jsonify({"error": f"model failed: {e}"}), 500



    out = []
    for f in faces:
        if not f or "emotion" not in f:
            continue
        emo = max(f["emotion"], key=f["emotion"].get)
        conf = float(f["emotion"][emo]) / 100      # ← cast to built-in float
        region = f.get("region") or {"x": 0, "y": 0, "w": 0, "h": 0}
        out.append({
            "emotion": emo,
            "confidence": round(conf, 3),          # still a plain float
            "box": [int(region["x"]), int(region["y"]),
                    int(region["w"]), int(region["h"])],   # cast ints too
        })

    return jsonify({"emotions": out}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
