"""
ir_check.py

Decides, per frame, whether the pipeline should rely on normal-light face
recognition or fall back to IR-lit footage + gait recognition.

Logic:
    - Compute mean grayscale brightness of the frame.
    - If brightness >= DARKNESS_BRIGHTNESS_THRESHOLD -> "face" mode
      (normal color footage, face recognition is attempted first).
    - If brightness < DARKNESS_BRIGHTNESS_THRESHOLD -> "ir_gait" mode
      (assume the camera has switched to IR illumination; skip straight to
      gait recognition, since face recognition is unreliable under IR/low
      light without a model trained specifically for IR faces).

This module does not control the physical IR cut filter / illuminator on
the camera itself — most indoor security cameras switch to IR automatically
in low light. This module only decides which *software* path to run against
whatever footage is coming in.
"""

