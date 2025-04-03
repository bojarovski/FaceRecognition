import cv2
import time
import requests
import base64
import numpy as np
import threading
from queue import Queue
from requests.exceptions import ConnectionError, Timeout

SERVER_URL = 'http://127.0.0.1:5000/recognize'  # Update with your server URL

class APIWorker:
    def __init__(self):
        self.last_message = ""
        self.message_expiry = 0
        self.lock = threading.Lock()
        self.request_queue = Queue(maxsize=1)  # Only keep latest frame

    def send_frame_async(self, frame):
        """Add frame to queue for processing"""
        try:
            # Clear previous frame if not processed yet
            if self.request_queue.full():
                self.request_queue.get_nowait()
            self.request_queue.put_nowait(frame.copy())
        except:
            pass

    def process_queue(self):
        """Worker thread function to process frames from queue"""
        while True:
            try:
                frame = self.request_queue.get(timeout=1)
                self._send_to_server(frame)
            except:
                pass

    def _send_to_server(self, frame):
        """Handle API communication"""
        try:
            _, buffer = cv2.imencode('.jpg', frame)
            image_data = base64.b64encode(buffer).decode('utf-8')
            response = requests.post(SERVER_URL, json={'image': image_data}, timeout=1)
            
            if response.ok:
                data = response.json()
                names = data.get('recognized_faces', [])
                message = ", ".join(names) if names else "No recognized faces"
                print(f"Recognized: {message}")
            else:
                message = f"Server error: {response.status_code}"
        except ConnectionError:
            message = "⚠️ Server offline"
        except Timeout:
            message = "⚠️ Response timeout"
        except Exception as e:
            message = f"⚠️ Error: {str(e)}"

        with self.lock:
            self.last_message = message
            self.message_expiry = time.time() + 3

def fit_to_fullscreen(frame, screen_width, screen_height):
    """Resize frame to fit screen with letterboxing"""
    h, w = frame.shape[:2]
    scale = min(screen_width/w, screen_height/h)
    new_w, new_h = int(w*scale), int(h*scale)
    resized = cv2.resize(frame, (new_w, new_h))
    
    fullscreen = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
    y = (screen_height - new_h) // 2
    x = (screen_width - new_w) // 2
    fullscreen[y:y+new_h, x:x+new_w] = resized
    return fullscreen

def draw_toast(frame, message, screen_width, screen_height):
    """Draw semi-transparent message at bottom center"""
    if not message:
        return frame

    overlay = frame.copy()
    text = message.upper()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.2 if len(text) < 20 else 0.8
    thickness = 2

    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    x = (screen_width - text_w) // 2
    y = screen_height - 50

    cv2.rectangle(overlay,
                 (x - 20, y - text_h - 20),
                 (x + text_w + 20, y + 20),
                 (0, 0, 0), -1)

    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    cv2.putText(frame, text, (x, y), font, font_scale, 
               (255, 255, 255), thickness, cv2.LINE_AA)
    return frame

def get_screen_resolution():
    """Get primary display resolution"""
    try:
        import tkinter as tk
        root = tk.Tk()
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        root.destroy()
        return width, height
    except:
        return 1920, 1080  # Fallback resolution

def capture_and_send():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera")
        return

    # Initialize API worker and start processing thread
    api_worker = APIWorker()
    processing_thread = threading.Thread(target=api_worker.process_queue)
    processing_thread.daemon = True
    processing_thread.start()

    # Window setup
    time.sleep(0.1)  # Allow camera to warm up
    cv2.namedWindow("Face Recognition", cv2.WND_PROP_FULLSCREEN)
    time.sleep(0.1)  # Allow camera to warm up
    cv2.setWindowProperty("Face Recognition", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    screen_width, screen_height = get_screen_resolution()

    last_sent_time = 0
    fps_counter = 0
    fps_time = time.time()

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            current_time = time.time()

            # Send frame every 0.5s without blocking
            if current_time - last_sent_time >= 0.5:
                api_worker.send_frame_async(frame)
                last_sent_time = current_time

            # Get current message safely
            with api_worker.lock:
                current_message = api_worker.last_message
                message_expiry = api_worker.message_expiry

            # Draw UI elements
            if time.time() < message_expiry:
                frame = draw_toast(frame, current_message, screen_width, screen_height)

            # Calculate FPS
            fps_counter += 1
            if current_time - fps_time >= 1:
                # print(f"FPS: {fps_counter}")
                fps_counter = 0
                fps_time = current_time

            # Display handling
            fullscreen_frame = fit_to_fullscreen(frame, screen_width, screen_height)
            cv2.imshow("Face Recognition", fullscreen_frame)

            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_send()