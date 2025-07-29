from goldenverba.components.embedding.SentenceTransformersEmbedder import (
    SentenceTransformersEmbedder,
)


class MiniLMEmbedder(SentenceTransformersEmbedder):
    """
    MiniLMEmbedder for Verba.
    """

    def __init__(self):
        super().__init__(vectorizer="all-MiniLM-L6-v2")
