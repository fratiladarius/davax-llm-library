from config import OPENAI_EMBED_MODEL
from llm_client import get_openai_client


class Embedder:
    def __init__(self, model=OPENAI_EMBED_MODEL):
        self.client = get_openai_client()
        self.model = model

    def embed(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        if not texts:
            return []

        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )

        return [resp.embedding for resp in response.data]
