#!/usr/bin/env python3
"""
Kiosk client **with face-ID + emotion** agents  (macOS M-series)
================================================================
Face recognition  → http://localhost:5001/recognize
Emotion detection → http://localhost:5002/analyse
"""

import base64
import os               # ← need this for ENV + txt-file lookup
import threading
import time
from queue import Queue, Empty
from typing import Callable, List

import cv2
import numpy as np
import requests
from requests.exceptions import ConnectionError, Timeout

# ─── Configuration ───────────────────────────────────────────
MESSAGE_LIFETIME = 3     # toast line lifetime

AGENT_SPECS: List[dict] = [
    {
        "name": "faces",
        "url": "http://localhost:5001/recognize",
        "interval": 1,  
        "parse": lambda js: ", ".join(js.get("recognized_faces", [])) or "No faces",
    },
    {
        "name": "emotion",
        "url": "http://localhost:5002/analyse",
        "interval": 1, 
        "parse": lambda js: (
            "No emotion"
            if not js.get("emotions")
            else (
                lambda best: f"{best['emotion'].title()} ({int(best['confidence']*100)}%)"
            )(max(js["emotions"], key=lambda d: d["confidence"]))
        ),
    },
]


# ─── Dynamic event-ID helper ─────────────────────────────────
def load_event_id() -> str | None:
    """ENV var has priority, fallback to the tiny text-file."""
    eid = os.getenv("ACTIVE_EVENT_ID")
    if eid:
        return eid
    try:
        with open(os.path.join(os.path.dirname(__file__), "current_event_id.txt")) as fh:
            return fh.read().strip()
    except FileNotFoundError:
        return None

EVENT_ID = load_event_id()
if not EVENT_ID:
    print("⚠️  No ACTIVE_EVENT_ID found – attendance logging disabled")

# ─── Background worker  (one per HTTP agent) ────────────────
class APIWorker(threading.Thread):
    """Uploads frames to one service and keeps its latest toast message."""

    def __init__(self, name: str, url: str, parse_fn: Callable[[dict], str], interval: float):
        super().__init__(daemon=True)
        self.name = name
        self.url = url
        self.parse_fn = parse_fn
        self.interval = interval
        self.queue = Queue(maxsize=1)
        self.last_message = ""
        self.message_expiry = 0.0
        self.last_sent_time = 0.0  # NEW: track per-agent send time
        self.lock = threading.Lock()


    def enqueue(self, frame: np.ndarray):
        now = time.time()
        if now - self.last_sent_time < self.interval:
            return  # Skip sending if interval hasn't passed
        self.last_sent_time = now

        try:
            resized = cv2.resize(frame, (640, 480))  # Resize to speed up API
            if self.queue.full():
                self.queue.get_nowait()
            self.queue.put_nowait(resized)
        except Exception as e:
            print(f"[{self.name}] Failed to enqueue frame: {e}")


    # thread main
    def run(self):
        while True:
            try:
                frame = self.queue.get(timeout=1)
                self._call_api(frame)
            except Empty:
                pass

    # internal – talk to one HTTP service
    def _call_api(self, frame: np.ndarray):
        try:
            ok, buf = cv2.imencode(".jpg", frame)
            if not ok:
                raise RuntimeError("JPEG encode failed")

            payload = {"image": base64.b64encode(buf).decode()}
            res     = requests.post(self.url, json=payload, timeout=10)

            if res.ok:
                msg = self.parse_fn(res.json())

                # ── Attendance logging (only for face-agent) ──
                if self.name == "faces" and EVENT_ID:
                    for person in res.json().get("recognized_faces", []):
                        try:
                            # Save JPEG of current image for emotion analysis
                            image_b64 = base64.b64encode(buf).decode()

                            att_res = requests.post(
                                "http://localhost:5050/attendance/by-name",
                                json={"eventId": EVENT_ID, "name": person},
                                timeout=5,
                            )

                            if att_res.status_code == 201:
                                # Call emotion detection ONLY if attendance was new
                                emo_res = requests.post(
                                    "http://localhost:5002/analyse",
                                    json={"image": image_b64},
                                    timeout=5,
                                )
                                if emo_res.ok:
                                    emo_payload = emo_res.json()
                                    try:
                                        # Send to logging route
                                        requests.post(
                                            "http://localhost:5050/attendance/emotion-detected",
                                            json={
                                                "eventId": EVENT_ID,
                                                "name": person,
                                                "emotion": emo_payload.get("emotions", []),
                                            },
                                            timeout=5,
                                        )
                                    except Exception as log_exc:
                                        print(f"[Emotion log] {person}: {log_exc}")
                                else:
                                    print(f"[Emotion API] {emo_res.status_code}")
                        except Exception as exc:
                            print(f"[Attendance] {person}: {exc}")

            else:
                msg = f"{self.name}: HTTP {res.status_code}"

        except ConnectionError:
            msg = f"{self.name}: server offline"
        except Timeout:
            msg = f"{self.name}: timeout"
        except Exception as exc:
            msg = f"{self.name}: {exc}"
        finally:
            with self.lock:
                self.last_message   = msg
                self.message_expiry = time.time() + MESSAGE_LIFETIME

