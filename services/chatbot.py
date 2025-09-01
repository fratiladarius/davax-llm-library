from config import CHROMA_DIR, OPENAI_CHAT_MODEL
from llm_client import get_openai_client
from db.vector_store import get_chromadb_client, get_collection
from services.embedder import Embedder
from services.retriever import Retriever
from utils.formatter import format_candidates
from services.ask_llm import ask_recommend_with_summary
from utils.safety import is_offensive


def main():
    client = get_openai_client()
    embedder = Embedder()
    chroma = get_chromadb_client(CHROMA_DIR)
    collection = get_collection(chroma, "books")
    retriever = Retriever(collection, embedder)

    print("bookbot ready. ask for books.\n")
    while True:
        try:
            query = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not query:
            continue

        flagged = is_offensive(query)
        if flagged:
            print('offensive query')
            break

        hits = retriever.retrieve(query, k=3, max_dist=0.5)
        if not hits:
            print("no candidates found. try a different phrasing.\n")
            continue

        print("\nshortlist (closest first):")
        print(format_candidates(hits), "\n")

        slate = format_candidates(hits)
        content = f"user request: {query}\n\ncandidates:\n{slate}"
        resp = ask_recommend_with_summary(
            client, OPENAI_CHAT_MODEL, content
        )

        print('recommendation:\n')
        print(resp)


if __name__ == "__main__":
    main()
