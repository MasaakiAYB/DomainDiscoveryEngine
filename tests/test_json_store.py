from pathlib import Path

from domain_discovery_engine.memory.json_store import JsonProjectMemoryStore
from domain_discovery_engine.schemas.memory import MemoryItem, MemoryItemType, MemorySource, ProjectMemory


def test_save_then_load_preserves_fields(tmp_path: Path) -> None:
    store = JsonProjectMemoryStore(tmp_path)
    memory = ProjectMemory(project_id="demo")
    memory.concepts.append(
        MemoryItem(
            id="concept_1",
            type=MemoryItemType.CONCEPT,
            label="実験",
            confidence=0.9,
            source=MemorySource.USER,
        )
    )
    store.save(memory)

    loaded = store.load("demo")
    assert loaded is not None
    assert loaded.concepts[0].label == "実験"


def test_loading_missing_project_returns_none(tmp_path: Path) -> None:
    store = JsonProjectMemoryStore(tmp_path)
    assert store.load("missing") is None


def test_exists_works(tmp_path: Path) -> None:
    store = JsonProjectMemoryStore(tmp_path)
    memory = ProjectMemory(project_id="demo")
    assert store.exists("demo") is False
    store.save(memory)
    assert store.exists("demo") is True


def test_store_creates_parent_directories(tmp_path: Path) -> None:
    store = JsonProjectMemoryStore(tmp_path / "nested" / "projects")
    store.save(ProjectMemory(project_id="demo"))
    assert (tmp_path / "nested" / "projects" / "demo" / "project_memory.json").exists()
