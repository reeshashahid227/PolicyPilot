import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, BASE_DIR)

from src.retrieval.retriever import Retriever
from src.generation.citations import format_citations


INDEX_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "policy.index"
)

CHUNKS_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "chunks.json"
)


def main():

    retriever = Retriever(
        INDEX_PATH,
        CHUNKS_PATH
    )

    query = "What benefits are available to employees?"

    results = retriever.retrieve(
        query,
        top_k=5
    )

    citations = format_citations(results)

    print("\nRetrieved Sources:\n")

    for citation in citations:

        print(f"Source: {citation['source']}")

        if citation["section"]:
            print(f"Section: {citation['section']}")

        print()


if __name__ == "__main__":
    main()