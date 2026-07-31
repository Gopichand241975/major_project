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

def compute_suspicion_score(identity_name, dwell_time, forced_entry_motion, weapon_detected):
    """
    identity_name: str name if recognised (face or gait), else None
    dwell_time: seconds spent in the door/lock zone
    forced_entry_motion: bool, True if repetitive lock-tampering motion detected
    weapon_detected: bool, True if a tool/weapon was found near the hand
    """
    score = 0
    reasons = []

    is_unknown = identity_name is None
    if is_unknown:
        score += WEIGHTS["unknown_identity"]
        reasons.append("unrecognised person")

    if dwell_time >= DWELL_TIME_ALERT_SECONDS:
        score += WEIGHTS["long_dwell_time"]
        reasons.append(f"long dwell time ({dwell_time:.1f}s at lock)")

    if forced_entry_motion:
        score += WEIGHTS["forced_entry_motion"]
        reasons.append("repetitive forced-entry motion")

    if weapon_detected:
        score += WEIGHTS["weapon_or_tool_detected"]
        reasons.append("tool/weapon detected near hand")

    triggered = score >= SUSPICION_SCORE_THRESHOLD

    return {
        "score": score,
        "triggered": triggered,
        "reasons": reasons,
        "identity": identity_name if identity_name else "Unknown",
    }

