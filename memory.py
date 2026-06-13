import os
import json
import logging

logger = logging.getLogger(__name__)

MEMORY_FILE = "seen_trends.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_trend(trend):
    memory = load_memory()
    memory.append(trend.get("title", ""))
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

def is_new_trend(trend):
    memory = load_memory()
    return trend.get("title", "") not in memory
