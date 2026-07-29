import os
import sys
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from src.retrieval.retriever import Retriever
from src.generation.llm_generator import LLMGenerator


# --------------------------------------------------
# Project root
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# --------------------------------------------------
# Processed data
# --------------------------------------------------

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

    print("=" * 60)
    print("PolicyPilot - Phase 5")
    print("RAG Answer Generation")
    print("=" * 60)

    # Check files
    if not os.path.exists(INDEX_FILE):
        raise FileNotFoundError(
            f"FAISS index not found:\n{INDEX_FILE}"
        )

    if not os.path.exists(CHUNKS_FILE):
        raise FileNotFoundError(
            f"Chunks file not found:\n{CHUNKS_FILE}"
        )

    # Load retriever
    print("\nLoading Retriever...")

    retriever = Retriever(
        index_path=INDEX_FILE,
        chunks_path=CHUNKS_FILE
    )

    # Load LLM
    print("Loading LLM...")

    generator = LLMGenerator()

    # Question
    question = input(
        "\nAsk a policy question: "
    ).strip()

    if not question:
        print("Question cannot be empty.")
        return

    # Retrieval
    print(
        "\nSearching policy documents..."
    )

    retrieved_chunks = retriever.retrieve(
        query=question,
        top_k=5
    )

    print(
        f"Retrieved chunks: "
        f"{len(retrieved_chunks)}"
    )

    # Generation
    print(
        "\nGenerating answer..."
    )

    answer = generator.generate_answer(
        question=question,
        retrieved_chunks=retrieved_chunks
    )

    # Answer
    print("\n" + "=" * 60)
    print("POLICYPILOT ANSWER")
    print("=" * 60)

    print(answer)

    # Sources
    print("\n" + "=" * 60)
    print("RETRIEVED SOURCES")
    print("=" * 60)

    if not retrieved_chunks:

        print("No relevant sources found.")

    else:

        for chunk in retrieved_chunks:

            metadata = chunk.get(
                "metadata",
                {}
            )

            source = metadata.get(
                "source",
                "Unknown source"
            )

            print(
                f"\nRank: {chunk['rank']}"
            )

            print(
                f"Score: "
                f"{chunk['score']:.4f}"
            )

            print(
                f"Source: {source}"
            )


if __name__ == "__main__":
    main()