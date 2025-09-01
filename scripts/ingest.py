from config import BOOKS_JSON, CHROMA_DIR
from utils.loader import load_summaries, embed_documents
from db.vector_store import get_chromadb_client, get_collection, store_books
from services.embedder import Embedder


def main():
    books = load_summaries(BOOKS_JSON)
    docs = embed_documents(books)

    embedder = Embedder()
    vectors = embedder.embed(docs)

    chroma = get_chromadb_client(CHROMA_DIR)
    col = get_collection(chroma, "books")

    n = store_books(col, docs, books, vectors)
    print(f"ingested {n}, collection count = {col.count()}")


if __name__ == "__main__":
    main()
