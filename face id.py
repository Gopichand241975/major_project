"""Face recognition against a database of known family members.
Known people never trigger an alert; unknown alone is not decisive —
that's handled later in scoring_engine.py.
"""
import os
import pickle
import face_recognition


class FaceIdentifier:
    def __init__(self, db_path="data/faces/", tolerance=0.5):
        self.db_path = db_path
        self.tolerance = tolerance
        self.known_encodings = []
        self.known_names = []
        self._load_known_faces()

    def _load_known_faces(self):
        index_file = os.path.join(self.db_path, "index.pkl")
        if os.path.exists(index_file):
            with open(index_file, "rb") as f:
                data = pickle.load(f)
                self.known_encodings = data["encodings"]
                self.known_names = data["names"]

    def register_face(self, name, image_path):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            raise ValueError(f"No face found in {image_path}")
        self.known_encodings.append(encodings[0])
        self.known_names.append(name)
        os.makedirs(self.db_path, exist_ok=True)
        with open(os.path.join(self.db_path, "index.pkl"), "wb") as f:
            pickle.dump({"encodings": self.known_encodings, "names": self.known_names}, f)

    def identify(self, frame, bbox):
        x1, y1, x2, y2 = bbox
        face_crop = frame[max(0, y1):y2, max(0, x1):x2]
        encodings = face_recognition.face_encodings(face_crop)
        if not encodings:
            return None
        matches = face_recognition.compare_faces(
            self.known_encodings, encodings[0], tolerance=self.tolerance)
        if True in matches:
            return self.known_names[matches.index(True)]
        return None