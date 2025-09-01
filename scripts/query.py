import sys
from db.vector_store import get_chromadb_client, get_collection
from services.embedder import Embedder
from utils.formatter import print_ranked_results
from config import CHROMA_DIR


def search(query: str, k: int = 3):
    embedder = Embedder()
    qvec = embedder.embed(query)[0]

    chroma = get_chromadb_client(CHROMA_DIR)
    col = get_collection(chroma, "books")

    res = col.query(query_embeddings=[qvec], n_results=k)
    metas = res["metadatas"][0]
    scores = res["distances"][0]

    ranked = sorted(zip(metas, scores), key=lambda x: x[1])
    print_ranked_results(ranked, top_k=k)


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or "state rewrites reality"
    search(q)
