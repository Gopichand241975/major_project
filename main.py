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


def run(camera_source):
    cap = cv2.VideoCapture(camera_source)
    detector = PersonDetector()
    tracker = PersonTracker()
    face_id = FaceIdentifier()
    weapon_detector = WeaponDetector()
    tamper_monitor = TamperMonitor()

    alerted_tracks = set()  # avoid spamming repeat alerts for the same track

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        tamper_monitor.check(frame, camera_name="Camera 1 (Door)")

        detections = detector.detect(frame)
        tracks = tracker.update(detections, frame)

        for t in tracks:
            name = face_id.identify(frame, t["bbox"])
            weapon = weapon_detector.detect_in_hand(frame, t["bbox"])
            forced_entry_motion = t["dwell_time"] >= 5  # placeholder for motion-pattern check

            result = compute_suspicion_score(
                identity_name=name,
                dwell_time=t["dwell_time"],
                forced_entry_motion=forced_entry_motion,
                weapon_detected=bool(weapon),
            )

            if result["triggered"] and t["track_id"] not in alerted_tracks:
                snapshot_path = f"snapshot_{t['track_id']}_{int(time.time())}.jpg"
                cv2.imwrite(snapshot_path, frame)
                reasons = ", ".join(result["reasons"])
                send_alert(
                    f"Possible break-in attempt detected. Identity: {result['identity']}. "
                    f"Score: {result['score']}. Reasons: {reasons}.",
                    snapshot_path,
                )
                alerted_tracks.add(t["track_id"])

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--camera", type=int, default=0, help="Camera index or path")
    args = parser.parse_args()
    run(args.camera)