from typing import List

import numpy as np

from .base import BaseEmbed


class SentenceEmbed(BaseEmbed):
    """Sentence Transformers embedding provider - local, no API keys needed."""

    def __init__(self, model: str = "all-MiniLM-L6-v2", **kwargs):
        super().__init__(api_key=None, **kwargs)
        self.model = model
        self._model_instance = None
        self._init_model()

    def _init_model(self):
        """Initialize sentence transformer model."""
        try:
            from sentence_transformers import SentenceTransformer
            self._model_instance = SentenceTransformer(self.model)
        except ImportError:
            raise ImportError("sentence-transformers package required. Install with: pip install sentence-transformers")

    def embed_single(self, text: str, **kwargs) -> np.ndarray:
        """Embed a single text string."""
        return self._model_instance.encode(text, **kwargs)

    def embed_batch(self, texts: List[str], **kwargs) -> List[np.ndarray]:
        """Embed multiple texts."""
        embeddings = self._model_instance.encode(texts, **kwargs)
        return [np.array(emb) for emb in embeddings]

    @property
    def dimensionality(self) -> int:
        """Get embedding dimensionality."""
        if "MiniLM-L6" in self.model:
            return 384
        elif "MiniLM-L12" in self.model:
            return 384
        elif "all-mpnet-base" in self.model:
            return 768
        else:
            return 384  # Default for MiniLM