import os
import sys

# ============================================================
# Project Root
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ============================================================
# FastAPI
# ============================================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.api.schemas import QuestionRequest, QuestionResponse
from src.core.policy_engine import PolicyEngine


# ============================================================
# App
# ============================================================

app = FastAPI(
    title="PolicyPilot API",
    description=(
        "AI-powered policy assistant "
        "using Retrieval-Augmented Generation"
    ),
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Policy Engine
# ============================================================

engine = PolicyEngine()


# ============================================================
# Root
# ============================================================

@app.get("/")
def root():
    return {
        "message": "PolicyPilot API is running"
    }


# ============================================================
# Health
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# Ask
# ============================================================

@app.post(
    "/ask",
    response_model=QuestionResponse
)
def ask_question(
    request: QuestionRequest
):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        result = engine.ask(question)

        return result

    except Exception as e:

        print(
            f"ERROR IN /ask: "
            f"{type(e).__name__}: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to process question: "
                f"{type(e).__name__}: {e}"
            )
        )