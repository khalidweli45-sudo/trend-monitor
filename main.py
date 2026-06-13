import time
import logging
from grok_client import get_trends
from analyzer import analyze_trend
from slack_client import send_message
from memory import is_new_trend, save_trend
from config import LOOP_INTERVAL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("Trend monitor started")
    while True:
        try:
            trends = get_trends()
            for trend in trends:
                if is_new_trend(trend):
                    analysis = analyze_trend(trend)
                    message = f"📊 Trend: {trend.get('title', '')}\n\nAnalysis: {analysis.get('analysis', '')}"
                    send_message(message)
                    save_trend(trend)
            logger.info("Cycle complete. Sleeping...")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        time.sleep(LOOP_INTERVAL)

if __name__ == "__main__":
    main()
