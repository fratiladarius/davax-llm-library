from pathlib import Path
from chromadb.config import Settings  # type: ignore
from utils.formatter import canonical_metadata
from typing import Union

import chromadb  # type: ignore


def get_chromadb_client(path: Union[str, Path] = './chroma_db'):
    Path(path).mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=path, settings=Settings(anonymized_telemetry=False)
    )


def get_collection(client, name='books'):
    return client.get_or_create_collection(
        name=name,
        metadata={'hnsw:space': 'cosine'}
    )


def store_books(collection, docs, books, vectors, verbose=False):
    assert len(docs) == len(books) == len(vectors), 'length mismatch'

    metadatas = [canonical_metadata(book) for book in books]
    ids = [m['id'] for m in metadatas]

    existing = set(collection.get()["ids"])
    new_items = [
        (doc, vec, meta, id_)
        for doc, vec, meta, id_ in zip(docs, vectors, metadatas, ids)
        if id_ not in existing
    ]

    if not new_items:
        if verbose:
            print("no new books to add")
        return 0

    docs, vectors, metadatas, ids = map(list, zip(*new_items))

    if verbose:
        for i, id_ in enumerate(ids):
            print(f"[{i}] id={id_}")
            print(f"    metadata={metadatas[i]}")

    collection.add(
        documents=docs, embeddings=vectors, metadatas=metadatas, ids=ids
    )
    return len(ids)
