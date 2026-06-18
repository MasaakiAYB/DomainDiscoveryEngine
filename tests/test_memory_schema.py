from pydantic import ValidationError

from domain_discovery_engine.schemas.memory import MemoryItem, MemoryItemType, MemorySource, ProjectMemory


def test_empty_project_memory_can_be_created() -> None:
    memory = ProjectMemory(project_id="demo")
    assert memory.project_id == "demo"
    assert memory.goals == []


def test_memory_item_confidence_must_be_between_zero_and_one() -> None:
    try:
        MemoryItem(
            id="item_1",
            type=MemoryItemType.CONCEPT,
            label="実験",
            confidence=1.5,
            source=MemorySource.USER,
        )
    except ValidationError:
        pass
    else:
        raise AssertionError("Expected confidence validation to fail")


def test_list_defaults_are_not_shared() -> None:
    first = ProjectMemory(project_id="a")
    second = ProjectMemory(project_id="b")
    first.goals.append(
        MemoryItem(
            id="goal_1",
            type=MemoryItemType.GOAL,
            label="goal",
            confidence=0.5,
            source=MemorySource.USER,
        )
    )
    assert second.goals == []


def test_extended_memory_sections_exist() -> None:
    memory = ProjectMemory(project_id="demo")
    assert memory.business_rules == []
    assert memory.decision_criteria == []
    assert memory.procedures == []
    assert memory.input_outputs == []
    assert memory.executable_task_candidates == []
