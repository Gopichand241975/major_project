"""Gait recognition fallback for when the face isn't usable (dark, masked,
side-on). Uses a Gait Energy Image (GEI) matched against registered profiles.
"""
import os
import numpy as np

def compute_gei(silhouette_frames):
    stack = np.stack(silhouette_frames, axis=0).astype(np.float32)
    return np.mean(stack, axis=0)