from domain_discovery_engine.agents.dialogue_analyzer import LLMDialogueAnalyzer, RuleBasedDialogueAnalyzer
from domain_discovery_engine.agents.question_generator import LLMQuestionGenerator, RuleBasedQuestionGenerator
from domain_discovery_engine.core.config import AppConfig
from domain_discovery_engine.schemas.domain_model import DomainModel
from domain_discovery_engine.schemas.memory import (
    MemoryItem,
    MemoryItemType,
    MemorySource,
    MemoryStatus,
    ProjectMemory,
)
from domain_discovery_engine.schemas.simulation import SimulationResult
from domain_discovery_engine.utils.prompts import load_prompt


class EchoJapaneseProvider:
    def __init__(self) -> None:
        self.prompts: list[tuple[str, str]] = []

    def invoke(self, system_prompt: str, user_prompt: str) -> str:
        self.prompts.append((system_prompt, user_prompt))
        if "QuestionSet" in user_prompt:
            return '{"candidate_questions":[{"id":"q1","text":"過去の実験を探すとき、何を基準に「似ている」と判断しますか？","reason":"検索条件を明確にするためです。","priority":"high","target_unknown_ids":["u1"],"examples":["試料","実験条件"]}],"selected_question":{"id":"q1","text":"過去の実験を探すとき、何を基準に「似ている」と判断しますか？","reason":"検索条件を明確にするためです。","priority":"high","target_unknown_ids":["u1"],"examples":["試料","実験条件"]}}'
        return '{"goals":[{"label":"過去の似た実験を探せるようにする","source":"user","confidence":0.8}],"concepts":[{"label":"実験条件","source":"user","confidence":0.8},{"label":"実験結果","source":"user","confidence":0.8},{"label":"実験","source":"ai_inferred","confidence":0.6}],"tasks":[],"constraints":[],"assumptions":[],"unknowns":[]}'


def test_japanese_user_input_remains_japanese_in_extracted_labels() -> None:
    analyzer = RuleBasedDialogueAnalyzer()
    extraction = analyzer.analyze(
        "実験条件と結果を記録して、過去の似た実験を探せるようにしたい",
        ProjectMemory(project_id="demo"),
    )
    labels = [item.label for item in extraction.concepts]
    assert "実験条件" in labels
    assert "実験結果" in labels
    assert "実験" in labels


def test_question_generator_returns_japanese_text() -> None:
    unknown = MemoryItem(
        id="u1",
        type=MemoryItemType.UNKNOWN,
        label="類似判定基準が未定義",
        status=MemoryStatus.UNRESOLVED,
        confidence=0.7,
        source=MemorySource.SIMULATION,
    )
    question_set = RuleBasedQuestionGenerator().generate(
        ProjectMemory(project_id="demo", unknowns=[unknown]),
        DomainModel(project_id="demo"),
        SimulationResult(unknowns=[unknown]),
    )
    assert question_set.selected_question is not None
    assert any("\u3040" <= char <= "\u30ff" or "\u4e00" <= char <= "\u9faf" for char in question_set.selected_question.text)


def test_internal_schema_fields_remain_english() -> None:
    keys = set(ProjectMemory.model_fields.keys())
    assert "project_id" in keys
    assert "unknowns" in keys
    assert "goals" in keys


def test_prompt_files_exist_in_new_directory_structure() -> None:
    assert load_prompt("internal", "dialogue_analyzer.md")
    assert load_prompt("internal", "domain_model_builder.md")
    assert load_prompt("internal", "simulation_tester.md")
    assert load_prompt("user_facing", "question_generator.md")
    assert load_prompt("user_facing", "response_composer.md")


def test_llm_question_generator_uses_japanese_locale_instruction() -> None:
    provider = EchoJapaneseProvider()
    unknown = MemoryItem(
        id="u1",
        type=MemoryItemType.UNKNOWN,
        label="検索条件が未定義",
        status=MemoryStatus.UNRESOLVED,
        confidence=0.7,
        source=MemorySource.SIMULATION,
    )
    generator = LLMQuestionGenerator(provider=provider, config=AppConfig(user_locale="ja-JP"))
    result = generator.generate(
        ProjectMemory(project_id="demo", unknowns=[unknown]),
        DomainModel(project_id="demo"),
        SimulationResult(unknowns=[unknown]),
    )
    assert result.selected_question is not None
    assert "ja-JP" in provider.prompts[-1][1]
