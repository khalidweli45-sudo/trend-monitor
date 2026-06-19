import imaplib
import email
import time
import os
from twilio.rest import Client

# ─────────────────────────────────────────
# YOUR SETTINGS — replace these values
# ─────────────────────────────────────────
GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS", "YOUR_GMAIL_HERE")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "YOUR_16_LETTER_APP_PASSWORD_HERE")

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "YOUR_TWILIO_SID_HERE")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "YOUR_TWILIO_AUTH_TOKEN_HERE")
TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER", "YOUR_TWILIO_PHONE_NUMBER_HERE")
YOUR_REAL_NUMBER = os.environ.get("YOUR_REAL_NUMBER", "YOUR_REAL_PHONE_NUMBER_HERE")

# How often to check (in seconds) — 1800 = 30 minutes
CHECK_INTERVAL = 1800

# ─────────────────────────────────────────
# DO NOT EDIT BELOW THIS LINE
# ─────────────────────────────────────────

def check_gmail_for_fiverr():
    try:
        print("Checking Gmail for Fiverr messages...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        mail.select("inbox")

        # Search for unread emails from Fiverr
        status, messages = mail.search(None, '(UNSEEN FROM "fiverr.com")')

        if status != "OK":
            print("No new Fiverr emails found.")
            mail.logout()
            return

        email_ids = messages[0].split()

        if not email_ids:
            print("No new Fiverr emails.")
            mail.logout()
            return

        print(f"Found {len(email_ids)} new Fiverr email(s)!")

        for email_id in email_ids:
            # Fetch email subject
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject = msg["subject"] or "New Fiverr Notification"

            # Send SMS alert
            send_sms_alert(subject)

            # Mark email as read so we don't alert twice
            mail.store(email_id, "+FLAGS", "\\Seen")

        mail.logout()

    except Exception as e:
        print(f"Error checking Gmail: {e}")


def send_sms_alert(subject):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"📬 FIVERR ALERT: You have a new message!\n\nSubject: {subject}\n\nGo respond now → fiverr.com/inbox",
            from_=TWILIO_FROM_NUMBER,
            to=YOUR_REAL_NUMBER
        )
        print(f"SMS sent! Message SID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")


def run():
    print("✅ Fiverr Inbox Alert Agent is running...")
    print(f"Checking every {CHECK_INTERVAL // 60} minutes.\n")
    while True:
        check_gmail_for_fiverr()
        print(f"Sleeping for {CHECK_INTERVAL // 60} minutes...\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    run()
