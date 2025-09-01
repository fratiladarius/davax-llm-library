class Retriever:
    def __init__(self, collection, embedder):
        self.collection = collection
        self.embedder = embedder

    def retrieve(self, query, k=3, max_dist=None, dedupe=True):
        qvec = self.embedder.embed(query)[0]

        res = self.collection.query(
            query_embeddings=[qvec],
            n_results=k,
            include=["metadatas", "distances"]
        )

        metas = res.get("metadatas", [[]])[0]
        dists = res.get("distances", [[]])[0]

        ranked = sorted(zip(metas, dists), key=lambda x: x[1])

        if dedupe:
            seen = set()
            deduped = []
            for m, d in ranked:
                key = (m.get("id") or m.get("title", "").lower())
                if key in seen:
                    continue
                seen.add(key)
                deduped.append((m, d))
            ranked = deduped

        if max_dist is None:
            return ranked

        filtered = [(m, d) for (m, d) in ranked if d <= float(max_dist)]
        return filtered or ranked
