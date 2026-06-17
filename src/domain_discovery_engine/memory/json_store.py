from __future__ import annotations

import json
from pathlib import Path

from domain_discovery_engine.memory.store import ProjectMemoryStore
from domain_discovery_engine.schemas.memory import ProjectMemory


class JsonProjectMemoryStore(ProjectMemoryStore):
    def __init__(self, base_dir: Path | str = Path(".data/projects")) -> None:
        self.base_dir = Path(base_dir)

    def save(self, memory: ProjectMemory) -> None:
        path = self._project_file(memory.project_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(memory.model_dump(mode="json"), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load(self, project_id: str) -> ProjectMemory | None:
        path = self._project_file(project_id)
        if not path.exists():
            return None
        return ProjectMemory.model_validate_json(path.read_text(encoding="utf-8"))

    def exists(self, project_id: str) -> bool:
        return self._project_file(project_id).exists()

    def _project_file(self, project_id: str) -> Path:
        return self.base_dir / project_id / "project_memory.json"
