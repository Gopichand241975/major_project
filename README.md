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