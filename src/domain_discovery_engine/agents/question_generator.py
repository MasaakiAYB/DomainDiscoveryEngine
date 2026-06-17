from __future__ import annotations

from domain_discovery_engine.llm.provider import LLMProvider
from domain_discovery_engine.schemas.domain_model import DomainModel
from domain_discovery_engine.schemas.memory import MemoryItem, MemorySource, ProjectMemory
from domain_discovery_engine.schemas.question import Question, QuestionPriority, QuestionSet
from domain_discovery_engine.schemas.simulation import SimulationResult
from domain_discovery_engine.utils.ids import new_id
from domain_discovery_engine.utils.json import extract_json_object
from domain_discovery_engine.utils.prompts import load_prompt


class RuleBasedQuestionGenerator:
    def generate(
        self,
        memory: ProjectMemory,
        domain_model: DomainModel,
        simulation_result: SimulationResult | None = None,
    ) -> QuestionSet:
        del domain_model
        unknowns = list(memory.unknowns)
        if simulation_result is not None:
            simulation_ids = {item.id for item in simulation_result.unknowns}
            unknowns.sort(key=lambda item: (item.id not in simulation_ids, item.label))
        else:
            unknowns.sort(key=lambda item: item.label)

        candidates = [self._question_for_unknown(item) for item in unknowns]
        selected = self._select(candidates)
        return QuestionSet(candidate_questions=candidates, selected_question=selected)

    def _question_for_unknown(self, item: MemoryItem) -> Question:
        if "似た実験の判定基準" in item.label or "類似判定基準" in item.label:
            return Question(
                id=new_id("question"),
                text="「似た実験」を探すとき、何が近いものを似ていると判断しますか？",
                reason="類似条件が決まらないと、検索結果の出し方を決められないためです。",
                priority=self._priority(item),
                target_unknown_ids=[item.id],
                examples=["試料", "実験条件", "測定値", "目的", "担当者"],
            )
        if "予約に必要な入力項目" in item.label:
            return Question(
                id=new_id("question"),
                text="設備を予約するとき、予約に必要な情報は何ですか？",
                reason="予約処理に必要な入力が決まっていないためです。",
                priority=self._priority(item),
                target_unknown_ids=[item.id],
                examples=["設備名", "利用者", "開始時刻", "終了時刻", "利用目的"],
            )
        if "検索条件" in item.label:
            return Question(
                id=new_id("question"),
                text="探したい情報を絞り込むとき、どんな条件で検索できるとよいですか？",
                reason="検索条件がないと、目的の情報にたどり着けないためです。",
                priority=self._priority(item),
                target_unknown_ids=[item.id],
                examples=["キーワード", "日付", "担当者", "設備", "状態"],
            )
        return Question(
            id=new_id("question"),
            text=f"{item.label}について、利用者の立場でどう決めたいですか？",
            reason="業務に必要な前提がまだ固まっていないためです。",
            priority=self._priority(item),
            target_unknown_ids=[item.id],
        )

    def _priority(self, item: MemoryItem) -> QuestionPriority:
        if item.source == MemorySource.SIMULATION:
            return QuestionPriority.HIGH
        if "条件" in item.label or "基準" in item.label:
            return QuestionPriority.HIGH
        return QuestionPriority.MEDIUM

    def _select(self, candidates: list[Question]) -> Question | None:
        if not candidates:
            return None
        order = {
            QuestionPriority.HIGH: 0,
            QuestionPriority.MEDIUM: 1,
            QuestionPriority.LOW: 2,
        }
        return sorted(candidates, key=lambda question: (order[question.priority], question.text))[0]


class LLMQuestionGenerator:
    def __init__(
        self,
        provider: LLMProvider,
        fallback: RuleBasedQuestionGenerator | None = None,
    ) -> None:
        self.provider = provider
        self.fallback = fallback or RuleBasedQuestionGenerator()

    def generate(
        self,
        memory: ProjectMemory,
        domain_model: DomainModel,
        simulation_result: SimulationResult | None = None,
    ) -> QuestionSet:
        system_prompt = load_prompt("question_generator.md")
        simulation_json = simulation_result.model_dump_json(indent=2) if simulation_result else "null"
        user_prompt = (
            "Return JSON only matching the QuestionSet schema.\n"
            "The selected question must be business-friendly and explain why the information is needed.\n"
            f"Project memory:\n{memory.model_dump_json(indent=2)}\n"
            f"Domain model:\n{domain_model.model_dump_json(indent=2)}\n"
            f"Simulation result:\n{simulation_json}\n"
        )
        try:
            payload = extract_json_object(self.provider.invoke(system_prompt, user_prompt))
            if not isinstance(payload, dict):
                raise ValueError("Question generator response must be a JSON object")
            return QuestionSet.model_validate(payload)
        except Exception:
            return self.fallback.generate(memory, domain_model, simulation_result)


QuestionGenerator = RuleBasedQuestionGenerator
