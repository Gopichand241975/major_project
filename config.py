"""Central configuration for the smart home security system."""

# --- Camera sources ---
CAMERA_1_SOURCE = 0 # Outside, door-facing

# --- Zone around the door lock (x1, y1, x2, y2) — calibrate later ---
DOOR_LOCK_ZONE = (400, 300, 700, 850)

# --- Behaviour thresholds ---
DWELL_TIME_ALERT_SECONDS = 8
SUSPICION_SCORE_THRESHOLD = 71