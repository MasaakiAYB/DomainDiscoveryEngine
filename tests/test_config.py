from __future__ import annotations

from pathlib import Path

from domain_discovery_engine.core.config import AppConfig


def test_default_data_dir(monkeypatch) -> None:
    monkeypatch.delenv("DDE_DATA_DIR", raising=False)
    config = AppConfig()
    assert config.data_dir == Path(".data/projects")


def test_env_overrides_data_dir(monkeypatch) -> None:
    monkeypatch.setenv("DDE_DATA_DIR", "/tmp/dde-data")
    config = AppConfig()
    assert config.data_dir == Path("/tmp/dde-data")
