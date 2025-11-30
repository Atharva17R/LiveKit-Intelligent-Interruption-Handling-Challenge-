# utils_text.py
import re

def normalize_text(raw: str) -> str:
    if raw is None:
        return ""
    s = raw.lower()
    # keep letters, numbers, spaces, apostrophes and hyphens
    s = re.sub(r"[^\w\s'\-]+", " ", s, flags=re.UNICODE)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def tokenize(text: str):
    norm = normalize_text(text)
    if not norm:
        return []
    return [t for t in norm.split(" ") if t]
