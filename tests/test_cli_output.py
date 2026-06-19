from domain_discovery_engine.core.state import DiscoveryState
from domain_discovery_engine.interfaces.cli import _print_state
from domain_discovery_engine.schemas.business_capability import (
    BusinessCapabilityModel,
    BusinessRule,
    DecisionCriterion,
    ExecutableTaskCandidate,
    InputOutputSpec,
)
from domain_discovery_engine.schemas.domain_model import DomainModel, DomainTask
from domain_discovery_engine.schemas.memory import MemorySource, MemoryStatus, ProjectMemory


def test_cli_prints_business_capability_sections(capsys) -> None:
    state = DiscoveryState(
        project_id="demo",
        latest_user_message="msg",
        project_memory=ProjectMemory(project_id="demo"),
        domain_model=DomainModel(
            project_id="demo",
            tasks=[DomainTask(id="t1", name="見積候補を評価する")],
            unresolved_questions=["判断基準が未定義"],
        ),
        business_capability_model=BusinessCapabilityModel(
            purpose=["見積評価を標準化する"],
            rules=[
                BusinessRule(
                    id="r1",
                    label="対象外候補は除外する",
                    rule_type="eligibility",
                    status=MemoryStatus.CANDIDATE,
                    source=MemorySource.USER,
                    confidence=0.8,
                )
            ],
            decision_criteria=[
                DecisionCriterion(
                    id="d1",
                    label="仕様一致",
                    criterion_type="evaluation",
                    status=MemoryStatus.CANDIDATE,
                    source=MemorySource.USER,
                    confidence=0.8,
                )
            ],
            input_outputs=[
                InputOutputSpec(
                    id="io1",
                    label="見積評価",
                    input_items=["品名"],
                    output_items=["評価結果"],
                    status=MemoryStatus.CANDIDATE,
                    source=MemorySource.AI_INFERRED,
                    confidence=0.6,
                )
            ],
            executable_task_candidates=[
                ExecutableTaskCandidate(
                    id="x1",
                    label="見積候補を評価する",
                    task_type="unknown",
                    required_inputs=["品名"],
                    expected_outputs=["評価結果"],
                    required_rules=["r1"],
                    required_decision_criteria=["d1"],
                    required_procedures=[],
                    status=MemoryStatus.CANDIDATE,
                    source=MemorySource.AI_INFERRED,
                    confidence=0.6,
                )
            ],
            unknowns=["判断基準が未定義"],
        ),
    )
    _print_state(state)
    output = capsys.readouterr().out
    assert "業務ルール（BusinessRule）" in output
    assert "判断基準（DecisionCriterion）" in output
    assert "入出力仕様（InputOutputSpec）" in output
    assert "実行可能タスク候補（ExecutableTaskCandidate）" in output
    assert "未解決事項（Unknown）" in output
