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
                metadata={"rule_type": "eligibility"},
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


def test_business_capability_builder_prefers_metadata_over_description() -> None:
    memory = ProjectMemory(
        project_id="demo",
        business_rules=[
            MemoryItem(
                id="r1",
                type=MemoryItemType.BUSINESS_RULE,
                label="対象外候補は除外する",
                description="rule_type:validation",
                metadata={"rule_type": "eligibility"},
                confidence=0.8,
                source=MemorySource.USER,
            )
        ],
    )
    model = RuleBasedBusinessCapabilityBuilder().build(memory)
    assert model.rules[0].rule_type == "eligibility"


def test_business_capability_builder_falls_back_to_description_metadata() -> None:
    memory = ProjectMemory(
        project_id="demo",
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
    assert model.rules[0].rule_type == "eligibility"


def test_new_task_candidate_data_does_not_require_description_parsing() -> None:
    memory = ProjectMemory(
        project_id="demo",
        executable_task_candidates=[
            MemoryItem(
                id="x1",
                type=MemoryItemType.EXECUTABLE_TASK_CANDIDATE,
                label="見積候補を評価する",
                description="見積候補を評価する",
                metadata={
                    "task_type": "unknown",
                    "required_inputs": ["品名", "仕様"],
                    "expected_outputs": ["評価結果"],
                    "required_rules": ["r1"],
                    "required_decision_criteria": ["d1"],
                    "required_procedures": ["p1"],
                },
                confidence=0.7,
                source=MemorySource.AI_INFERRED,
            )
        ],
    )
    model = RuleBasedBusinessCapabilityBuilder().build(memory)
    candidate = model.executable_task_candidates[0]
    assert candidate.required_inputs == ["品名", "仕様"]
    assert candidate.required_rules == ["r1"]