# ─── Drawing helpers ──────────────────────────────────────────────────────────

def fit_to_fullscreen(frame: np.ndarray, screen_w: int, screen_h: int) -> np.ndarray:
    h, w = frame.shape[:2]
    scale = min(screen_w / w, screen_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(frame, (new_w, new_h))
    canvas = np.zeros((screen_h, screen_w, 3), dtype=np.uint8)
    y, x = (screen_h - new_h) // 2, (screen_w - new_w) // 2
    canvas[y : y + new_h, x : x + new_w] = resized
    return canvas

def draw_toast(frame: np.ndarray, message: str, screen_w: int, screen_h: int) -> np.ndarray:
    if not message:
        return frame
    overlay = frame.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8 if len(message) > 25 else 1.1
    thickness = 2
    (tw, th), _ = cv2.getTextSize(message, font, font_scale, thickness)
    x = (screen_w - tw) // 2
    y = screen_h - 50
    cv2.rectangle(overlay, (x - 20, y - th - 20), (x + tw + 20, y + 20), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    cv2.putText(frame, message, (x, y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
    return frame

# ─── Utilities ───────────────────────────────────────────────────────────────

import AppKit

def get_screen_resolution() -> tuple[int, int]:
    screen = AppKit.NSScreen.mainScreen()
    frame = screen.frame()
    return int(frame.size.width), int(frame.size.height)


def open_camera(index: int = 0) -> cv2.VideoCapture:
    for backend in (cv2.CAP_AVFOUNDATION, cv2.CAP_QT):
        cap = cv2.VideoCapture(index, backend)
        if cap.isOpened():
            print(f"✅ Opened camera {index} via backend {backend}")
            return cap
        cap.release()
    raise RuntimeError("Camera permission missing? Grant it in System Settings › Privacy & Security › Camera.")

# ─── Main loop ───────────────────────────────────────────────────────────────
def capture_and_send(device_index: int = 0):
    cap = open_camera(device_index)

    workers = [
        APIWorker(s["name"], s["url"], s["parse"], s["interval"])
        for s in AGENT_SPECS
    ]

    for w in workers:
        w.start()
    
    cv2.namedWindow("Kiosk", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Kiosk", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    screen_w, screen_h = get_screen_resolution()

    last_sent = 0.0
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("⚠️  Camera read failed – exiting")
                break

            now = time.time()
            for w in workers:
                w.enqueue(frame)
                

            # build toast line
            messages = []
            for w in workers:
                with w.lock:
                    if now < w.message_expiry and w.last_message:
                        messages.append(w.last_message)
            toast = "  •  ".join(messages)

            cv2.imshow(
                "Kiosk",
                fit_to_fullscreen(
                    draw_toast(frame, toast, screen_w, screen_h),
                    screen_w,
                    screen_h,
                ),
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

# ─── Entry point ────────────────────────────────────────────
if __name__ == "__main__":
    capture_and_send()