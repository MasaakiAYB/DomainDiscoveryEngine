from __future__ import annotations

from domain_discovery_engine.llm.provider import LLMProvider
from domain_discovery_engine.schemas.domain_model import (
    DomainConcept,
    DomainConstraint,
    DomainModel,
    DomainModelItemStatus,
    DomainRelation,
    DomainTask,
)
from domain_discovery_engine.schemas.memory import MemoryItem, MemoryStatus, ProjectMemory
from domain_discovery_engine.utils.json import extract_json_object
from domain_discovery_engine.utils.prompts import load_prompt


class RuleBasedDomainModelBuilder:
    def build(self, memory: ProjectMemory) -> DomainModel:
        model = DomainModel(
            project_id=memory.project_id,
            title=memory.title,
            purpose=[item.label for item in memory.goals if item.status != MemoryStatus.REJECTED],
            concepts=[self._concept(item) for item in memory.concepts if item.status != MemoryStatus.REJECTED],
            relations=[
                self._relation(item) for item in memory.relations if item.status != MemoryStatus.REJECTED
            ],
            tasks=[self._task(item) for item in memory.tasks if item.status != MemoryStatus.REJECTED],
            constraints=[
                self._constraint(item) for item in memory.constraints if item.status != MemoryStatus.REJECTED
            ],
            assumptions=[item.label for item in memory.assumptions if item.status != MemoryStatus.REJECTED],
            decisions=[item.label for item in memory.decisions if item.status != MemoryStatus.REJECTED],
            unresolved_questions=[
                item.label for item in memory.unknowns if item.status == MemoryStatus.UNRESOLVED
            ],
        )
        self._add_default_relations(model)
        self._add_default_descriptions(model)
        return model

    def _concept(self, item: MemoryItem) -> DomainConcept:
        return DomainConcept(
            id=item.id,
            name=item.label,
            description=item.description,
            status=self._status(item.status),
            source_memory_item_ids=[item.id],
        )

    def _relation(self, item: MemoryItem) -> DomainRelation:
        subject, predicate, obj = self._parse_relation(item.label)
        return DomainRelation(
            id=item.id,
            subject=subject,
            predicate=predicate,
            object=obj,
            description=item.description,
            status=self._status(item.status),
            source_memory_item_ids=[item.id],
        )

    def _task(self, item: MemoryItem) -> DomainTask:
        return DomainTask(
            id=item.id,
            name=item.label,
            description=item.description,
            status=self._status(item.status),
            source_memory_item_ids=[item.id],
        )

    def _constraint(self, item: MemoryItem) -> DomainConstraint:
        return DomainConstraint(
            id=item.id,
            label=item.label,
            description=item.description,
            status=self._status(item.status),
            source_memory_item_ids=[item.id],
        )

    def _status(self, status: MemoryStatus) -> DomainModelItemStatus:
        mapping = {
            MemoryStatus.CANDIDATE: DomainModelItemStatus.CANDIDATE,
            MemoryStatus.CONFIRMED: DomainModelItemStatus.CONFIRMED,
            MemoryStatus.UNRESOLVED: DomainModelItemStatus.UNRESOLVED,
            MemoryStatus.REJECTED: DomainModelItemStatus.CANDIDATE,
        }
        return mapping[status]

    def _parse_relation(self, label: str) -> tuple[str, str, str]:
        parts = label.split("|")
        if len(parts) == 3:
            return parts[0], parts[1], parts[2]
        return label, "関連する", ""

    def _add_default_relations(self, model: DomainModel) -> None:
        existing = {(item.subject, item.predicate, item.object) for item in model.relations}
        concept_names = {concept.name for concept in model.concepts}
        if {"実験", "実験条件"} <= concept_names and ("実験", "持つ", "実験条件") not in existing:
            model.relations.append(
                DomainRelation(
                    id="derived_relation_experiment_condition",
                    subject="実験",
                    predicate="持つ",
                    object="実験条件",
                    status=DomainModelItemStatus.CANDIDATE,
                )
            )
        if {"実験", "実験結果"} <= concept_names and ("実験", "生み出す", "実験結果") not in existing:
            model.relations.append(
                DomainRelation(
                    id="derived_relation_experiment_result",
                    subject="実験",
                    predicate="生み出す",
                    object="実験結果",
                    status=DomainModelItemStatus.CANDIDATE,
                )
            )
        if {"利用者", "予約"} <= concept_names and ("利用者", "作成する", "予約") not in existing:
            model.relations.append(
                DomainRelation(
                    id="derived_relation_user_reservation",
                    subject="利用者",
                    predicate="作成する",
                    object="予約",
                    status=DomainModelItemStatus.CANDIDATE,
                )
            )
        if {"予約", "設備"} <= concept_names and ("予約", "対象にする", "設備") not in existing:
            model.relations.append(
                DomainRelation(
                    id="derived_relation_reservation_equipment",
                    subject="予約",
                    predicate="対象にする",
                    object="設備",
                    status=DomainModelItemStatus.CANDIDATE,
                )
            )

    def _add_default_descriptions(self, model: DomainModel) -> None:
        descriptions = {
            "実験": "条件と結果を持つ業務単位",
            "実験条件": "実験時に設定する条件",
            "実験結果": "実験から得られる結果",
            "設備": "予約対象となる共通設備",
            "予約": "利用者が設備を特定時間帯に利用する予定",
            "利用者": "設備を予約・利用する部署メンバー",
        }
        for concept in model.concepts:
            if not concept.description and concept.name in descriptions:
                concept.description = descriptions[concept.name]


class LLMDomainModelBuilder:
    def __init__(
        self,
        provider: LLMProvider,
        fallback: RuleBasedDomainModelBuilder | None = None,
    ) -> None:
        self.provider = provider
        self.fallback = fallback or RuleBasedDomainModelBuilder()

    def build(self, memory: ProjectMemory) -> DomainModel:
        system_prompt = load_prompt("internal", "domain_model_builder.md")
        user_prompt = (
            "Return JSON only matching the DomainModel schema.\n"
            f"Project memory:\n{memory.model_dump_json(indent=2)}\n"
        )
        try:
            payload = extract_json_object(self.provider.invoke(system_prompt, user_prompt))
            if not isinstance(payload, dict):
                raise ValueError("Domain model builder response must be a JSON object")
            payload.setdefault("project_id", memory.project_id)
            payload.setdefault("title", memory.title)
            return DomainModel.model_validate(payload)
        except Exception:
            return self.fallback.build(memory)


DomainModelBuilder = RuleBasedDomainModelBuilder
