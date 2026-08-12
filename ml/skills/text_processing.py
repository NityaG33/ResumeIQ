import re
from ml.utilities.skill_aliases import build_alias_lookup

SKILL_SYNONYMS = build_alias_lookup()


def normalize_text(text: str) -> str:
    text = text.lower()

    for alias, canonical_skill in SKILL_SYNONYMS.items():
        pattern = r"\b" + re.escape(alias) + r"\b"
        text = re.sub(pattern, canonical_skill, text)

    return text


def clean_and_normalize(text: str) -> str:
    return normalize_text(text)
