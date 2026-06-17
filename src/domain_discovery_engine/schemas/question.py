from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class QuestionPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Question(BaseModel):
    id: str
    text: str
    reason: str
    priority: QuestionPriority
    target_unknown_ids: list[str]
    examples: list[str] = Field(default_factory=list)


class QuestionSet(BaseModel):
    candidate_questions: list[Question] = Field(default_factory=list)
    selected_question: Question | None = None
