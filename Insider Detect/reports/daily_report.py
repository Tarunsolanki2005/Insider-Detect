import json
import csv
import os
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import LOG_FILE, DAILY_REPORT_CSV


def generate_daily_report():
    # Ensure directory for CSV exists
    os.makedirs(os.path.dirname(DAILY_REPORT_CSV), exist_ok=True)

    # Load JSON log data
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Process events to get counts by event type
    summary = {}
    for event in data:
        etype = event.get("event", "unknown")
        summary[etype] = summary.get(etype, 0) + 1

    # Write summary to CSV
    with open(DAILY_REPORT_CSV, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Event Type", "Count"])
        for event_type, count in summary.items():
            writer.writerow([event_type, count])

    print(f"Daily report generated and saved to {DAILY_REPORT_CSV}")

if __name__ == "__main__":
    generate_daily_report()
