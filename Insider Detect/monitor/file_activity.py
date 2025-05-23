from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import json
from datetime import datetime
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# file_activity.py
from utils.config import WATCHED_FOLDER, LOG_FILE, FILE_MONITOR_INTERVAL


class FileActivityHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            log_event("created", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            log_event("modified", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            log_event("deleted", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            log_event("moved", f"{event.src_path} -> {event.dest_path}")

def log_event(event_type, file_path):
    event = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event": event_type,
        "file": file_path
    }

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

    data = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    data.append(event)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def start_file_monitor():
    event_handler = FileActivityHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCHED_FOLDER, recursive=True)
    observer.start()
    print(f"Monitoring started on: {WATCHED_FOLDER}")
    return observer

    try:
        while True:
            time.sleep(FILE_MONITOR_INTERVAL)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_file_monitor()
