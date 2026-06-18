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
    business_rules: list[MemoryItem] = Field(default_factory=list)
    decision_criteria: list[MemoryItem] = Field(default_factory=list)
    procedures: list[MemoryItem] = Field(default_factory=list)
    input_outputs: list[MemoryItem] = Field(default_factory=list)
    executable_task_candidates: list[MemoryItem] = Field(default_factory=list)
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
            *self.business_rules,
            *self.decision_criteria,
            *self.procedures,
            *self.input_outputs,
            *self.executable_task_candidates,
            *self.unknowns,
        ]
