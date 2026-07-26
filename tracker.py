"""Multi-person tracking with dwell-time in the door/lock zone."""
import time
from deep_sort_realtime.deepsort_tracker import DeepSort
from config import DOOR_LOCK_ZONE

def _in_zone(bbox, zone):
    x1, y1, x2, y2 = bbox
    zx1, zy1, zx2, zy2 = zone
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    return zx1 <= cx <= zx2 and zy1 <= cy <= zy2

class PersonTracker:
    def __init__(self):
        self.tracker = DeepSort(max_age=30)
        self.zone_entry_time = {}

    def update(self, detections, frame):
        ds_input = [([d["bbox"][0], d["bbox"][1],
                      d["bbox"][2] - d["bbox"][0], d["bbox"][3] - d["bbox"][1]],
                     d["conf"], "person") for d in detections]
        tracks = self.tracker.update_tracks(ds_input, frame=frame)