from __future__ import annotations

from domain_discovery_engine.llm.provider import LLMProvider
from domain_discovery_engine.schemas.extraction import DialogueExtraction
from domain_discovery_engine.schemas.memory import (
    MemoryItem,
    MemoryItemType,
    MemorySource,
    MemoryStatus,
    ProjectMemory,
)
from domain_discovery_engine.utils.ids import new_id
from domain_discovery_engine.utils.json import extract_json_object
from domain_discovery_engine.utils.prompts import load_prompt


class RuleBasedDialogueAnalyzer:
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

        if "評価" in stripped and "見積" in stripped:
            extraction.tasks.append(
                self._item(MemoryItemType.TASK, "見積候補を評価する", MemorySource.USER, stripped)
            )
            extraction.executable_task_candidates.append(
                self._item(
                    MemoryItemType.EXECUTABLE_TASK_CANDIDATE,
                    "見積候補を評価する",
                    MemorySource.AI_INFERRED,
                    stripped,
                    description="task_type:unknown",
                )
            )
        if "レビュー対象" in stripped:
            extraction.executable_task_candidates.append(
                self._item(
                    MemoryItemType.EXECUTABLE_TASK_CANDIDATE,
                    "レビュー対象を抽出する",
                    MemorySource.AI_INFERRED,
                    stripped,
                    description="task_type:unknown",
                )
            )
            extraction.business_rules.append(
                self._item(
                    MemoryItemType.BUSINESS_RULE,
                    "判断が難しいものはレビュー対象にする",
                    MemorySource.USER,
                    stripped,
                    description="rule_type:exception",
                )
            )
        if "対象外" in stripped and "除外" in stripped:
            extraction.business_rules.append(
                self._item(
                    MemoryItemType.BUSINESS_RULE,
                    "対象外候補は除外する",
                    MemorySource.USER,
                    stripped,
                    description="rule_type:eligibility",
                )
            )
        for criterion in ("仕様一致", "単位整合", "過去実績との差分", "単価"):
            if criterion in stripped:
                extraction.decision_criteria.append(
                    self._item(
                        MemoryItemType.DECISION_CRITERION,
                        criterion,
                        MemorySource.USER,
                        stripped,
                        description="criterion_type:evaluation",
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


class LLMDialogueAnalyzer:
    def __init__(
        self,
        provider: LLMProvider,
        fallback: RuleBasedDialogueAnalyzer | None = None,
    ) -> None:
        self.provider = provider
        self.fallback = fallback or RuleBasedDialogueAnalyzer()

    def analyze(self, message: str, memory: ProjectMemory) -> DialogueExtraction:
        system_prompt = load_prompt("internal", "dialogue_analyzer.md")
        user_prompt = (
            "Return JSON only.\n"
            "Schema keys: goals, concepts, tasks, constraints, assumptions, unknowns.\n"
            "Additional schema keys: business_rules, decision_criteria, procedures, input_outputs, executable_task_candidates.\n"
            "Each item may include label, description, source, status, confidence, evidence.\n"
            f"Current memory:\n{memory.model_dump_json(indent=2)}\n"
            f"User message:\n{message}\n"
        )
        try:
            payload = extract_json_object(self.provider.invoke(system_prompt, user_prompt))
            if not isinstance(payload, dict):
                raise ValueError("Dialogue analyzer response must be a JSON object")
            return DialogueExtraction(
                goals=self._build_items(payload.get("goals", []), MemoryItemType.GOAL, message),
                concepts=self._build_items(payload.get("concepts", []), MemoryItemType.CONCEPT, message),
                tasks=self._build_items(payload.get("tasks", []), MemoryItemType.TASK, message),
                constraints=self._build_items(
                    payload.get("constraints", []), MemoryItemType.CONSTRAINT, message
                ),
                assumptions=self._build_items(
                    payload.get("assumptions", []), MemoryItemType.ASSUMPTION, message
                ),
                business_rules=self._build_items(
                    payload.get("business_rules", []), MemoryItemType.BUSINESS_RULE, message
                ),
                decision_criteria=self._build_items(
                    payload.get("decision_criteria", []), MemoryItemType.DECISION_CRITERION, message
                ),
                procedures=self._build_items(
                    payload.get("procedures", []), MemoryItemType.PROCEDURE, message
                ),
                input_outputs=self._build_items(
                    payload.get("input_outputs", []), MemoryItemType.INPUT_OUTPUT, message
                ),
                executable_task_candidates=self._build_items(
                    payload.get("executable_task_candidates", []),
                    MemoryItemType.EXECUTABLE_TASK_CANDIDATE,
                    message,
                ),
                unknowns=self._build_items(payload.get("unknowns", []), MemoryItemType.UNKNOWN, message),
            )
        except Exception:
            return self.fallback.analyze(message, memory)

    def _build_items(
        self,
        raw_items: list[dict] | list[str],
        item_type: MemoryItemType,
        evidence: str,
    ) -> list[MemoryItem]:
        items: list[MemoryItem] = []
        for raw_item in raw_items:
            if isinstance(raw_item, str):
                raw_item = {"label": raw_item}
            source = MemorySource(raw_item.get("source", MemorySource.AI_INFERRED.value))
            default_status = (
                MemoryStatus.UNRESOLVED.value if item_type == MemoryItemType.UNKNOWN else MemoryStatus.CANDIDATE.value
            )
            items.append(
                MemoryItem(
                    id=raw_item.get("id", new_id(item_type.value)),
                    type=item_type,
                    label=raw_item["label"],
                    description=raw_item.get("description", ""),
                    status=MemoryStatus(raw_item.get("status", default_status)),
                    confidence=float(raw_item.get("confidence", 0.7)),
                    source=source,
                    evidence=raw_item.get("evidence", evidence),
                )
            )
        return items


DialogueAnalyzer = RuleBasedDialogueAnalyzer
