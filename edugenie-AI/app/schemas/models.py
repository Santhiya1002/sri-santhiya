from typing import List
from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=2,
        max_length=30000
    )

    @field_validator("text")
    @classmethod
    def clean_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Input cannot be empty.")

        return value


class QARequest(TextRequest):
    pass


class ExplainRequest(TextRequest):
    pass


class SummaryRequest(TextRequest):
    pass


class LearningPathRequest(TextRequest):
    level: str = Field(
        default="beginner",
        min_length=3,
        max_length=30
    )

    @field_validator("level")
    @classmethod
    def normalize_level(cls, value: str) -> str:
        value = value.strip().lower()

        allowed_levels = {
            "beginner",
            "intermediate",
            "advanced"
        }

        if value not in allowed_levels:
            raise ValueError(
                "Level must be beginner, intermediate, or advanced."
            )

        return value


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(
        ...,
        min_length=4,
        max_length=4
    )
    correct_answer: str

    @field_validator("correct_answer")
    @classmethod
    def validate_answer(cls, value: str) -> str:
        return value.strip()


class QuizResponse(BaseModel):
    questions: List[QuizQuestion] = Field(
        ...,
        min_length=3,
        max_length=3
    )


class TextResponse(BaseModel):
    result: str


class HealthResponse(BaseModel):
    status: str
    gemini_configured: bool
    model: str
