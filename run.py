import cv2
import time
from object_detector import ObjectDetector # Import the class from object_detector.py

# --- Configuration ---
# Use 0 for the default webcam, or provide a path to a video file 
VIDEO_SOURCE = 0 
# ---------------------

def main_simulation():
    """
    Main function to run the video stream and object detection loop.
    """
    # Initialize the object detector
    detector = ObjectDetector()
    print("ObjectDetector initialized successfully.")

    # Capture video from the source
    cap = cv2.VideoCapture(VIDEO_SOURCE)

    if not cap.isOpened():
        print(f"Error: Could not open video source {VIDEO_SOURCE}")
        return

    # Initialize variables for FPS calculation
    frame_count = 0
    start_time = time.time()
    
    # Loop to process frames
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Finished processing video stream or cannot read frame.")
            break

        # 1. Run detection
        processed_frame, people_detected = detector.detect_objects(frame)
        
        # 2. Display live data
        
        # Calculate FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time if elapsed_time > 0 else 0

        # Create status text
        status_text = f"FPS: {fps:.2f} | VICTIMS DETECTED: {people_detected}"
        
        # Draw status overlay on the frame
        cv2.putText(processed_frame, status_text, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        # 3. Display the result
        cv2.imshow("Disaster Response Simulation - Object Detection", processed_frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up and release resources
    cap.release()
    cv2.destroyAllWindows()
    print("Simulation stopped.")

if __name__ == "_main_":
    main_simulation()
