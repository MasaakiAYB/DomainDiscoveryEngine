from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class DomainModelItemStatus(str, Enum):
    CANDIDATE = "candidate"
    CONFIRMED = "confirmed"
    UNRESOLVED = "unresolved"


class DomainConcept(BaseModel):
    id: str
    name: str
    description: str = ""
    status: DomainModelItemStatus = DomainModelItemStatus.CANDIDATE
    source_memory_item_ids: list[str] = Field(default_factory=list)


class DomainRelation(BaseModel):
    id: str
    subject: str
    predicate: str
    object: str
    description: str = ""
    status: DomainModelItemStatus = DomainModelItemStatus.CANDIDATE
    source_memory_item_ids: list[str] = Field(default_factory=list)


class DomainTask(BaseModel):
    id: str
    name: str
    description: str = ""
    actor: str | None = None
    status: DomainModelItemStatus = DomainModelItemStatus.CANDIDATE
    source_memory_item_ids: list[str] = Field(default_factory=list)


class DomainConstraint(BaseModel):
    id: str
    label: str
    description: str = ""
    status: DomainModelItemStatus = DomainModelItemStatus.CANDIDATE
    source_memory_item_ids: list[str] = Field(default_factory=list)


class DomainModel(BaseModel):
    project_id: str
    title: str = ""
    purpose: list[str] = Field(default_factory=list)
    concepts: list[DomainConcept] = Field(default_factory=list)
    relations: list[DomainRelation] = Field(default_factory=list)
    tasks: list[DomainTask] = Field(default_factory=list)
    constraints: list[DomainConstraint] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
