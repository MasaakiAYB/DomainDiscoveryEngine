from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - optional at runtime
    def load_dotenv() -> None:
        return None


load_dotenv()


class AppConfig(BaseModel):
    data_dir: Path = Path(".data/projects")
