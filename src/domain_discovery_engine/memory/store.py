from __future__ import annotations

from typing import Protocol

from domain_discovery_engine.schemas.memory import ProjectMemory


class ProjectMemoryStore(Protocol):
    def save(self, memory: ProjectMemory) -> None:
        ...

    def load(self, project_id: str) -> ProjectMemory | None:
        ...

    def exists(self, project_id: str) -> bool:
        ...
