import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from email_alert import send_email_alert


if __name__ == "__main__":
    subject = "Test Email Alert"
    message = "This is a test message to check if the email alert works."
    send_email_alert(subject, message)
