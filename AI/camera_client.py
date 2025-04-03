import cv2
import time
import requests
import base64
import numpy as np
from requests.exceptions import ConnectionError, Timeout

SERVER_URL = 'http://localhost:5000/recognize'  # Update with your server URL

def fit_to_fullscreen(frame, screen_width, screen_height):
    """Resize frame to fit screen with letterboxing."""
    h, w = frame.shape[:2]
    scale = min(screen_width/w, screen_height/h)
    new_w, new_h = int(w*scale), int(h*scale)
    resized = cv2.resize(frame, (new_w, new_h))
    
    # Center on black background
    fullscreen = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
    y = (screen_height - new_h) // 2
    x = (screen_width - new_w) // 2
    fullscreen[y:y+new_h, x:x+new_w] = resized
    return fullscreen

def draw_toast(frame, message, screen_width, screen_height):
    """Draw semi-transparent message at bottom center."""
    if not message:
        return frame

    # Create overlay
    overlay = frame.copy()
    text = message.upper()
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.2 if len(text) < 20 else 0.8
    thickness = 2

    # Calculate text size
    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Text position
    x = (screen_width - text_w) // 2
    y = screen_height - 50

    # Background rectangle
    cv2.rectangle(overlay,
                 (x - 20, y - text_h - 20),
                 (x + text_w + 20, y + 20),
                 (0, 0, 0), -1)

    # Blend and add text
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    cv2.putText(frame, text, (x, y), font, font_scale, 
               (255, 255, 255), thickness, cv2.LINE_AA)
    return frame

def get_screen_resolution():
    """Get primary display resolution."""
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

    # Window setup
    cv2.namedWindow("Face Recognition", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Face Recognition", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    screen_width, screen_height = get_screen_resolution()

    last_message = ""
    message_expiry = 0
    last_sent_time = 0

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            current_time = time.time()

            # Send frame every 0.5 seconds
            if current_time - last_sent_time >= 0.5:
                # Encode and send
                _, buffer = cv2.imencode('.jpg', frame)
                image_data = base64.b64encode(buffer).decode('utf-8')
                
                try:
                    response = requests.post(SERVER_URL, json={'image': image_data}, timeout=1)
                    if response.ok:
                        data = response.json()
                        names = data.get('recognized_faces', [])
                        last_message = ", ".join(names) if names else "No recognized faces"
                    else:
                        last_message = f"Server error: {response.status_code}"
                except ConnectionError:
                    last_message = "⚠️ Server offline"
                except Timeout:
                    last_message = "⚠️ Response timeout"
                except Exception as e:
                    last_message = f"⚠️ Error: {str(e)}"

                finally:
                    print(f"Sent frame to server. Response: {last_message}")
                
                message_expiry = current_time + 3  # Show message for 3 seconds
                last_sent_time = current_time

            # Display handling
            if current_time < message_expiry:
                frame = draw_toast(frame, last_message, screen_width, screen_height)
            
            # Show fullscreen frame
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