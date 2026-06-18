from domain_discovery_engine.schemas.business_capability import (
    BusinessCapabilityModel,
    BusinessRule,
    DecisionCriterion,
    ExecutableTaskCandidate,
    InputOutputSpec,
)
from domain_discovery_engine.schemas.domain_model import DomainConcept, DomainTask
from domain_discovery_engine.schemas.memory import MemorySource, MemoryStatus


def test_business_capability_model_can_be_created() -> None:
    model = BusinessCapabilityModel(
        purpose=["見積評価を標準化する"],
        concepts=[DomainConcept(id="c1", name="見積候補")],
        tasks=[DomainTask(id="t1", name="見積候補を評価する")],
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
                label="見積評価入出力",
                input_items=["仕様", "単価"],
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
                required_inputs=["仕様", "単価"],
                expected_outputs=["評価結果"],
                required_rules=["対象外候補は除外する"],
                required_decision_criteria=["仕様一致"],
                required_procedures=[],
                status=MemoryStatus.CANDIDATE,
                source=MemorySource.AI_INFERRED,
                confidence=0.6,
            )
        ],
    )
    assert model.rules[0].label == "対象外候補は除外する"

