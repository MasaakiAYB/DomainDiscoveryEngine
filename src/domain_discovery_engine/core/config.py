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
    analyzer_mode: str = Field(default_factory=lambda: os.getenv("DDE_ANALYZER_MODE", "rule_based"))
    user_locale: str = Field(default_factory=lambda: os.getenv("DDE_USER_LOCALE", "ja-JP"))
    azure_openai_api_key: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_KEY", ""))
    azure_openai_endpoint: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_ENDPOINT", ""))
    azure_openai_api_version: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_API_VERSION", ""))
    azure_openai_deployment: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_DEPLOYMENT", ""))
    azure_openai_model: str = Field(default_factory=lambda: os.getenv("AZURE_OPENAI_MODEL", ""))
    llm_temperature: float = Field(default_factory=lambda: float(os.getenv("DDE_LLM_TEMPERATURE", "0")))
    llm_reasoning_effort: str = Field(default_factory=lambda: os.getenv("DDE_LLM_REASONING_EFFORT", ""))
