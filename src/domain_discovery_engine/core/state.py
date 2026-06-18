from __future__ import annotations

from domain_discovery_engine.schemas.business_capability import BusinessCapabilityModel, ExecutableTaskCandidate
from pydantic import BaseModel

from domain_discovery_engine.schemas.domain_model import DomainModel
from domain_discovery_engine.schemas.memory import ProjectMemory
from domain_discovery_engine.schemas.question import QuestionSet
from domain_discovery_engine.schemas.simulation import SimulationResult


class DiscoveryState(BaseModel):
    project_id: str
    latest_user_message: str | None
    project_memory: ProjectMemory
    domain_model: DomainModel | None = None
    business_capability_model: BusinessCapabilityModel | None = None
    executable_task_candidates: list[ExecutableTaskCandidate] | None = None
    simulation_result: SimulationResult | None = None
    question_set: QuestionSet | None = None
