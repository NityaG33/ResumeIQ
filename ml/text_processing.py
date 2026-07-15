import re
from ml.utilities.skill_normalizer import SKILL_SYNONYMS

def normalize_text(text: str) -> str:
    text = text.lower()

    for short, full in SKILL_SYNONYMS.items():
        pattern = r"\b" + re.escape(short) + r"\b"
        text = re.sub(pattern, full, text)

    return text


def clean_and_normalize(text: str) -> str:
    return normalize_text(text)
