from domain_discovery_engine.schemas.memory import ProjectMemory


def test_project_memory_without_metadata_still_loads() -> None:
    payload = {
        "project_id": "demo",
        "business_rules": [
            {
                "id": "r1",
                "type": "business_rule",
                "label": "対象外候補は除外する",
                "description": "rule_type:eligibility",
                "status": "candidate",
                "confidence": 0.8,
                "source": "user",
                "evidence": "",
                "related_item_ids": [],
            }
        ],
    }
    memory = ProjectMemory.model_validate(payload)
    assert memory.business_rules[0].metadata == {}
