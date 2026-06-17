from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, Field

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - optional at runtime
    def load_dotenv() -> None:
        return None


load_dotenv()


class AppConfig(BaseModel):
    data_dir: Path = Field(default_factory=lambda: Path(os.getenv("DDE_DATA_DIR", ".data/projects")))
