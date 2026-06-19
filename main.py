
import imaplib
import email
import time
import os
from twilio.rest import Client
 
# ─────────────────────────────────────────
# YOUR SETTINGS — all set via Railway Variables
# ─────────────────────────────────────────
GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
 
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
 
# Twilio WhatsApp sandbox number (don't change this)
TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"
 
# Your WhatsApp number
YOUR_WHATSAPP_NUMBER = os.environ.get("YOUR_WHATSAPP_NUMBER")
 
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
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject = msg["subject"] or "New Fiverr Notification"
 
            send_whatsapp_alert(subject)
 
            mail.store(email_id, "+FLAGS", "\\Seen")
 
        mail.logout()
 
    except Exception as e:
        print(f"Error checking Gmail: {e}")
 
 
def send_whatsapp_alert(subject):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"📬 FIVERR ALERT: You have a new message!\n\nSubject: {subject}\n\nRespond now → fiverr.com/inbox",
            from_=TWILIO_WHATSAPP_FROM,
            to=f"whatsapp:{YOUR_WHATSAPP_NUMBER}"
        )
        print(f"WhatsApp alert sent! SID: {message.sid}")
    except Exception as e:
        print(f"Error sending WhatsApp: {e}")
 
 
def run():
    print("✅ Fiverr Inbox Alert Agent is running...")
    print(f"Checking every {CHECK_INTERVAL // 60} minutes.\n")
    while True:
        check_gmail_for_fiverr()
        print(f"Sleeping for {CHECK_INTERVAL // 60} minutes...\n")
        time.sleep(CHECK_INTERVAL)
 
 
if __name__ == "__main__":
    run()
