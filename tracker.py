"""
tracker.py

Post-entry version. The door-lock zone / dwell-time-at-lock logic is gone
(there's no door zone indoors). Instead, each track now gets a lightweight
`unusual_movement` flag based on erratic path behaviour — sudden direction
reversals and/or lingering in place for too long. This is intentionally
simple; swap in a proper activity-recognition model later if you want it
more robust (see the BlazePose / activity-recognition references in the
research papers PDF).
"""


import time
from collections import deque

import numpy as np
from deep_sort_realtime.deepsort_tracker import DeepSort


HISTORY_LEN = 15
LINGER_SECONDS = 10
DIRECTION_REVERSAL_THRESHOLD = 3  # reversals within HISTORY_LEN to flag


def _center(bbox):
    x1, y1, x2, y2 = bbox
    return ((x1 + x2) / 2, (y1 + y2) / 2)

class PersonTracker:
    def __init__(self):
        self.tracker = DeepSort(max_age=30)
        self.position_history = {}   # track_id -> deque of (x, y)
        self.first_seen = {}         # track_id -> timestamp
        self.last_center = {}        # track_id -> (x, y)

    def update(self, detections, frame):
        ds_input = [
            (
                [d["bbox"][0], d["bbox"][1],
                 d["bbox"][2] - d["bbox"][0], d["bbox"][3] - d["bbox"][1]],
                d["conf"], "person",
            )
            for d in detections
        ]
        tracks = self.tracker.update_tracks(ds_input, frame=frame)
        now = time.time()
        results = []

        for t in tracks:
            if not t.is_confirmed():
                continue
            track_id = t.track_id
            bbox = tuple(map(int, t.to_ltrb()))
            center = _center(bbox)

            self.first_seen.setdefault(track_id, now)
            hist = self.position_history.setdefault(track_id, deque(maxlen=HISTORY_LEN))
            hist.append(center)

            unusual_movement = self._is_unusual(track_id, hist, now)

            results.append({
                "track_id": track_id,
                "bbox": bbox,
                "time_in_frame": now - self.first_seen[track_id],
                "unusual_movement": unusual_movement,
            })

        return results

    def _is_unusual(self, track_id, hist, now):
        # Flag 1: lingering in roughly the same spot too long.
        lingering = (now - self.first_seen[track_id]) >= LINGER_SECONDS and self._low_variance(hist)

        # Flag 2: repeated direction reversals (pacing / erratic movement).
        reversals = self._count_reversals(hist)

        return bool(lingering or reversals >= DIRECTION_REVERSAL_THRESHOLD)

    @staticmethod
    def _low_variance(hist, spread_px=40):
        if len(hist) < 5:
            return False
        pts = np.array(hist)
        spread = pts.max(axis=0) - pts.min(axis=0)
        return bool((spread < spread_px).all())

    @staticmethod
    def _count_reversals(hist):
        if len(hist) < 4:
            return 0
        pts = np.array(hist)
        deltas = np.diff(pts, axis=0)
        reversals = 0
        for i in range(1, len(deltas)):
            dot = np.dot(deltas[i - 1], deltas[i])
            if dot < 0:
                reversals += 1
        return reversals
