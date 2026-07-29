from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Policy question"
    )


class Source(BaseModel):
    source: str
    section: str = ""


class QuestionResponse(BaseModel):
    answer: str
    sources: list[Source]