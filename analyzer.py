import os
import logging
import anthropic

logger = logging.getLogger(__name__)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyze_trend(trend):
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this trending topic briefly. What's happening and why does it matter?\n\nTrend: {trend.get('title', '')}\nSummary: {trend.get('summary', '')}"
                }
            ]
        )
        analysis = message.content[0].text
        logger.info("Trend analyzed successfully")
        return {"analysis": analysis}
    except Exception as e:
        logger.error(f"Error analyzing trend: {e}")
        return {"analysis": "Analysis unavailable"}
