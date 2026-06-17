from domain_discovery_engine.agents.simulation_tester import SimulationTester
from domain_discovery_engine.schemas.domain_model import DomainModel, DomainTask
from domain_discovery_engine.schemas.memory import MemorySource, MemoryStatus, ProjectMemory


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
