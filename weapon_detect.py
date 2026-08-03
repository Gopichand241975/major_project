
import numpy as np
from ultralytics import YOLO
import mediapipe as mp

TOOL_CLASSES = {"knife", "screwdriver", "crowbar", "hammer", "handgun"}
PROXIMITY_PX = 60


class WeaponDetector:
    def __init__(self, model_path="weapon_yolov8.pt", conf_threshold=0.5):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.pose = mp.solutions.pose.Pose(static_image_mode=False)

    def _wrist_points(self, person_crop):
        result = self.pose.process(person_crop)
        if not result.pose_landmarks:
            return []
        h, w, _ = person_crop.shape
        lm = result.pose_landmarks.landmark
        wrists = [lm[mp.solutions.pose.PoseLandmark.LEFT_WRIST],
                  lm[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]]
        return [(int(pt.x * w), int(pt.y * h)) for pt in wrists]

    def detect_in_hand(self, frame, person_bbox):
        x1, y1, x2, y2 = person_bbox
        person_crop = frame[max(0, y1):y2, max(0, x1):x2]
        if person_crop.size == 0:
            return None
        wrists = self._wrist_points(person_crop)
        if not wrists:
            return None
        results = self.model(person_crop, verbose=False)[0]
        for box in results.boxes:
            cls_name = self.model.names[int(box.cls[0])]
            conf = float(box.conf[0])
            if cls_name not in TOOL_CLASSES or conf < self.conf_threshold:
                continue
            bx1, by1, bx2, by2 = map(int, box.xyxy[0])
            center = ((bx1 + bx2) / 2, (by1 + by2) / 2)
            for wx, wy in wrists:
                if np.hypot(center[0] - wx, center[1] - wy) <= PROXIMITY_PX:
                    return cls_name
        return None
