from domain_discovery_engine.core.workflow import DiscoveryWorkflow
from domain_discovery_engine.schemas.memory import ProjectMemory


def test_business_capability_flow_extracts_rules_criteria_and_candidates() -> None:
    state = DiscoveryWorkflow().run_turn(
        ProjectMemory(project_id="demo"),
        "購買見積を評価するとき、単価だけでなく仕様一致、単位整合、過去実績との差分を見て判断したい。明らかに対象外の候補は除外し、判断が難しいものはレビュー対象にしたい。",
    )
    assert state.business_capability_model is not None
    assert any(item.label == "対象外候補は除外する" for item in state.business_capability_model.rules)
    assert any(item.label == "仕様一致" for item in state.business_capability_model.decision_criteria)
    assert state.executable_task_candidates is not None
    assert any(item.label == "見積候補を評価する" for item in state.executable_task_candidates)
