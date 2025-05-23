# alert/email_alert.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.config import EMAIL_SETTINGS

def send_email_alert(subject, message):
    """
    Send an email alert with the given subject and message.
    """
    try:
        smtp_server = EMAIL_SETTINGS["smtp_server"]
        smtp_port = EMAIL_SETTINGS["smtp_port"]
        sender_email = EMAIL_SETTINGS["sender_email"]
        password = EMAIL_SETTINGS["password"]
        recipient_email = EMAIL_SETTINGS["recipient_email"]

        # Create message container
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the message body
        msg.attach(MIMEText(message, 'plain'))

        # Connect to server and send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        print("Email alert sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")
