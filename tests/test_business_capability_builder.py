from domain_discovery_engine.agents.business_capability_builder import RuleBasedBusinessCapabilityBuilder
from domain_discovery_engine.agents.task_candidate_extractor import RuleBasedTaskCandidateExtractor
from domain_discovery_engine.schemas.memory import MemoryItem, MemoryItemType, MemorySource, ProjectMemory


def test_business_capability_builder_maps_extended_memory() -> None:
    memory = ProjectMemory(
        project_id="demo",
        goals=[
            MemoryItem(
                id="g1",
                type=MemoryItemType.GOAL,
                label="見積評価を標準化する",
                confidence=0.8,
                source=MemorySource.USER,
            )
        ],
        business_rules=[
            MemoryItem(
                id="r1",
                type=MemoryItemType.BUSINESS_RULE,
                label="対象外候補は除外する",
                description="rule_type:eligibility",
                confidence=0.8,
                source=MemorySource.USER,
            )
        ],
    )
    model = RuleBasedBusinessCapabilityBuilder().build(memory)
    assert model.purpose == ["見積評価を標準化する"]
    assert model.rules[0].label == "対象外候補は除外する"


def test_task_candidate_extractor_generates_candidates() -> None:
    memory = ProjectMemory(
        project_id="demo",
        tasks=[
            MemoryItem(
                id="t1",
                type=MemoryItemType.TASK,
                label="見積候補を評価する",
                confidence=0.8,
                source=MemorySource.USER,
            )
        ],
        business_rules=[
            MemoryItem(
                id="r1",
                type=MemoryItemType.BUSINESS_RULE,
                label="対象外候補は除外する",
                confidence=0.8,
                source=MemorySource.USER,
            )
        ],
    )
    candidates = RuleBasedTaskCandidateExtractor().extract(memory)
    assert any(candidate.label == "見積候補を評価する" for candidate in candidates)
