from domain_discovery_engine.core.config import AppConfig
from domain_discovery_engine.core.workflow import DiscoveryWorkflow


def test_workflow_uses_rule_based_mode_by_default() -> None:
    workflow = DiscoveryWorkflow(config=AppConfig(analyzer_mode="rule_based"))
    assert workflow.dialogue_analyzer.__class__.__name__ == "RuleBasedDialogueAnalyzer"


def test_workflow_uses_llm_mode_when_configured() -> None:
    class DummyProvider:
        def invoke(self, system_prompt: str, user_prompt: str) -> str:
            return '{"goals":[],"concepts":[],"tasks":[],"constraints":[],"assumptions":[],"unknowns":[]}'

    workflow = DiscoveryWorkflow(
        config=AppConfig(analyzer_mode="llm"),
        llm_provider=DummyProvider(),
    )
    assert workflow.dialogue_analyzer.__class__.__name__ == "LLMDialogueAnalyzer"
