import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "thamilprakasam2005@gmail.com"
APP_PASSWORD = "safo uksx dqbu njdh"

RECEIVER_EMAIL = "swathi@gmail.com"

try:

    with open(
        "reports/rca_report.txt",
        "r",
        encoding="utf-8"
    ) as f:

        report = f.read()

except Exception as e:

    print("Failed to read report:", e)
    exit()

msg = MIMEText(report)

msg["Subject"] = "CI/CD Pipeline Failure Alert"
msg["From"] = SENDER_EMAIL
msg["To"] = RECEIVER_EMAIL

try:

    print("Connecting to Gmail SMTP...")

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587,
        timeout=30
    )

    print("Starting TLS...")

    server.starttls()

    print("Logging in...")

    server.login(
        SENDER_EMAIL,
        APP_PASSWORD
    )

    print("Sending Email...")

    server.send_message(msg)

    print("Closing Connection...")

    server.quit()

    print("Email Sent Successfully")

except Exception as e:

    print("\nMail Error:")
    print(type(e).__name__)
    print(str(e))