import json
import os
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import LOG_FILE

# Risk weights for different event types
RISK_WEIGHTS = {
    "usb_connected": 5,
    "usb_disconnected": 3,
    "created": 4,
    "modified": 2,
    "deleted": 5,
    "moved": 4,
}

def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def calculate_risk_score(time_window_hours=24):
    """
    Calculate risk score based on events in the last `time_window_hours` hours.
    """
    logs = load_logs()
    if not logs:
        return 0

    now = datetime.now()
    cutoff_time = now - timedelta(hours=time_window_hours)

    score = 0
    for event in logs:
        try:
            event_time = datetime.strptime(event["timestamp"], "%Y-%m-%d %H:%M:%S")
        except (KeyError, ValueError):
            continue

        if event_time < cutoff_time:
            continue

        event_type = event.get("event", "").lower()
        score += RISK_WEIGHTS.get(event_type, 0)

    return score

def print_risk_score():
    score = calculate_risk_score()
    print(f"Risk score in the last 24 hours: {score}")

if __name__ == "__main__":
    print_risk_score()
