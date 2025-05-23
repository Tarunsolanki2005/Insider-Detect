import threading
import time
import sys
import os

# Add necessary folders to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "monitor")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "utils")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "alerts")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "reports")))  # Added reports folder

from file_activity import start_file_monitor
from usb_monitor import main as start_usb_monitor
from utils.risk_score import calculate_risk_score
from alerts.email_alert import send_email_alert
from daily_report import generate_daily_report   # Now this import will work

RISK_CHECK_INTERVAL = 60  # seconds between risk checks
RISK_THRESHOLD = 70       # risk score threshold for email alert

def run_usb_monitor():
    print("Starting USB Monitor...")
    start_usb_monitor()

def risk_monitor():
    while True:
        risk = calculate_risk_score()
        print(f"Risk score in the last 24 hours: {risk}")
        if risk >= RISK_THRESHOLD:
            send_email_alert(
                subject=f"Risk Alert: Score {risk}",
                message=f"Alert! Risk score has reached {risk}. Immediate attention needed."
            )
        time.sleep(RISK_CHECK_INTERVAL)

if __name__ == "__main__":
    # Start file monitor (non-blocking)
    observer = start_file_monitor()

    # Start USB monitor thread (daemon)
    usb_thread = threading.Thread(target=run_usb_monitor, daemon=True)
    usb_thread.start()

    # Start risk score monitoring thread (daemon)
    risk_thread = threading.Thread(target=risk_monitor, daemon=True)
    risk_thread.start()

    print("All monitors and risk checks started. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)  # Keep main thread alive
    except KeyboardInterrupt:
        print("\nStopping monitors...")

        # Stop the file observer
        observer.stop()
        observer.join()

        # Generate daily report automatically on exit
        print("Generating daily report before exit...")
        generate_daily_report()

        print("Monitors stopped. Goodbye!")
