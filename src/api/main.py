import os
import sys

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

sys.path.insert(0, BASE_DIR)

from fastapi import FastAPI, HTTPException

from src.api.schemas import QuestionRequest, QuestionResponse
from src.retrieval.retriever import Retriever
from src.generation.llm_generator import LLMGenerator
from src.generation.citations import format_citations


app = FastAPI(
    title="PolicyPilot API",
    description="AI-powered policy assistant using Retrieval-Augmented Generation",
    version="1.0.0"
)

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


retriever = Retriever(
    INDEX_PATH,
    CHUNKS_PATH
)


@app.get("/")
def root():
    return {
        "message": "PolicyPilot API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        results = retriever.retrieve(
            question,
            top_k=5
        )

        if not results:
            return {
                "answer": "I could not find relevant information in the available policies.",
                "sources": []
            }

       
        generator = LLMGenerator()

        answer = generator.generate_answer(
        question,
        results)



        citations = format_citations(
            results
        )

        return {
            "answer": answer,
            "sources": citations
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process question: {str(e)}"
        )