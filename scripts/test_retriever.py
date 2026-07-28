import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

sys.path.insert(0, BASE_DIR)

from src.retrieval.retriever import Retriever

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

INDEX_FILE = os.path.join(
    PROCESSED_DIR,
    "policy.index"
)

CHUNKS_FILE = os.path.join(
    PROCESSED_DIR,
    "chunks.json"
)


def main():

    if not os.path.exists(INDEX_FILE):
        raise FileNotFoundError(
            f"FAISS index not found: {INDEX_FILE}"
        )

    if not os.path.exists(CHUNKS_FILE):
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_FILE}"
        )

    retriever = Retriever(
        index_path=INDEX_FILE,
        chunk_path=CHUNKS_FILE
    )

    query = input(
        "\nEnter your policy question: "
    ).strip()

    results = retriever.retrieve(
        query=query,
        top_k=5
    )

    if not results:
        print("No relevant results found.")
        return

    for result in results:
        print(f"\nRank: {result['rank']}")
        print(f"Similarity Score: {result['score']:.4f}")
        print(f"Text:\n{result['text']}")
        print(f"Metadata:\n{result['metadata']}")
        print("-" * 60)


if __name__ == "__main__":
    main()