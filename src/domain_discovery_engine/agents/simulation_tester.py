from __future__ import annotations

from domain_discovery_engine.llm.provider import LLMProvider
from domain_discovery_engine.schemas.domain_model import DomainModel
from domain_discovery_engine.schemas.memory import (
    MemoryItem,
    MemoryItemType,
    MemorySource,
    MemoryStatus,
    ProjectMemory,
)
from domain_discovery_engine.schemas.simulation import SimulationFinding, SimulationResult
from domain_discovery_engine.utils.ids import new_id
from domain_discovery_engine.utils.json import extract_json_object
from domain_discovery_engine.utils.prompts import load_prompt


class RuleBasedSimulationTester:
    def run(self, domain_model: DomainModel, memory: ProjectMemory) -> SimulationResult:
        result = SimulationResult()
        known_texts = {
            *domain_model.unresolved_questions,
            *[item.label for item in memory.unknowns],
            *[item.label for item in memory.constraints],
            *[item.label for item in memory.decisions],
            *[item.name for item in domain_model.concepts],
        }

        for task in domain_model.tasks:
            task_name = task.name
            if any(word in task_name for word in ("探す", "検索", "search")) and not self._contains_any(
                known_texts, ("検索条件", "検索キー")
            ):
                result.findings.append(self._finding("search", task_name, "検索条件が未定義"))
                result.unknowns.append(self._unknown("検索条件が未定義", task_name))
                known_texts.add("検索条件が未定義")

            if any(word in task_name for word in ("似た", "類似")) and not self._contains_any(
                known_texts, ("類似", "似た実験の判定基準", "類似判定基準")
            ):
                result.findings.append(self._finding("similarity", task_name, "類似判定基準が未定義"))
                result.unknowns.append(self._unknown("類似判定基準が未定義", task_name))
                known_texts.add("類似判定基準が未定義")

            if "予約" in task_name:
                if not self._contains_any(known_texts, ("時間", "時刻", "日付")):
                    result.findings.append(self._finding("reservation-time", task_name, "予約時間帯が未定義"))
                    result.unknowns.append(self._unknown("予約時間帯が未定義", task_name))
                    known_texts.add("予約時間帯が未定義")
                if not self._contains_any(known_texts, ("重複予約", "ダブルブッキング", "重複")):
                    result.findings.append(
                        self._finding("reservation-duplicate", task_name, "重複予約防止ルールが未定義")
                    )
                    result.unknowns.append(self._unknown("重複予約防止ルールが未定義", task_name))
                    known_texts.add("重複予約防止ルールが未定義")
                if "予約に必要な入力項目" not in known_texts:
                    result.findings.append(self._finding("reservation-input", task_name, "予約に必要な入力項目"))
                    result.unknowns.append(self._unknown("予約に必要な入力項目", task_name))
                    known_texts.add("予約に必要な入力項目")

        for candidate in memory.executable_task_candidates:
            self._check_task_candidate(candidate.label, memory, result)

        return result

    def _check_task_candidate(self, label: str, memory: ProjectMemory, result: SimulationResult) -> None:
        if "評価" in label:
            if not memory.input_outputs:
                result.findings.append(self._finding("candidate-input", label, "評価に必要な入力情報が未定義"))
                result.unknowns.append(self._unknown("評価に必要な入力情報が未定義", label))
            if not memory.decision_criteria:
                result.findings.append(self._finding("candidate-criteria", label, "評価の判断基準が未定義"))
                result.unknowns.append(self._unknown("評価の判断基準が未定義", label))
            if not memory.business_rules:
                result.findings.append(self._finding("candidate-rules", label, "評価時の業務ルールが未定義"))
                result.unknowns.append(self._unknown("評価時の業務ルールが未定義", label))
        if "レビュー対象" in label and not any("レビュー" in item.label or "閾値" in item.label for item in memory.business_rules + memory.unknowns):
            result.findings.append(self._finding("review-threshold", label, "レビュー対象とする閾値が未定義"))
            result.unknowns.append(self._unknown("レビュー対象とする閾値が未定義", label))

        if any(item.label == "仕様一致" for item in memory.decision_criteria) and not any(
            "仕様一致" in item.label for item in memory.unknowns
        ):
            result.findings.append(self._finding("spec-match", label, "仕様一致の判定基準が未定義"))
            result.unknowns.append(self._unknown("仕様一致の判定基準が未定義", label))
        if any(item.label == "単位整合" for item in memory.decision_criteria) and not any(
            "単位換算可能" in item.label or "単位整合" in item.label for item in memory.unknowns
        ):
            result.findings.append(self._finding("unit-match", label, "単位換算可能と判断する条件が未定義"))
            result.unknowns.append(self._unknown("単位換算可能と判断する条件が未定義", label))

    def _contains_any(self, texts: set[str], keywords: tuple[str, ...]) -> bool:
        return any(keyword in text for text in texts for keyword in keywords)

    def _unknown(self, label: str, related_task: str) -> MemoryItem:
        return MemoryItem(
            id=new_id("unknown"),
            type=MemoryItemType.UNKNOWN,
            label=label,
            status=MemoryStatus.UNRESOLVED,
            confidence=0.7,
            source=MemorySource.SIMULATION,
            evidence=f"simulation:{related_task}",
        )

    def _finding(self, scenario: str, task_name: str, message: str) -> SimulationFinding:
        unknown = self._unknown(message, task_name)
        return SimulationFinding(
            id=new_id("finding"),
            scenario=scenario,
            finding_type="missing_info",
            message=message,
            related_task=task_name,
            generated_unknown=unknown,
        )


class LLMSimulationTester:
    def __init__(
        self,
        provider: LLMProvider,
        fallback: RuleBasedSimulationTester | None = None,
    ) -> None:
        self.provider = provider
        self.fallback = fallback or RuleBasedSimulationTester()

    def run(self, domain_model: DomainModel, memory: ProjectMemory) -> SimulationResult:
        system_prompt = load_prompt("internal", "simulation_tester.md")
        user_prompt = (
            "Return JSON only matching the SimulationResult schema.\n"
            "Use finding_type values such as missing_info, contradiction, risk.\n"
            "Test business capability completeness for executable task candidates as well.\n"
            f"Domain model:\n{domain_model.model_dump_json(indent=2)}\n"
            f"Project memory:\n{memory.model_dump_json(indent=2)}\n"
        )
        try:
            payload = extract_json_object(self.provider.invoke(system_prompt, user_prompt))
            if not isinstance(payload, dict):
                raise ValueError("Simulation tester response must be a JSON object")
            return SimulationResult.model_validate(payload)
        except Exception:
            return self.fallback.run(domain_model, memory)


SimulationTester = RuleBasedSimulationTester
