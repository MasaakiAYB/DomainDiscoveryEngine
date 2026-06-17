from domain_discovery_engine.agents.memory_updater import MemoryUpdater
from domain_discovery_engine.schemas.memory import (
    MemoryItem,
    MemoryItemType,
    MemorySource,
    MemoryStatus,
    ProjectMemory,
)


def test_new_concept_is_added() -> None:
    memory = ProjectMemory(project_id="demo")
    updater = MemoryUpdater()
    updater.merge_items(
        memory,
        [
            MemoryItem(
                id="c1",
                type=MemoryItemType.CONCEPT,
                label="実験",
                confidence=0.8,
                source=MemorySource.USER,
            )
        ],
    )
    assert memory.concepts[0].label == "実験"


def test_duplicate_label_is_not_duplicated() -> None:
    memory = ProjectMemory(project_id="demo")
    updater = MemoryUpdater()
    items = [
        MemoryItem(
            id="c1",
            type=MemoryItemType.CONCEPT,
            label="実験結果",
            confidence=0.5,
            source=MemorySource.USER,
        ),
        MemoryItem(
            id="c2",
            type=MemoryItemType.CONCEPT,
            label=" 実験結果 ",
            confidence=0.7,
            source=MemorySource.AI_INFERRED,
        ),
    ]
    updater.merge_items(memory, items)
    assert len(memory.concepts) == 1
    assert memory.concepts[0].confidence == 0.7


def test_confirmed_user_item_is_not_downgraded() -> None:
    memory = ProjectMemory(
        project_id="demo",
        concepts=[
            MemoryItem(
                id="c1",
                type=MemoryItemType.CONCEPT,
                label="実験",
                status=MemoryStatus.CONFIRMED,
                confidence=0.9,
                source=MemorySource.USER,
            )
        ],
    )
    updater = MemoryUpdater()
    updater.merge_items(
        memory,
        [
            MemoryItem(
                id="c2",
                type=MemoryItemType.CONCEPT,
                label="実験",
                status=MemoryStatus.CANDIDATE,
                confidence=0.4,
                source=MemorySource.AI_INFERRED,
            )
        ],
    )
    assert memory.concepts[0].status == MemoryStatus.CONFIRMED
    assert memory.concepts[0].source == MemorySource.USER


def test_rejected_item_is_routed_to_rejected_items() -> None:
    memory = ProjectMemory(project_id="demo")
    updater = MemoryUpdater()
    updater.merge_items(
        memory,
        [
            MemoryItem(
                id="r1",
                type=MemoryItemType.REJECTED,
                label="不要機能",
                status=MemoryStatus.REJECTED,
                confidence=0.8,
                source=MemorySource.USER,
            )
        ],
    )
    assert len(memory.rejected_items) == 1
