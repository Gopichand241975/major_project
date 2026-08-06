"""Central configuration for the post-entry intrusion detection system.

Focus: an indoor camera detects a person AFTER they have entered the house.
It tries face recognition first; if the face isn't usable (angle, motion,
or darkness), it falls back to gait recognition. In low light, IR footage
is used instead of normal color footage for both checks.
"""