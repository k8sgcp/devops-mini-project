from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 1. Mock user database
users = [
    {
        "name": "Alice",
        "email": "alice@example.com",
        "subscription_end": "2026-09-07",  # Expires in exactly 7 days (assuming today is Aug 31)
    },
    {
        "name": "Bob",
        "email": "bob@example.com",
        "subscription_end": "2026-09-15",  # Expires in 15 days
    },
]


def send_renewal_email(user_email, user_name, expiry_date):
    # SMTP configuration (Replace with your SMTP server details)
    smtp_server = "smtp.example.com"
    smtp_port = 587
    sender_email = "no-reply@yourcompany.com"
    sender_password = "your_email_password"

    # Draft the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = user_email
    msg["Subject"] = "Action Required: Your subscription expires in 7 days!"

    body = f"""Hi {user_name},

Your monthly subscription will expire on {expiry_date}. 

Since this service requires manual renewal, please log in to your account and renew your plan to ensure uninterrupted access.

Best regards,
Your Support Team
"""
    msg.attach(MIMEText(body, "plain"))

    # Send via SMTP
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Alert successfully sent to {user_email}")
    except Exception as e:
        print(f"Failed to send email to {user_email}: {e}")


def check_expirations_and_alert():
    today = datetime.now().date()
    target_notice_date = today + timedelta(days=7)

    for user in users:
        # Convert string date to a datetime.date object
        expiry_date = datetime.strptime(
            user["subscription_end"], "%Y-%m-%d"
        ).date()

        # Check if expiration date is exactly 7 days away
        if expiry_date == target_notice_date:
            send_renewal_email(
                user["email"], user["name"], user["subscription_end"]
            )


if __name__ == "__main__":
    check_expirations_and_alert()
