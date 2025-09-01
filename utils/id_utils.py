import hashlib
import re


def _canon(s):
    s = (s or "").lower().strip()
    return re.sub(r"\s+", " ", s)


def make_book_id(title, summary=None):
    parts = [_canon(title)]
    if summary:
        parts.append(_canon(summary)[:80])
    key = " | ".join(parts)
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]
