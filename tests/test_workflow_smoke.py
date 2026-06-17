from domain_discovery_engine.core.workflow import DiscoveryWorkflow
from domain_discovery_engine.schemas.memory import ProjectMemory


def test_workflow_smoke() -> None:
    state = DiscoveryWorkflow().run_turn(
        ProjectMemory(project_id="smoke"),
        "実験条件と結果を記録して、過去の似た実験を探せるようにしたい",
    )
    assert state.project_memory is not None
    assert state.domain_model is not None
    assert state.domain_model.concepts or state.domain_model.tasks or state.domain_model.unresolved_questions
