"""Person detection using YOLOv8 (Ultralytics).
Restricting to the 'person' class = humans only (pets/vehicles ignored).
"""
from ultralytics import YOLO

PERSON_CLASS_ID = 0  # COCO class id for 'person'


class PersonDetector:
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.5):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        results = self.model(frame, verbose=False)[0]
        detections = []
        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            if cls_id == PERSON_CLASS_ID and conf >= self.conf_threshold:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append({"bbox": (x1, y1, x2, y2), "conf": conf})
        return detections