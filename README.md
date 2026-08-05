# AI-Based Smart Home Intrusion Detection System
A camera-based security system that goes beyond plain CCTV: it detects people,
recognises known family members (by face, and by gait when the face isn't
visible), watches for tool-assisted forced-entry behaviour at the door, checks
for weapons/tools near a person's hand, and only alerts the homeowner when
suspicious *behaviour* is present — not just because a face is unrecognised.

## Key design principle
Being **unknown** is not enough to trigger an alert. A delivery rider,
neighbour, or unfamiliar guest who rings the bell and leaves normally will
NOT be flagged. Only **unknown identity + suspicious behaviour** (long dwell
time at the lock, forced-entry motion, or a tool/weapon near the hand)
crosses the alert threshold.

## Modules

| Module | File | Purpose |
|---|---|---|
| Config | `config.py` | Central settings — zones, thresholds, alert channel |
| Detection | `detection.py` | YOLOv8 person detection (humans only) |
| Tracking | `tracker.py` | DeepSORT tracking with door-zone dwell-time |
| Face Recognition | `face_id.py` | Match faces against known family members |
| Gait Recognition | `gait_id.py` | Fallback identity check via Gait Energy Image |
| Weapon Detection | `weapon_detect.py` | Detect tools/weapons near a person's hand |
| Scoring Engine | `scoring_engine.py` | Weighted suspicion score combining all signals |
| Alerts | `alerts.py` | Telegram notification + camera-tamper detection |
| Entry point | `main.py` | Wires the full pipeline together |