from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class MemoryItemType(str, Enum):
    GOAL = "goal"
    CONCEPT = "concept"
    TASK = "task"
    RELATION = "relation"
    CONSTRAINT = "constraint"
    ASSUMPTION = "assumption"
    DECISION = "decision"
    UNKNOWN = "unknown"
    REJECTED = "rejected"
    CONTRADICTION = "contradiction"


class MemoryStatus(str, Enum):
    CANDIDATE = "candidate"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    UNRESOLVED = "unresolved"


class MemorySource(str, Enum):
    USER = "user"
    AI_INFERRED = "ai_inferred"
    SIMULATION = "simulation"


class MemoryItem(BaseModel):
    id: str
    type: MemoryItemType
    label: str
    description: str = ""
    status: MemoryStatus = MemoryStatus.CANDIDATE
    confidence: float = Field(ge=0.0, le=1.0)
    source: MemorySource
    evidence: str = ""
    related_item_ids: list[str] = Field(default_factory=list)


class ProjectMemory(BaseModel):
    project_id: str
    title: str = ""
    goals: list[MemoryItem] = Field(default_factory=list)
    concepts: list[MemoryItem] = Field(default_factory=list)
    tasks: list[MemoryItem] = Field(default_factory=list)
    relations: list[MemoryItem] = Field(default_factory=list)
    constraints: list[MemoryItem] = Field(default_factory=list)
    assumptions: list[MemoryItem] = Field(default_factory=list)
    decisions: list[MemoryItem] = Field(default_factory=list)
    unknowns: list[MemoryItem] = Field(default_factory=list)
    rejected_items: list[MemoryItem] = Field(default_factory=list)
    contradictions: list[MemoryItem] = Field(default_factory=list)
