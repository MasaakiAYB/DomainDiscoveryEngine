from __future__ import annotations

from pydantic import BaseModel, Field

from domain_discovery_engine.schemas.domain_model import DomainConcept, DomainConstraint, DomainTask
from domain_discovery_engine.schemas.memory import MemorySource, MemoryStatus


class BusinessRule(BaseModel):
    id: str
    label: str
    description: str = ""
    rule_type: str
    status: MemoryStatus
    source: MemorySource
    evidence: str | None = None
    confidence: float


class DecisionCriterion(BaseModel):
    id: str
    label: str
    description: str = ""
    criterion_type: str
    status: MemoryStatus
    source: MemorySource
    evidence: str | None = None
    confidence: float


class BusinessProcedure(BaseModel):
    id: str
    label: str
    description: str = ""
    steps: list[str] = Field(default_factory=list)
    status: MemoryStatus
    source: MemorySource
    evidence: str | None = None
    confidence: float


class InputOutputSpec(BaseModel):
    id: str
    label: str
    description: str = ""
    input_items: list[str] = Field(default_factory=list)
    output_items: list[str] = Field(default_factory=list)
    status: MemoryStatus
    source: MemorySource
    evidence: str | None = None
    confidence: float


class ExecutableTaskCandidate(BaseModel):
    id: str
    label: str
    description: str = ""
    task_type: str
    required_inputs: list[str] = Field(default_factory=list)
    expected_outputs: list[str] = Field(default_factory=list)
    required_rules: list[str] = Field(default_factory=list)
    required_decision_criteria: list[str] = Field(default_factory=list)
    required_procedures: list[str] = Field(default_factory=list)
    status: MemoryStatus
    source: MemorySource
    evidence: str | None = None
    confidence: float


class BusinessCapabilityModel(BaseModel):
    purpose: list[str] = Field(default_factory=list)
    concepts: list[DomainConcept] = Field(default_factory=list)
    tasks: list[DomainTask] = Field(default_factory=list)
    rules: list[BusinessRule] = Field(default_factory=list)
    decision_criteria: list[DecisionCriterion] = Field(default_factory=list)
    procedures: list[BusinessProcedure] = Field(default_factory=list)
    input_outputs: list[InputOutputSpec] = Field(default_factory=list)
    constraints: list[DomainConstraint] = Field(default_factory=list)
    executable_task_candidates: list[ExecutableTaskCandidate] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
