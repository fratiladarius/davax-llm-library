from config import BOOKS_JSON
from utils.loader import load_summaries, find_by_title


def get_summary_by_title(title):
    books = load_summaries(BOOKS_JSON)
    b = find_by_title(title, books)
    if not b:
        return ""
    return b.get("long_summary") or b.get("short_summary") or ""


GET_SUMMARY_TOOL = {
    "type": "function",
    "function": {
        "name": "get_summary_by_title",
        "description": "return the full summary for an exact book title.",
        "parameters": {
            "type": "object",
            "properties": {"title": {"type": "string"}},
            "required": ["title"]
        }
    }
}
