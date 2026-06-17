from __future__ import annotations

from domain_discovery_engine.schemas.extraction import DialogueExtraction
from domain_discovery_engine.schemas.memory import (
    MemoryItem,
    MemoryItemType,
    MemorySource,
    MemoryStatus,
    ProjectMemory,
)
from domain_discovery_engine.utils.ids import new_id


class DialogueAnalyzer:
    def analyze(self, message: str, memory: ProjectMemory) -> DialogueExtraction:
        del memory
        extraction = DialogueExtraction()
        stripped = message.strip()

        if "実験条件" in stripped:
            extraction.concepts.append(
                self._item(MemoryItemType.CONCEPT, "実験条件", MemorySource.USER, stripped)
            )
        if "結果" in stripped:
            extraction.concepts.append(
                self._item(MemoryItemType.CONCEPT, "実験結果", MemorySource.USER, stripped)
            )
        if "実験" in stripped:
            extraction.concepts.append(
                self._item(
                    MemoryItemType.CONCEPT,
                    "実験",
                    MemorySource.AI_INFERRED,
                    stripped,
                    description="条件と結果を持つ業務単位",
                )
            )
        if "記録" in stripped:
            label = "実験条件と結果を記録する" if "実験条件" in stripped and "結果" in stripped else "記録する"
            extraction.tasks.append(self._item(MemoryItemType.TASK, label, MemorySource.USER, stripped))
        if "探せるようにしたい" in stripped or "探す" in stripped:
            extraction.goals.append(
                self._item(
                    MemoryItemType.GOAL,
                    "過去の似た実験を探せるようにする",
                    MemorySource.USER,
                    stripped,
                )
            )
            extraction.tasks.append(
                self._item(MemoryItemType.TASK, "過去の似た実験を探す", MemorySource.USER, stripped)
            )
        if "似た実験" in stripped:
            extraction.unknowns.append(
                self._item(
                    MemoryItemType.UNKNOWN,
                    "似た実験の判定基準",
                    MemorySource.AI_INFERRED,
                    stripped,
                    status=MemoryStatus.UNRESOLVED,
                )
            )

        if "設備" in stripped:
            extraction.concepts.append(
                self._item(MemoryItemType.CONCEPT, "設備", MemorySource.USER, stripped)
            )
        if "予約" in stripped:
            extraction.concepts.append(
                self._item(MemoryItemType.CONCEPT, "予約", MemorySource.AI_INFERRED, stripped)
            )
            extraction.tasks.append(
                self._item(MemoryItemType.TASK, "設備を予約する", MemorySource.USER, stripped)
            )
        if "部署" in stripped or "メンバー" in stripped:
            extraction.concepts.append(
                self._item(MemoryItemType.CONCEPT, "利用者", MemorySource.AI_INFERRED, stripped)
            )
            extraction.goals.append(
                self._item(
                    MemoryItemType.GOAL,
                    "部署メンバーが共通設備を予約できるようにする",
                    MemorySource.USER,
                    stripped,
                )
            )
        if "ダブルブッキング" in stripped:
            extraction.goals.append(
                self._item(MemoryItemType.GOAL, "ダブルブッキングを防ぐ", MemorySource.USER, stripped)
            )
            extraction.constraints.append(
                self._item(
                    MemoryItemType.CONSTRAINT,
                    "同じ設備は同じ時間帯に重複予約できない",
                    MemorySource.USER,
                    stripped,
                )
            )

        return extraction

    def _item(
        self,
        item_type: MemoryItemType,
        label: str,
        source: MemorySource,
        evidence: str,
        *,
        status: MemoryStatus = MemoryStatus.CANDIDATE,
        description: str = "",
    ) -> MemoryItem:
        return MemoryItem(
            id=new_id(item_type.value),
            type=item_type,
            label=label,
            description=description,
            status=status,
            confidence=0.8 if source == MemorySource.USER else 0.6,
            source=source,
            evidence=evidence,
        )
