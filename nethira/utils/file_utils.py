# utils/file_utils.py
import os
from datetime import datetime

def ensure_logs_dir():
    if not os.path.exists("logs"):
        os.makedirs("logs")

def get_timestamped_log_path(prefix: str = "session") -> str:
    ensure_logs_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join("logs", f"{prefix}_{timestamp}.log")

def save_text_to_file(filepath: str, text: str):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
