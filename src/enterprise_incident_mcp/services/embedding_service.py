from sentence_transformers import SentenceTransformer


class EmbeddingService:
    _model: SentenceTransformer | None = None

    @classmethod
    def _get_model(cls) -> SentenceTransformer:
        if cls._model is None:
            cls._model = SentenceTransformer("all-MiniLM-L6-v2")
        return cls._model

    def embed(self, text: str) -> list[float]:
        model = self._get_model()

        return model.encode(
            text,
            normalize_embeddings=True,
        ).tolist()