"""Alert dispatch (Telegram) and camera-tamper detection."""
import time
import cv2
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TAMPER_BLACKOUT_THRESHOLD = 15   # mean pixel intensity below this = likely covered/blocked
TAMPER_DURATION_SECONDS = 3      # must persist this long to avoid false alarms

