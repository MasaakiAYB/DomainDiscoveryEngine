from domain_discovery_engine.core.workflow import DiscoveryWorkflow
from domain_discovery_engine.schemas.memory import ProjectMemory


def test_workflow_generates_domain_model_and_question() -> None:
    workflow = DiscoveryWorkflow()
    state = workflow.run_turn(
        ProjectMemory(project_id="demo"),
        "実験条件と結果を記録して、過去の似た実験を探せるようにしたい",
    )

    assert any(concept.name == "実験条件" for concept in state.domain_model.concepts)
    assert any(task.name == "過去の似た実験を探す" for task in state.domain_model.tasks)
    assert state.question_set is not None
    assert state.question_set.selected_question is not None
