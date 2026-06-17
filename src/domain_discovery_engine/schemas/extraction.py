from __future__ import annotations

from pydantic import BaseModel, Field

from domain_discovery_engine.schemas.memory import MemoryItem


class DialogueExtraction(BaseModel):
    goals: list[MemoryItem] = Field(default_factory=list)
    concepts: list[MemoryItem] = Field(default_factory=list)
    tasks: list[MemoryItem] = Field(default_factory=list)
    relations: list[MemoryItem] = Field(default_factory=list)
    constraints: list[MemoryItem] = Field(default_factory=list)
    assumptions: list[MemoryItem] = Field(default_factory=list)
    decisions: list[MemoryItem] = Field(default_factory=list)
    unknowns: list[MemoryItem] = Field(default_factory=list)

    def all_items(self) -> list[MemoryItem]:
        return [
            *self.goals,
            *self.concepts,
            *self.tasks,
            *self.relations,
            *self.constraints,
            *self.assumptions,
            *self.decisions,
            *self.unknowns,
        ]
