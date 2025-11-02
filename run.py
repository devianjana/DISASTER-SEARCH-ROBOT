import cv2
import time
from object_detector import ObjectDetector 
VIDEO_SOURCE = 0 
def main_simulation():
    detector = ObjectDetector()
    print("ObjectDetector initialized successfully.")
    cap = cv2.VideoCapture(VIDEO_SOURCE)

