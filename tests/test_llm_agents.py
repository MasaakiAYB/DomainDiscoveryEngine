from domain_discovery_engine.agents.dialogue_analyzer import LLMDialogueAnalyzer
from domain_discovery_engine.agents.domain_model_builder import LLMDomainModelBuilder
from domain_discovery_engine.agents.question_generator import LLMQuestionGenerator
from domain_discovery_engine.agents.simulation_tester import LLMSimulationTester
from domain_discovery_engine.schemas.domain_model import DomainModel
from domain_discovery_engine.schemas.memory import (
    MemoryItem,
    MemoryItemType,
    MemorySource,
    MemoryStatus,
    ProjectMemory,
)
from domain_discovery_engine.schemas.simulation import SimulationResult


class StubProvider:
    def __init__(self, response: str) -> None:
        self.response = response

    def invoke(self, system_prompt: str, user_prompt: str) -> str:
        assert system_prompt
        assert user_prompt
        return self.response


def test_llm_dialogue_analyzer_parses_json() -> None:
    analyzer = LLMDialogueAnalyzer(
        provider=StubProvider(
            '{"goals":[{"label":"実験を探しやすくする","source":"user","confidence":0.8}],"concepts":[{"label":"実験","source":"ai_inferred","confidence":0.6}],"tasks":[],"constraints":[],"assumptions":[],"unknowns":[]}'
        )
    )
    extraction = analyzer.analyze("msg", ProjectMemory(project_id="demo"))
    assert extraction.goals[0].label == "実験を探しやすくする"


def test_llm_domain_model_builder_parses_json() -> None:
    builder = LLMDomainModelBuilder(
        provider=StubProvider('{"project_id":"demo","purpose":["整理する"],"concepts":[],"relations":[],"tasks":[],"constraints":[],"assumptions":[],"decisions":[],"unresolved_questions":[]}')
    )
    model = builder.build(ProjectMemory(project_id="demo"))
    assert model.purpose == ["整理する"]


def test_llm_simulation_tester_falls_back_on_invalid_json() -> None:
    tester = LLMSimulationTester(provider=StubProvider("not json"))
    result = tester.run(
        DomainModel(project_id="demo", tasks=[]),
        ProjectMemory(project_id="demo"),
    )
    assert isinstance(result, SimulationResult)


def test_llm_question_generator_parses_json() -> None:
    unknown = MemoryItem(
        id="u1",
        type=MemoryItemType.UNKNOWN,
        label="検索条件が未定義",
        status=MemoryStatus.UNRESOLVED,
        confidence=0.7,
        source=MemorySource.SIMULATION,
    )
    generator = LLMQuestionGenerator(
        provider=StubProvider(
            '{"candidate_questions":[{"id":"q1","text":"どんな条件で絞り込みますか？","reason":"検索に必要なため","priority":"high","target_unknown_ids":["u1"],"examples":["日付"]}],"selected_question":{"id":"q1","text":"どんな条件で絞り込みますか？","reason":"検索に必要なため","priority":"high","target_unknown_ids":["u1"],"examples":["日付"]}}'
        )
    )
    result = generator.generate(
        ProjectMemory(project_id="demo", unknowns=[unknown]),
        DomainModel(project_id="demo"),
        SimulationResult(unknowns=[unknown]),
    )
    assert result.selected_question is not None
    assert result.selected_question.target_unknown_ids == ["u1"]
