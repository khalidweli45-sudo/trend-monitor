import os
import logging
import requests
import time

logger = logging.getLogger(__name__)

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_message(text):
    if not SLACK_WEBHOOK_URL:
        logger.error("SLACK_WEBHOOK_URL not set")
        return False
    attempt = 1
    while attempt <= 3:
        try:
            response = requests.post(SLACK_WEBHOOK_URL, json={"text": text}, timeout=10)
            response.raise_for_status()
            logger.info(f"Slack message sent ({len(text)} chars)")
            return True
        except requests.HTTPError as exc:
            logger.warning(f"Slack HTTP error attempt {attempt}/3: {exc.response.status_code}")
            attempt += 1
            time.sleep(2 ** attempt)
        except Exception as exc:
            logger.warning(f"Slack send error attempt {attempt}/3: {exc}")
            attempt += 1
            time.sleep(2 ** attempt)
    logger.error("All Slack send attempts failed")
    return False
