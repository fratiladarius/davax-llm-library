import json
from pathlib import Path


def load_summaries(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"cannot find summaries file at: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("expected a list of books, got something else.")
    return data


def find_by_title(title, summaries_list):
    needle = title.strip().lower()
    for book in summaries_list:
        if book["title"].strip().lower() == needle:
            return book
    return None


def embed_documents(books):
    docs = []
    for book in books:
        doc = f"{book['title']} | {', '.join(book['themes'])} | {
            book['short_summary']}"
        docs.append(doc)
    return docs
