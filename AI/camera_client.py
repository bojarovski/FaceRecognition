import cv2
import time
import requests
import base64
import numpy as np  # <-- Needed for black bar background

SERVER_URL = 'http://localhost:5000/recognize'

def fit_to_fullscreen(frame, screen_width, screen_height):
    """
    Resize 'frame' to fit within (screen_width x screen_height) while
    preserving aspect ratio, and add black bars if needed.
    """
    h, w = frame.shape[:2]

    # Find scaling factor to fit entire frame in screen
    scale_w = screen_width / w
    scale_h = screen_height / h
    scale = min(scale_w, scale_h)  # ensures no crop

    new_width = int(w * scale)
    new_height = int(h * scale)
    resized = cv2.resize(frame, (new_width, new_height))

    # Create black background for entire screen
    fullscreen = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

    # Center the resized frame on this black background
    x_offset = (screen_width - new_width) // 2
    y_offset = (screen_height - new_height) // 2

    fullscreen[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = resized
    return fullscreen

def draw_toast(frame, message, screen_width, screen_height):
    """Draw a semi-transparent toast message at bottom center."""
    if not message:
        return frame

    overlay = frame.copy()
    alpha = 0.6

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.2
    thickness = 2
    text_size, _ = cv2.getTextSize(message, font, font_scale, thickness)
    text_width, text_height = text_size

    # Calculate position: centered bottom
    x = (screen_width - text_width) // 2
    y = screen_height - 80

    # Draw background rectangle
    box_coords = ((x - 20, y - text_height - 20), (x + text_width + 20, y + 20))
    cv2.rectangle(overlay, box_coords[0], box_coords[1], (0, 0, 0), -1)

    # Blend overlay with original
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    # Draw text
    cv2.putText(frame, message, (x, y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

    return frame

def capture_and_send():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        return

    # Make fullscreen window
    cv2.namedWindow("Face Recognition", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Face Recognition", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Get screen resolution
    screen_width = 1920
    screen_height = 1080
    try:
        import tkinter as tk
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
    except:
        pass

    last_message = ""
    message_time = 0
    last_check_time = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            current_time = time.time()

            # Send to server every 0.5 seconds
            if current_time - last_check_time >= 0.5:
                last_check_time = current_time

                _, buffer = cv2.imencode('.jpg', frame)
                jpg_as_text = base64.b64encode(buffer).decode('utf-8')

                try:
                    response = requests.post(SERVER_URL, json={'image': jpg_as_text}, timeout=1)
                    if response.ok:
                        json_data = response.json()
                        recognized = json_data.get("recognized_faces", [])
                        new_message = ", ".join(recognized) if recognized else "No face"
                    else:
                        new_message = f"Server error: {response.status_code}"
                except requests.exceptions.ConnectionError:
                    new_message = "⚠️ No backend"
                except requests.exceptions.Timeout:
                    new_message = "⚠️ Timeout"
                except Exception:
                    new_message = "⚠️ Unexpected error"

                # Update message and start timer
                last_message = new_message
                message_time = current_time

            # Display message for 3 seconds
            if current_time - message_time <= 3:
                frame = draw_toast(frame, last_message, frame.shape[1], frame.shape[0])

            # Letterbox to fit screen
            fullscreen_frame = fit_to_fullscreen(frame, screen_width, screen_height)
            cv2.imshow("Face Recognition", fullscreen_frame)

            # Quit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_send()
