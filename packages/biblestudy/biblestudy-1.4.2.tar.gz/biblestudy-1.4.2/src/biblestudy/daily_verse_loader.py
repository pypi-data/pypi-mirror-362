import json
from datetime import datetime
from pathlib import Path

def get_today_verse_reference():
    """
    Returns today's devotional verse reference (e.g., 'John 3:16')
    based on the day of the year.
    """
    path = Path(__file__).parent / "daily_verses.json"
    with open(path, "r") as f:
        verses = json.load(f)

    day_of_year = datetime.now().timetuple().tm_yday  # 1–366
    return verses[day_of_year - 1]
