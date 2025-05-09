# camera_api/camera_client.py
import os, time, base64, threading
import cv2, requests
import numpy as np
from queue import Queue
from requests.exceptions import ConnectionError, Timeout

# Endpoints
SERVER_URL    = "http://localhost:5001/recognize"
ATTEND_BY_NAME = "http://localhost:5000/attendance/by-name"
EVENT_ID      = os.getenv("EVENT_ID")

class APIWorker:
    def __init__(self):
        self.lock = threading.Lock()
        self.last_message   = ""
        self.message_expiry = 0
        self.queue          = Queue(maxsize=1)
        print("[Client] APIWorker ready")

    def send_frame_async(self, frame):
        if self.queue.full():
            try: self.queue.get_nowait()
            except: pass
        try:
            self.queue.put_nowait(frame.copy())
        except: pass

    def process_queue(self):
        while True:
            try:
                frame = self.queue.get(timeout=1)
                self._send_to_server(frame)
            except:
                pass

    def _send_to_server(self, frame):
        # 1) Send to recognition server
        try:
            _, buf = cv2.imencode(".jpg", frame)
            b64    = base64.b64encode(buf).decode("utf-8")
            resp   = requests.post(SERVER_URL, json={"image": b64}, timeout=1)
            print(f"[Client] Recognize → HTTP {resp.status_code}")
        except Exception as e:
            print(f"[Client] ⚠️ Recognition error: {e}")
            return

        if not resp.ok:
            message = f"Server error: {resp.status_code}"
        else:
            names = resp.json().get("recognized_faces", [])
            print(f"[Client] Faces: {names}")

            # 2) For each name, post attendance by-name
            for nm in names:
                if not EVENT_ID:
                    continue
                try:
                    r = requests.post(
                        ATTEND_BY_NAME,
                        json={"eventId": EVENT_ID, "name": nm},
                        timeout=0.5
                    )
                    print(f"[Client] Posted attendance for “{nm}” → {r.status_code}")
                except Exception as e:
                    print(f"[Client] ⚠️ Failed attendance for “{nm}”: {e}")

            message = ", ".join(names) if names else "No faces"

        # 3) Save message for toast
        with self.lock:
            self.last_message   = message
            self.message_expiry = time.time() + 3

def fit_to_fullscreen(frame, w, h):
    fh, fw = frame.shape[:2]
    scale  = min(w/fw, h/fh)
    nw, nh = int(fw*scale), int(fh*scale)
    small  = cv2.resize(frame, (nw, nh))
    canvas = np.zeros((h, w, 3), dtype=np.uint8)
    x, y   = (w-nw)//2, (h-nh)//2
    canvas[y:y+nh, x:x+nw] = small
    return canvas

def draw_toast(frame, msg, w, h):
    if not msg: return frame
    ov    = frame.copy()
    font  = cv2.FONT_HERSHEY_SIMPLEX
    scale = 1.0
    th    = 2
    (tw, th2), _ = cv2.getTextSize(msg, font, scale, th)
    x, y = (w-tw)//2, h-50
    cv2.rectangle(ov, (x-20, y-th2-20), (x+tw+20, y+20), (0,0,0), -1)
    cv2.addWeighted(ov, 0.6, frame, 0.4, 0, frame)
    cv2.putText(frame, msg, (x, y), font, scale, (255,255,255), th)
    return frame

def get_screen_resolution():
    try:
        import tkinter as tk
        root = tk.Tk()
        w, h = root.winfo_screenwidth(), root.winfo_screenheight()
        root.destroy()
        return w, h
    except:
        return 1920, 1080

def capture_and_send():
    print("[Client] Starting capture_and_send()")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # DirectShow on Windows
    if not cap.isOpened():
        print("❌ Could not open camera")
        return

    worker = APIWorker()
    threading.Thread(target=worker.process_queue, daemon=True).start()

    cv2.namedWindow("Face Recognition", cv2.WINDOW_FULLSCREEN)
    w, h = get_screen_resolution()

    last = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Frame grab failed")
            break
        if time.time() - last >= 0.5:
            worker.send_frame_async(frame)
            last = time.time()

        with worker.lock:
            msg, exp = worker.last_message, worker.message_expiry
        if time.time() < exp:
            frame = draw_toast(frame, msg, w, h)

        disp = fit_to_fullscreen(frame, w, h)
        cv2.imshow("Face Recognition", disp)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_send()
