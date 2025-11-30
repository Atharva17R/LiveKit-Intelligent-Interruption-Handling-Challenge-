# utils_keywords.py
from .config import DEFAULT_CONFIG

IGNORE_SET = set(DEFAULT_CONFIG["ignore_list"])
INTERRUPT_SET = set(DEFAULT_CONFIG["interrupt_keywords"])
QUESTION_SET = set(DEFAULT_CONFIG["question_words"])

def is_all_filler(tokens):
    if not tokens:
        return False
    return all(t in IGNORE_SET for t in tokens)

def contains_interrupt_keyword(tokens):
    for t in tokens:
        if t in INTERRUPT_SET or t in QUESTION_SET:
            return t
    return None

def contains_meaningful_token(tokens):
    for t in tokens:
        if t not in IGNORE_SET:
            return True
    return False
