from domain_discovery_engine.agents.simulation_tester import SimulationTester
from domain_discovery_engine.schemas.domain_model import DomainModel, DomainTask
from domain_discovery_engine.schemas.memory import MemoryItem, MemoryItemType, MemorySource, MemoryStatus, ProjectMemory


def test_similarity_search_generates_unknown() -> None:
    domain_model = DomainModel(
        project_id="demo",
        tasks=[DomainTask(id="t1", name="過去の似た実験を探す")],
    )
    result = SimulationTester().run(domain_model, ProjectMemory(project_id="demo"))
    assert any(item.label == "類似判定基準が未定義" for item in result.unknowns)


def test_search_task_generates_unknown() -> None:
    domain_model = DomainModel(
        project_id="demo",
        tasks=[DomainTask(id="t1", name="実験を検索する")],
    )
    result = SimulationTester().run(domain_model, ProjectMemory(project_id="demo"))
    assert any(item.label == "検索条件が未定義" for item in result.unknowns)


def test_generated_unknowns_have_simulation_source_and_unresolved_status() -> None:
    domain_model = DomainModel(
        project_id="demo",
        tasks=[DomainTask(id="t1", name="過去の似た実験を探す")],
    )
    result = SimulationTester().run(domain_model, ProjectMemory(project_id="demo"))
    assert result.unknowns
    assert all(item.source == MemorySource.SIMULATION for item in result.unknowns)
    assert all(item.status == MemoryStatus.UNRESOLVED for item in result.unknowns)


def test_executable_task_candidate_missing_inputs_generates_unknown() -> None:
    memory = ProjectMemory(
        project_id="demo",
        executable_task_candidates=[
            MemoryItem(
                id="x1",
                type=MemoryItemType.EXECUTABLE_TASK_CANDIDATE,
                label="見積候補を評価する",
                metadata={
                    "required_inputs": [],
                    "expected_outputs": ["評価結果"],
                    "required_rules": ["r1"],
                    "required_decision_criteria": ["d1"],
                },
                confidence=0.6,
                source=MemorySource.AI_INFERRED,
            )
        ],
    )
    result = SimulationTester().run(DomainModel(project_id="demo"), memory)
    assert any(item.label == "入力情報が未定義" for item in result.unknowns)


def test_executable_task_candidate_missing_outputs_rules_and_criteria_generate_unknowns() -> None:
    memory = ProjectMemory(
        project_id="demo",
        executable_task_candidates=[
            MemoryItem(
                id="x1",
                type=MemoryItemType.EXECUTABLE_TASK_CANDIDATE,
                label="見積候補を評価する",
                metadata={},
                confidence=0.6,
                source=MemorySource.AI_INFERRED,
            )
        ],
    )
    result = SimulationTester().run(DomainModel(project_id="demo"), memory)
    labels = {item.label for item in result.unknowns}
    assert "出力情報が未定義" in labels
    assert "業務ルールが未定義" in labels
    assert "判断基準が未定義" in labels
