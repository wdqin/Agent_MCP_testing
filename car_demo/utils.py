import os
import sys
import csv
from datetime import datetime
import json


LOG_FILE = os.path.join(os.path.dirname(__file__), "log.csv")

def write_log(func: str, input_text: str, comment: str):
    """Append a new log entry to log.csv."""
    # Create file with header if it doesn't exist
    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "func", "input", "comment"])
        
        timestamp = datetime.now().isoformat()
        writer.writerow([timestamp, func, input_text, comment])

def load_json_file(filepath):
    """Load JSON file if it exists, else return None."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def interpret_time_string(time_str):
    """Convert 'YY:MM:DD:HH:MM' to 'Year YYYY, Month MM, Day DD, Time HH:MM'."""
    try:
        year, month, day, hour, minute = time_str.split(":")
        year = int(year)
        # Assume 2000-based year (e.g., 25 -> 2025)
        full_year = 2000 + year if year < 100 else year
        return f"Year {full_year}, Month {month}, Day {day}, Time {hour}:{minute}"
    except ValueError:
        raise ValueError(f"Invalid time string format: {time_str}")

def interpret_preference_time_string(time_str):
    """Convert 'HH:MM' to 'Time HH:MM'."""
    try:
        hour, minute = time_str.split(":")
        # Assume 2000-based year (e.g., 25 -> 2025)
        return f"Time {hour}:{minute}"
    except ValueError:
        raise ValueError(f"Invalid time string format: {time_str}")
    