from textwrap import shorten
from utils.id_utils import make_book_id


def format_candidates(cands):
    lines = []
    for i, (m, d) in enumerate(cands, 1):
        short = m.get("short_summary", "")
        lines.append(
            " ".join([
                f"{i}. title: {m['title']}",
                f"| themes: {m.get('themes', '')}",
                f"| short: {shorten(short, 220, placeholder='...')}",
                f"| cosine_distance: {d:.4f}",
                f"| similarity: {1.0 - d:.4f}"
            ])
        )
    return "\n".join(lines)


def meta_to_book(meta):
    return {
        "title": meta.get("title", ""),
        "themes": meta.get("themes", []),
        "short_summary": meta.get("short_summary", ""),
        "long_summary": meta.get("long_summary", "")
    }


def canonical_metadata(book):
    themes = book.get("themes", [])
    return {
        "id": make_book_id(
            book.get("title", ""), book.get("short_summary", "")
        ),
        "title": book.get("title", ""),
        "themes": ", ".join(themes),
        "themes_csv": ", ".join(themes),
        "short_summary": book.get("short_summary", ""),
        "long_summary": book.get("long_summary", "")
    }


def print_ranked_results(results, top_k):
    print(format_candidates(results[:top_k] if top_k else results))
