"""Entry point: wires detection -> tracking -> identity -> weapon check ->
scoring -> alerts into a single real-time loop for Camera 1 (door-facing).
"""
import argparse
import time
import cv2


from detection import PersonDetector
from tracker import PersonTracker
from face_id import FaceIdentifier
from weapon_detect import WeaponDetector
from scoring_engine import compute_suspicion_score
from alerts import send_alert, TamperMonitor