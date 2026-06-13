import os
import logging
import anthropic

logger = logging.getLogger(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are a trend analyst. For each trending topic — football OR politics — output ONLY this format:

📊 [Trend Title]
Status: [1 sentence — what's happening right now]
Angle: [why this is blowing up / public reaction]
Content: [clip/post/thread opportunity]
Link: [search and find the most relevant article or tweet URL for this trend]

Rules:
- Max 5 lines per trend
- No headers, no essays, no long explanations
- Football trends: focus on match/player/storyline
- Politics trends: focus on the key move and public reaction
- If no clear content angle exists, write "N/A"
- Do not repeat similar trends — deduplicate before outputting"""

def analyze_trend(trend):
    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system=SYSTEM_PROMPT,
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search"
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": f"Trend: {trend.get('title', '')}\nSummary: {trend.get('summary', '')}"
                }
            ]
        )
        
        analysis = ""
        for block in message.content:
            if block.type == "text":
                analysis = block.text
                break
        
        logger.info("Trend analyzed successfully")
        return {"analysis": analysis}
    except Exception as e:
        logger.error(f"Error analyzing trend: {e}")
        return {"analysis": "Analysis unavailable"}
