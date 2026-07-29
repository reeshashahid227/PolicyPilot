import json
import os
import sys
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)
sys.path.insert(0, BASE_DIR)
from src.embeddings.embedder import Embedder
from src.embeddings.vector_store import VectorStore


class Retriever:
    """
    Retrieves the most relevant policy chunks
    using semantic similarity search.
    """

    def __init__(
        self,
        index_path,
        chunks_path,
        model_name="all-MiniLM-L6-v2"
    ):

        self.index_path = index_path
        self.chunks_path = chunks_path

        # Load embedding model
        self.embedder = Embedder(
            model_name=model_name
        )

        # Load FAISS index
        self.vector_store = VectorStore.load(
            index_path
        )

        # Load original chunks
        with open(
            chunks_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.chunks = json.load(file)

    def retrieve(
        self,
        query,
        top_k=5
    ):
        """
        Retrieve the most relevant chunks
        for a user query.
        """

        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        # Generate query embedding
        query_embedding = (
            self.embedder.generate_embeddings(
                [query]
            )
        )

        # Search FAISS
        scores, indices = (
            self.vector_store.search(
                query_embedding,
                top_k=top_k
            )
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            # FAISS may return -1 when
            # fewer results are available
            if index < 0:
                continue

            # Protect against invalid index
            if index >= len(self.chunks):
                continue

            chunk = self.chunks[index]

            results.append(
                {
                    "rank": len(results) + 1,
                    "score": float(score),
                    "text": chunk.get(
                        "text",
                        ""
                    ),
                    "metadata": chunk.get(
                        "metadata",
                        {}
                    )
                }
            )

        return results