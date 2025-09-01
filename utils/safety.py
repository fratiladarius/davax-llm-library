import re


OFFENSIVE_TERMS = {
    "idiot", "stupid", "retard", "cunt", "asshole"
}


def normalize(text):
    t = (text or "").lower()
    t = re.sub(r"\s+", " ", t).strip()
    return t


def is_offensive(text: str) -> bool:
    words = set(text.lower().split())
    return any(word in words for word in OFFENSIVE_TERMS)
