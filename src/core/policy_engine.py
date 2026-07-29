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
from src.generation.llm_generator import LLMGenerator
from src.generation.citations import format_citations


class PolicyEngine:

    def __init__(self):

        # Project root directory
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__)
                )
            )
        )

        # Paths
        index_path = os.path.join(
            base_dir,
            "data",
            "processed",
            "policy.index"
        )

        chunks_path = os.path.join(
            base_dir,
            "data",
            "processed",
            "chunks.json"
        )

        # RAG components
        self.retriever = Retriever(
            index_path,
            chunks_path
        )

        self.generator = LLMGenerator()

    def ask(self, question):

        question = question.strip()

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        # Retrieve relevant policy chunks
        results = self.retriever.retrieve(
            question,
            top_k=5
        )

        # No relevant information
        if not results:
            return {
                "answer": (
                    "I could not find relevant information "
                    "in the available policies."
                ),
                "sources": []
            }

        # Generate answer
        answer = self.generator.generate_answer(
            question,
            results
        )

        # Format sources
        citations = format_citations(
            results
        )

        return {
            "answer": answer,
            "sources": citations
        }