import os
import logging
import requests
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

XAI_API_KEY = os.getenv("XAI_API_KEY")

def get_trends():
    try:
        headers = {
            "Authorization": f"Bearer {XAI_API_KEY}",
            "Content-Type": "application/json"
        }
        since = (datetime.utcnow() - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
        payload = {
            "model": "grok-3",
            "messages": [
                {
                    "role": "user",
                    "content": f"What are the top 5 trending topics on X/Twitter right now covering football and politics since {since}? Return as JSON array with fields: title, summary, category, engagement_score (1-10)"
                }
            ],
            "stream": False
        }
        response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        import json
        trends = json.loads(content)
        logger.info(f"Fetched {len(trends)} trends")
        return trends
    except Exception as e:
        logger.error(f"Error fetching trends: {e}")
        return []
