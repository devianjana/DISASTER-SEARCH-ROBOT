import cv2
import numpy as np
import os


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WEIGHTS_PATH = os.path.join(SCRIPT_DIR, "yolov3.weights")
CONFIG_PATH = os.path.join(SCRIPT_DIR, "yolov3.cfg")
NAMES_PATH = os.path.join(SCRIPT_DIR, "coco.names")

if not os.path.exists(WEIGHTS_PATH) or not os.path.exists(CONFIG_PATH) or not os.path.exists(NAMES_PATH):
    print("\n\nERROR: One or more model files (yolov3.weights, yolov3.cfg, coco.names) not found.")
    print(f"Expected location: {SCRIPT_DIR}")
    print("Please ensure these three large files are in the same folder as this script.")
    exit() 

try:
    NET = cv2.dnn.readNet(WEIGHTS_PATH, CONFIG_PATH)
    LAYER_NAMES = NET.getLayerNames()
    OUTPUT_LAYERS = [LAYER_NAMES[i - 1] for i in NET.getUnconnectedOutLayers()]
except cv2.error as e:
    print(f"\n\nCRITICAL OpenCV Error during model loading: {e}")
    print("This often means the file names or paths in the config above are wrong, or the yolov3 files are corrupted.")
    exit()


CLASSES = []
