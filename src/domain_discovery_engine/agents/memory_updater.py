from __future__ import annotations

from domain_discovery_engine.schemas.memory import (
    MemoryItem,
    MemoryItemType,
    MemorySource,
    MemoryStatus,
    ProjectMemory,
)


class MemoryUpdater:
    def merge_items(self, memory: ProjectMemory, items: list[MemoryItem]) -> ProjectMemory:
        for item in items:
            target = self._target_list(memory, item.type)
            existing = self._find_equivalent(target, item.label)
            if existing is None:
                target.append(item.model_copy(deep=True))
                continue

            if self._preserve_user_confirmed(existing, item):
                existing.evidence = self._merge_text(existing.evidence, item.evidence)
                existing.confidence = max(existing.confidence, item.confidence)
                existing.related_item_ids = self._merge_related_ids(existing, item)
                continue

            existing.description = existing.description or item.description
            existing.evidence = self._merge_text(existing.evidence, item.evidence)
            existing.confidence = max(existing.confidence, item.confidence)
            existing.related_item_ids = self._merge_related_ids(existing, item)
            existing.status = self._select_status(existing.status, item.status)
            existing.source = self._select_source(existing.source, item.source)
        return memory

    def _target_list(self, memory: ProjectMemory, item_type: MemoryItemType) -> list[MemoryItem]:
        mapping = {
            MemoryItemType.GOAL: memory.goals,
            MemoryItemType.CONCEPT: memory.concepts,
            MemoryItemType.TASK: memory.tasks,
            MemoryItemType.RELATION: memory.relations,
            MemoryItemType.CONSTRAINT: memory.constraints,
            MemoryItemType.ASSUMPTION: memory.assumptions,
            MemoryItemType.DECISION: memory.decisions,
            MemoryItemType.BUSINESS_RULE: memory.business_rules,
            MemoryItemType.DECISION_CRITERION: memory.decision_criteria,
            MemoryItemType.PROCEDURE: memory.procedures,
            MemoryItemType.INPUT_OUTPUT: memory.input_outputs,
            MemoryItemType.EXECUTABLE_TASK_CANDIDATE: memory.executable_task_candidates,
            MemoryItemType.UNKNOWN: memory.unknowns,
            MemoryItemType.REJECTED: memory.rejected_items,
            MemoryItemType.CONTRADICTION: memory.contradictions,
        }
        return mapping[item_type]

    def _find_equivalent(self, items: list[MemoryItem], label: str) -> MemoryItem | None:
        normalized = self._normalize(label)
        for item in items:
            if self._normalize(item.label) == normalized:
                return item
        return None

    def _normalize(self, value: str) -> str:
        return "".join(value.lower().split())

    def _preserve_user_confirmed(self, existing: MemoryItem, incoming: MemoryItem) -> bool:
        return (
            existing.source == MemorySource.USER
            and existing.status == MemoryStatus.CONFIRMED
            and incoming.source == MemorySource.AI_INFERRED
            and incoming.status != MemoryStatus.CONFIRMED
        )

    def _select_status(self, current: MemoryStatus, incoming: MemoryStatus) -> MemoryStatus:
        priority = {
            MemoryStatus.CONFIRMED: 3,
            MemoryStatus.UNRESOLVED: 2,
            MemoryStatus.CANDIDATE: 1,
            MemoryStatus.REJECTED: 0,
        }
        return current if priority[current] >= priority[incoming] else incoming

    def _select_source(self, current: MemorySource, incoming: MemorySource) -> MemorySource:
        priority = {
            MemorySource.USER: 3,
            MemorySource.SIMULATION: 2,
            MemorySource.AI_INFERRED: 1,
        }
        return current if priority[current] >= priority[incoming] else incoming

    def _merge_text(self, current: str, incoming: str) -> str:
        if not incoming or incoming == current:
            return current
        if not current:
            return incoming
        return f"{current}\n{incoming}"

    def _merge_related_ids(self, current: MemoryItem, incoming: MemoryItem) -> list[str]:
        return list(dict.fromkeys([*current.related_item_ids, *incoming.related_item_ids]))
