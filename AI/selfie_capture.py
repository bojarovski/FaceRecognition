import cv2
import os
import time

def capture_selfie():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return None
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("Error: Failed to capture image.")
        return None
    
    return frame

def main():
    photos_dir = "photos"
    if not os.path.exists(photos_dir):
        os.makedirs(photos_dir)
    
    while True:
        input("Press Enter to capture a selfie...")
        frame = capture_selfie()
        if frame is None:
            continue
        
        cv2.imshow("Captured Selfie", frame)
        print("A window has opened showing your selfie. Close the window to continue.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        choice = input("Do you like this photo? (y/n): ").strip().lower()
        if choice == 'y':
            # Save the image with a timestamp filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(photos_dir, f"selfie_{timestamp}.png")
            cv2.imwrite(filename, frame)
            print(f"Photo saved as {filename}")
            break
        else:
            print("Let's try again.\n")

if __name__ == '__main__':
    main()
