import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class LLMGenerator:
    """
    Generates grounded answers using
    retrieved PolicyPilot context.
    """

    def __init__(
        self,
        model="llama-3.3-70b-versatile"
    ):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not set. "
                "Add it to your .env file."
            )

        self.client = Groq(
            api_key=api_key
        )

        self.model = model

    def generate_answer(
        self,
        question,
        retrieved_chunks
    ):
        """
        Generate an answer using only
        retrieved policy information.
        """

        if not question or not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        if not retrieved_chunks:
            return (
                "I couldn't find relevant information "
                "in the available policy documents."
            )

        # Build policy context
        context_parts = []

        for i, chunk in enumerate(
            retrieved_chunks,
            start=1
        ):
            text = chunk.get("text", "")

            metadata = chunk.get(
                "metadata",
                {}
            )

            source = metadata.get(
                "source",
                "Unknown source"
            )

            context_parts.append(
                f"""
POLICY SOURCE {i}:
{source}

POLICY CONTENT:
{text}
"""
            )

        context = "\n".join(context_parts)

        # System instructions
        system_prompt = """
You are PolicyPilot, an AI assistant that
answers questions about company policies.

Use ONLY the policy context provided by the user.

STRICT RULES:

1. Do not invent information.
2. Do not use outside knowledge.
3. Do not make assumptions about company policy.
4. If the answer is not supported by the context,
   clearly say that the information was not found
   in the available policy documents.
5. Give a concise and professional answer.
6. Do not claim something is company policy unless
   it is supported by the provided context.
"""

        # User prompt
        user_prompt = f"""
Relevant company policy context:

---------------- POLICY CONTEXT ----------------

{context}

-------------- END POLICY CONTEXT --------------

User question:

{question}

Answer using ONLY the policy context above.
"""

        # Call Groq
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.1
        )

        answer = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        return answer