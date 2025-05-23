# utils/config.py

import os

# === Folder and File Paths ===
WATCHED_FOLDER = r"C:\Users\solan\Desktop\test folder"
LOG_FILE = r"G:\Insider Detect\logs\activity_log.json"
DAILY_REPORT_CSV = r"G:\Insider Detect\reports\daily_report.csv"


# === Monitoring Intervals ===
FILE_MONITOR_INTERVAL = 1  # seconds
USB_POLL_INTERVAL = 5      # seconds

# === Notification Settings ===
NOTIFICATION_TIMEOUT = 5  # seconds

# === Sound Alert Settings ===
USB_CONNECTED_BEEP = (1000, 300)     # frequency, duration
USB_DISCONNECTED_BEEP = (600, 300)   # frequency, duration

#for email alerts
# Email configuration
EMAIL_SETTINGS = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "tpmine236@gmail.com",
    "password": "hbcefdejjtruknle",
    "recipient_email": "tpmine236@gmail.com"
}

# Risk score threshold to trigger email alert
RISK_THRESHOLD = 70