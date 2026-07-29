"""Gait recognition fallback for when the face isn't usable (dark, masked,
side-on). Uses a Gait Energy Image (GEI) matched against registered profiles.
"""
import os
import numpy as np