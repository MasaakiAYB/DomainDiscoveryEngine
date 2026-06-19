from __future__ import annotations

from domain_discovery_engine.agents.dialogue_analyzer import LLMDialogueAnalyzer, RuleBasedDialogueAnalyzer
from domain_discovery_engine.agents.business_capability_builder import (
    LLMBusinessCapabilityBuilder,
    RuleBasedBusinessCapabilityBuilder,
)
from domain_discovery_engine.agents.domain_model_builder import (
    LLMDomainModelBuilder,
    RuleBasedDomainModelBuilder,
)
from domain_discovery_engine.agents.memory_updater import MemoryUpdater
from domain_discovery_engine.agents.question_generator import (
    LLMQuestionGenerator,
    RuleBasedQuestionGenerator,
)
from domain_discovery_engine.agents.simulation_tester import (
    LLMSimulationTester,
    RuleBasedSimulationTester,
)
from domain_discovery_engine.agents.task_candidate_extractor import (
    LLMTaskCandidateExtractor,
    RuleBasedTaskCandidateExtractor,
)
from domain_discovery_engine.core.config import AppConfig
from domain_discovery_engine.core.state import DiscoveryState
from domain_discovery_engine.llm.provider import LLMProvider
from domain_discovery_engine.schemas.memory import ProjectMemory


class DiscoveryWorkflow:
    def __init__(
        self,
        dialogue_analyzer=None,
        memory_updater: MemoryUpdater | None = None,
        domain_model_builder=None,
        business_capability_builder=None,
        task_candidate_extractor=None,
        simulation_tester=None,
        question_generator=None,
        llm_provider: LLMProvider | None = None,
        config: AppConfig | None = None,
    ) -> None:
        self.config = config or AppConfig()
        provider = llm_provider or LLMProvider(self.config)
        use_llm = self.config.analyzer_mode == "llm"
        self.dialogue_analyzer = dialogue_analyzer or (
            LLMDialogueAnalyzer(provider=provider) if use_llm else RuleBasedDialogueAnalyzer()
        )
        self.memory_updater = memory_updater or MemoryUpdater()
        self.domain_model_builder = domain_model_builder or (
            LLMDomainModelBuilder(provider=provider) if use_llm else RuleBasedDomainModelBuilder()
        )
        self.business_capability_builder = business_capability_builder or (
            LLMBusinessCapabilityBuilder(provider=provider) if use_llm else RuleBasedBusinessCapabilityBuilder()
        )
        self.task_candidate_extractor = task_candidate_extractor or (
            LLMTaskCandidateExtractor(provider=provider) if use_llm else RuleBasedTaskCandidateExtractor()
        )
        self.simulation_tester = simulation_tester or (
            LLMSimulationTester(provider=provider) if use_llm else RuleBasedSimulationTester()
        )
        self.question_generator = question_generator or (
            LLMQuestionGenerator(provider=provider, config=self.config)
            if use_llm
            else RuleBasedQuestionGenerator()
        )

    def run_turn(self, project_memory: ProjectMemory, user_message: str) -> DiscoveryState:
        extraction = self.dialogue_analyzer.analyze(user_message, project_memory)
        memory = self.memory_updater.merge_items(project_memory, extraction.all_items())
        domain_model = self.domain_model_builder.build(memory)
        business_capability_model = self.business_capability_builder.build(memory)
        candidates = self.task_candidate_extractor.extract(business_capability_model)
        memory = self.memory_updater.merge_items(
            memory,
            [
                self._candidate_to_memory_item(candidate)
                for candidate in candidates
            ],
        )
        business_capability_model = self.business_capability_builder.build(memory)
        simulation_result = self.simulation_tester.run(domain_model, memory)
        memory = self.memory_updater.merge_items(memory, simulation_result.unknowns + simulation_result.contradictions)
        domain_model = self.domain_model_builder.build(memory)
        business_capability_model = self.business_capability_builder.build(memory)
        candidates = self.task_candidate_extractor.extract(business_capability_model)
        question_set = self.question_generator.generate(memory, domain_model, simulation_result)
        return DiscoveryState(
            project_id=memory.project_id,
            latest_user_message=user_message,
            project_memory=memory,
            domain_model=domain_model,
            business_capability_model=business_capability_model,
            executable_task_candidates=candidates,
            simulation_result=simulation_result,
            question_set=question_set,
        )

    def _candidate_to_memory_item(self, candidate):
        from domain_discovery_engine.schemas.memory import MemoryItem, MemoryItemType

        return MemoryItem(
            id=candidate.id,
            type=MemoryItemType.EXECUTABLE_TASK_CANDIDATE,
            label=candidate.label,
            description=candidate.description,
            metadata={
                "task_type": candidate.task_type,
                "required_inputs": candidate.required_inputs,
                "expected_outputs": candidate.expected_outputs,
                "required_rules": candidate.required_rules,
                "required_decision_criteria": candidate.required_decision_criteria,
                "required_procedures": candidate.required_procedures,
            },
            status=candidate.status,
            confidence=candidate.confidence,
            source=candidate.source,
            evidence=candidate.evidence or "",
        )
