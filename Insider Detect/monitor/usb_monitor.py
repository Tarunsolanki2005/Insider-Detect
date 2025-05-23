import subprocess
import time
import json
import os
from datetime import datetime
from plyer import notification
import winsound
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# usb_monitor.py
# Inside file_activity.py and usb_monitor.py

from utils.config import LOG_FILE, USB_POLL_INTERVAL, NOTIFICATION_TIMEOUT, USB_CONNECTED_BEEP, USB_DISCONNECTED_BEEP


def log_event(event_type, device):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": timestamp,
        "event": event_type,
        "device": device
    }

    title = "USB Activity Detected"
    message = f"{event_type.replace('_', ' ').title()} - {device} at {timestamp}"
    notification.notify(
        title=title,
        message=message,
        timeout=NOTIFICATION_TIMEOUT
    )

    if event_type == "usb_connected":
        winsound.Beep(*USB_CONNECTED_BEEP)
    elif event_type == "usb_disconnected":
        winsound.Beep(*USB_DISCONNECTED_BEEP)

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    data = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    data.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_connected_usb_devices():
    try:
        output = subprocess.check_output('wmic logicaldisk where drivetype=2 get deviceid', shell=True)
        output = output.decode().strip().split('\n')
        devices = set(line.strip() for line in output[1:] if line.strip())
        return devices
    except subprocess.CalledProcessError as e:
        print("Error running wmic:", e)
        return set()

def main():
    print("Starting USB monitoring")
    prev_devices = get_connected_usb_devices()
    print(f"Currently connected USB devices: {prev_devices}")

    try:
        while True:
            time.sleep(USB_POLL_INTERVAL)
            current_devices = get_connected_usb_devices()

            new_devices = current_devices - prev_devices
            for device in new_devices:
                print(f"USB connected: {device}")
                log_event("usb_connected", device)

            removed_devices = prev_devices - current_devices
            for device in removed_devices:
                print(f"USB disconnected: {device}")
                log_event("usb_disconnected", device)

            prev_devices = current_devices

    except KeyboardInterrupt:
        print("USB monitoring stopped by user")

if __name__ == "__main__":
    main()
