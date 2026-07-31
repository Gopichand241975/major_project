"""Weighted suspicion-scoring engine.

Core decision logic: being *unknown* alone is not enough to trigger an
alert — only unknown identity COMBINED WITH suspicious behaviour (long
dwell time, forced-entry motion, or a weapon/tool in hand) crosses the
threshold. This is what keeps family, neighbours, and delivery riders
from triggering false alerts.
"""

from config import DWELL_TIME_ALERT_SECONDS, SUSPICION_SCORE_THRESHOLD

WEIGHTS = {
    "unknown_identity": 25,
    "long_dwell_time": 20,
    "forced_entry_motion": 25,
    "weapon_or_tool_detected": 30,
}