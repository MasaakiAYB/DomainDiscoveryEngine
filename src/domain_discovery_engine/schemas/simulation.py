from __future__ import annotations

from pydantic import BaseModel, Field

from domain_discovery_engine.schemas.memory import MemoryItem


class SimulationFinding(BaseModel):
    id: str
    scenario: str
    finding_type: str
    message: str
    related_task: str | None = None
    generated_unknown: MemoryItem | None = None


class SimulationResult(BaseModel):
    findings: list[SimulationFinding] = Field(default_factory=list)
    unknowns: list[MemoryItem] = Field(default_factory=list)
    contradictions: list[MemoryItem] = Field(default_factory=list)
