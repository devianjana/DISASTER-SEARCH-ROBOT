import cv2
import numpy as np
import os

# --- Path Configuration ---
# THIS IS THE CRITICAL LINE: '_file_' gets the path of the current script.
# The code finds the directory where object_detector.py lives.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WEIGHTS_PATH = os.path.join(SCRIPT_DIR, "yolov3.weights")
CONFIG_PATH = os.path.join(SCRIPT_DIR, "yolov3.cfg")
NAMES_PATH = os.path.join(SCRIPT_DIR, "coco.names")
# --------------------------

# Load YOLO
# Check if files exist before trying to load them
if not os.path.exists(WEIGHTS_PATH) or not os.path.exists(CONFIG_PATH) or not os.path.exists(NAMES_PATH):
    print("\n\nERROR: One or more model files (yolov3.weights, yolov3.cfg, coco.names) not found.")
    print(f"Expected location: {SCRIPT_DIR}")
    print("Please ensure these three large files are in the same folder as this script.")
    # We exit here because without the files, the script cannot run.
    exit() 

try:
    # Load the neural network using the configuration and weights files
    NET = cv2.dnn.readNet(WEIGHTS_PATH, CONFIG_PATH)
    LAYER_NAMES = NET.getLayerNames()
    OUTPUT_LAYERS = [LAYER_NAMES[i - 1] for i in NET.getUnconnectedOutLayers()]
except cv2.error as e:
    print(f"\n\nCRITICAL OpenCV Error during model loading: {e}")
    print("This often means the file names or paths in the config above are wrong, or the yolov3 files are corrupted.")
    exit()

# Load class names from the coco.names file
CLASSES = []
try:
    with open(NAMES_PATH, "r") as f:
        CLASSES = [line.strip() for line in f.readlines()]
except FileNotFoundError:
    print(f"ERROR: Class names file not found at {NAMES_PATH}")
    exit()

class ObjectDetector:
    """
    Handles the initialization and execution of the YOLO object detection model.
    """
    def _init_(self):
        # The model is loaded globally above.
        pass

    def detect_objects(self, frame):
        """
        Performs object detection on a single frame.

        Args:
            frame (numpy.ndarray): The input video frame.

        Returns:
            tuple: (frame with bounding boxes drawn, count of people detected)
        """
        height, width, channels = frame.shape

        # Create a blob from the image for network input
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        NET.setInput(blob)
        outs = NET.forward(OUTPUT_LAYERS)

        class_ids = []
        confidences = []
        boxes = []
        person_count = 0

        # Process the network outputs
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5: # Confidence threshold
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        # Apply Non-Maximum Suppression (NMS) to remove overlapping boxes
        # We set thresholds (0.5 for confidence, 0.4 for NMS)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        # Draw the results
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                
                # Check if class ID is 0 (the 'person' class in COCO dataset)
                if class_ids[i] == 0:
                    label = "VICTIM"
                    color = (0, 0, 255) # Red for high visibility
                    person_count += 1
                else:
                    label = str(CLASSES[class_ids[i]])
                    color = (0, 255, 0) # Green for other objects

                confidence = confidences[i]
