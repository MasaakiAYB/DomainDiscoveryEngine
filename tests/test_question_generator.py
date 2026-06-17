from domain_discovery_engine.agents.question_generator import QuestionGenerator
from domain_discovery_engine.schemas.domain_model import DomainModel
from domain_discovery_engine.schemas.memory import (
    MemoryItem,
    MemoryItemType,
    MemorySource,
    MemoryStatus,
    ProjectMemory,
)
from domain_discovery_engine.schemas.simulation import SimulationResult


def test_similarity_unknown_produces_business_friendly_question() -> None:
    unknown = MemoryItem(
        id="u1",
        type=MemoryItemType.UNKNOWN,
        label="類似判定基準が未定義",
        status=MemoryStatus.UNRESOLVED,
        confidence=0.8,
        source=MemorySource.SIMULATION,
    )
    memory = ProjectMemory(project_id="demo", unknowns=[unknown])
    question_set = QuestionGenerator().generate(
        memory,
        DomainModel(project_id="demo"),
        SimulationResult(unknowns=[unknown]),
    )
    assert question_set.selected_question is not None
    assert "何が近いものを似ていると判断しますか？" in question_set.selected_question.text


def test_only_one_selected_question_is_returned() -> None:
    memory = ProjectMemory(
        project_id="demo",
        unknowns=[
            MemoryItem(
                id="u1",
                type=MemoryItemType.UNKNOWN,
                label="検索条件が未定義",
                status=MemoryStatus.UNRESOLVED,
                confidence=0.8,
                source=MemorySource.SIMULATION,
            ),
            MemoryItem(
                id="u2",
                type=MemoryItemType.UNKNOWN,
                label="予約に必要な入力項目",
                status=MemoryStatus.UNRESOLVED,
                confidence=0.8,
                source=MemorySource.SIMULATION,
            ),
        ],
    )
    question_set = QuestionGenerator().generate(memory, DomainModel(project_id="demo"))
    assert question_set.selected_question is not None
    assert len(question_set.selected_question.target_unknown_ids) == 1


def test_selected_question_references_target_unknown_ids() -> None:
    unknown = MemoryItem(
        id="u1",
        type=MemoryItemType.UNKNOWN,
        label="予約に必要な入力項目",
        status=MemoryStatus.UNRESOLVED,
        confidence=0.8,
        source=MemorySource.SIMULATION,
    )
    question_set = QuestionGenerator().generate(
        ProjectMemory(project_id="demo", unknowns=[unknown]),
        DomainModel(project_id="demo"),
    )
    assert question_set.selected_question is not None
    assert question_set.selected_question.target_unknown_ids == ["u1"]
