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