"""Face recognition against a database of known family members.
Known people never trigger an alert; unknown alone is not decisive —
that's handled later in scoring_engine.py.
"""
import os
import pickle
import face_recognition

