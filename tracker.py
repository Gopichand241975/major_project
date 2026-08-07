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