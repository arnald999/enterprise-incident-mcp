import os
from typing import Any


class EmbeddingService:
    _model: Any = None

    @classmethod
    def _get_model(cls):
        if os.getenv("DISABLE_EMBEDDINGS", "false").lower() == "true":
            raise RuntimeError("Embeddings disabled in this deployment")

        if cls._model is None:
            from sentence_transformers import SentenceTransformer

            cls._model = SentenceTransformer("all-MiniLM-L6-v2")

        return cls._model

    def embed(self, text: str) -> list[float]:
        model = self._get_model()
        return model.encode(text, normalize_embeddings=True).tolist()