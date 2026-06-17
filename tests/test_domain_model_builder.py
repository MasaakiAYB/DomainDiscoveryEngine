from domain_discovery_engine.agents.domain_model_builder import DomainModelBuilder
from domain_discovery_engine.schemas.memory import (
    MemoryItem,
    MemoryItemType,
    MemorySource,
    MemoryStatus,
    ProjectMemory,
)


def test_concepts_are_mapped() -> None:
    memory = ProjectMemory(
        project_id="demo",
        concepts=[
            MemoryItem(
                id="c1",
                type=MemoryItemType.CONCEPT,
                label="実験",
                confidence=0.7,
                source=MemorySource.USER,
            )
        ],
    )
    model = DomainModelBuilder().build(memory)
    assert model.concepts[0].name == "実験"


def test_unknowns_appear_as_unresolved_questions() -> None:
    memory = ProjectMemory(
        project_id="demo",
        unknowns=[
            MemoryItem(
                id="u1",
                type=MemoryItemType.UNKNOWN,
                label="似た実験の判定基準",
                status=MemoryStatus.UNRESOLVED,
                confidence=0.7,
                source=MemorySource.SIMULATION,
            )
        ],
    )
    model = DomainModelBuilder().build(memory)
    assert "似た実験の判定基準" in model.unresolved_questions


def test_rejected_items_do_not_appear() -> None:
    memory = ProjectMemory(
        project_id="demo",
        concepts=[
            MemoryItem(
                id="c1",
                type=MemoryItemType.CONCEPT,
                label="実験",
                status=MemoryStatus.REJECTED,
                confidence=0.7,
                source=MemorySource.USER,
            )
        ],
    )
    model = DomainModelBuilder().build(memory)
    assert model.concepts == []
