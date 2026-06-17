from __future__ import annotations

from domain_discovery_engine.agents.dialogue_analyzer import DialogueAnalyzer
from domain_discovery_engine.agents.domain_model_builder import DomainModelBuilder
from domain_discovery_engine.agents.memory_updater import MemoryUpdater
from domain_discovery_engine.agents.question_generator import QuestionGenerator
from domain_discovery_engine.agents.simulation_tester import SimulationTester
from domain_discovery_engine.core.state import DiscoveryState
from domain_discovery_engine.schemas.memory import ProjectMemory


class DiscoveryWorkflow:
    def __init__(
        self,
        dialogue_analyzer: DialogueAnalyzer | None = None,
        memory_updater: MemoryUpdater | None = None,
        domain_model_builder: DomainModelBuilder | None = None,
        simulation_tester: SimulationTester | None = None,
        question_generator: QuestionGenerator | None = None,
    ) -> None:
        self.dialogue_analyzer = dialogue_analyzer or DialogueAnalyzer()
        self.memory_updater = memory_updater or MemoryUpdater()
        self.domain_model_builder = domain_model_builder or DomainModelBuilder()
        self.simulation_tester = simulation_tester or SimulationTester()
        self.question_generator = question_generator or QuestionGenerator()

    def run_turn(self, project_memory: ProjectMemory, user_message: str) -> DiscoveryState:
        extraction = self.dialogue_analyzer.analyze(user_message, project_memory)
        memory = self.memory_updater.merge_items(project_memory, extraction.all_items())
        domain_model = self.domain_model_builder.build(memory)
        simulation_result = self.simulation_tester.run(domain_model, memory)
        memory = self.memory_updater.merge_items(memory, simulation_result.unknowns + simulation_result.contradictions)
        domain_model = self.domain_model_builder.build(memory)
        question_set = self.question_generator.generate(memory, domain_model, simulation_result)
        return DiscoveryState(
            project_id=memory.project_id,
            latest_user_message=user_message,
            project_memory=memory,
            domain_model=domain_model,
            simulation_result=simulation_result,
            question_set=question_set,
        )
