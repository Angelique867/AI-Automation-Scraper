import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email_with_html(subject, html_content, db_path=None):
    sender_email = os.getenv("SENDER_EMAIL")
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")

    if not all([sender_email, recipient_email, password]):
        raise ValueError("Missing required email environment variables.")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    msg.attach(MIMEText(html_content, "html"))

    # Optional: attach database
    if db_path and os.path.exists(db_path):
        with open(db_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(db_path)}")
        msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)
        print("✅ Email sent successfully.")