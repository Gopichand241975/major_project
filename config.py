"""Central configuration for the post-entry intrusion detection system.

Focus: an indoor camera detects a person AFTER they have entered the house.
It tries face recognition first; if the face isn't usable (angle, motion,
or darkness), it falls back to gait recognition. In low light, IR footage
is used instead of normal color footage for both checks.
"""

# --- Camera source (indoor camera only) ---
INDOOR_CAMERA_SOURCE = 0

# --- Lighting detection ---
# Mean pixel brightness (0-255) below this = treat frame as "dark",
# switch to IR-based analysis instead of normal color analysis.
DARKNESS_BRIGHTNESS_THRESHOLD = 40

# --- Suspicious behaviour thresholds ---
UNUSUAL_MOVEMENT_ALERT = True     # e.g. erratic movement / not a normal walking path
SUSPICION_SCORE_THRESHOLD = 60    # 0-100 scale, triggers alert

# --- Scoring weights ---
WEIGHTS = {
    "face_unrecognized": 30,
    "gait_unrecognized": 30,
    "unusual_movement": 40,
}

# --- Alert channel ---
TELEGRAM_BOT_TOKEN = "SET_ME"
TELEGRAM_CHAT_ID = "SET_ME"

# --- Known people database ---
FACE_DB_PATH = "data/faces/"
GAIT_DB_PATH = "data/gait/"