from __future__ import annotations

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


class SimulationTester:
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
                known_texts, ("検索条件", "検索キー", "予約に必要な入力項目", "条件")
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
                if not self._contains_any(known_texts, ("入力項目", "設備名", "利用者", "開始時刻", "終了時刻")):
                    result.findings.append(
                        self._finding("reservation-input", task_name, "予約に必要な入力項目")
                    )
                    result.unknowns.append(self._unknown("予約に必要な入力項目", task_name))
                    known_texts.add("予約に必要な入力項目")

        return result

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
