from __future__ import annotations

from domain_discovery_engine.schemas.business_capability import BusinessCapabilityModel, ExecutableTaskCandidate
from domain_discovery_engine.schemas.memory import MemorySource, MemoryStatus, ProjectMemory
from domain_discovery_engine.utils.ids import new_id
from domain_discovery_engine.utils.json import extract_json_object
from domain_discovery_engine.utils.prompts import load_prompt
from domain_discovery_engine.llm.provider import LLMProvider


class RuleBasedTaskCandidateExtractor:
    def extract(
        self,
        source: ProjectMemory | BusinessCapabilityModel,
    ) -> list[ExecutableTaskCandidate]:
        if isinstance(source, BusinessCapabilityModel):
            existing = list(source.executable_task_candidates)
            tasks = source.tasks
            constraints = [{"id": item.id, "label": item.label, "description": item.description} for item in source.constraints]
            rules = [{"id": item.id, "label": item.label, "description": item.description} for item in source.rules]
            criteria = [{"id": item.id, "label": item.label, "description": item.description} for item in source.decision_criteria]
            procedures = [{"id": item.id, "label": item.label, "description": item.description} for item in source.procedures]
            inputs = source.input_outputs
        else:
            existing = []
            tasks = source.tasks
            constraints = [{"id": item.id, "label": item.label, "description": item.description} for item in source.constraints]
            rules = [{"id": item.id, "label": item.label, "description": item.description} for item in source.business_rules]
            criteria = [{"id": item.id, "label": item.label, "description": item.description} for item in source.decision_criteria]
            procedures = [{"id": item.id, "label": item.label, "description": item.description} for item in source.procedures]
            inputs = source.input_outputs

        candidates = [self._enrich_candidate(item, tasks, rules, criteria, procedures, constraints, inputs) for item in existing]
        for task in tasks:
            label = getattr(task, "name", None) or getattr(task, "label", "")
            if not label:
                continue
            if not (rules or criteria or procedures or constraints):
                continue
            if any(item.label == label for item in candidates):
                continue
            io_spec = self._match_io(label, inputs)
            candidates.append(
                ExecutableTaskCandidate(
                    id=new_id("task_candidate"),
                    label=label,
                    description="",
                    task_type="unknown",
                    required_inputs=getattr(io_spec, "input_items", []),
                    expected_outputs=getattr(io_spec, "output_items", []),
                    required_rules=self._collect_related_ids(label, "", rules, len(tasks)),
                    required_decision_criteria=self._collect_related_ids(label, "", criteria, len(tasks)),
                    required_procedures=self._collect_related_ids(label, "", procedures, len(tasks)),
                    status=MemoryStatus.CANDIDATE,
                    source=MemorySource.AI_INFERRED,
                    evidence="derived from tasks and business capability knowledge",
                    confidence=0.6,
                )
            )
        return candidates

    def _enrich_candidate(self, candidate, tasks, rules, criteria, procedures, constraints, inputs):
        task_context = self._find_task_context(candidate.label, tasks)
        task_label = task_context.get("label", candidate.label)
        task_description = task_context.get("description", candidate.description)
        io_spec = self._match_io(task_label, inputs)
        return ExecutableTaskCandidate(
            id=candidate.id,
            label=candidate.label,
            description=candidate.description,
            task_type=candidate.task_type,
            required_inputs=candidate.required_inputs or getattr(io_spec, "input_items", []),
            expected_outputs=candidate.expected_outputs or getattr(io_spec, "output_items", []),
            required_rules=candidate.required_rules or self._collect_related_ids(task_label, task_description, rules, len(tasks)),
            required_decision_criteria=candidate.required_decision_criteria
            or self._collect_related_ids(task_label, task_description, criteria, len(tasks)),
            required_procedures=candidate.required_procedures
            or self._collect_related_ids(task_label, task_description, procedures, len(tasks)),
            status=candidate.status,
            source=candidate.source,
            evidence=candidate.evidence,
            confidence=candidate.confidence,
        )

    def _match_io(self, label: str, io_specs) -> object | None:
        for item in io_specs:
            item_label = getattr(item, "label", "")
            if item_label and (item_label in label or label in item_label):
                return item
        return None

    def _find_task_context(self, candidate_label: str, tasks) -> dict[str, str]:
        for task in tasks:
            label = getattr(task, "name", None) or getattr(task, "label", "")
            description = getattr(task, "description", "")
            if candidate_label == label:
                return {"label": label, "description": description}
        return {"label": candidate_label, "description": ""}

    def _collect_related_ids(
        self,
        task_label: str,
        task_description: str,
        items: list[dict[str, str]],
        task_count: int,
    ) -> list[str]:
        if not items:
            return []
        if len(items) == 1 and task_count == 1:
            return [items[0]["id"]]
        related: list[str] = []
        for item in items:
            if self._is_relevant(task_label, task_description, item["label"], item.get("description", "")):
                related.append(item["id"])
        return related

    def _is_relevant(self, task_label: str, task_description: str, item_label: str, item_description: str) -> bool:
        task_text = f"{task_label} {task_description}".strip()
        item_text = f"{item_label} {item_description}".strip()
        if not task_text or not item_text:
            return False
        if item_label in task_text or task_label in item_text:
            return True
        task_keywords = self._keywords(task_text)
        item_keywords = self._keywords(item_text)
        return bool(task_keywords & item_keywords)

    def _keywords(self, text: str) -> set[str]:
        parts = text.replace("、", " ").replace("。", " ").replace("・", " ").replace("/", " ").split()
        keywords = {part for part in parts if len(part) >= 2}
        for part in parts or [text]:
            if len(part) >= 2:
                keywords.update({part[i : i + 2] for i in range(len(part) - 1)})
        if not keywords and len(text) >= 2:
            keywords = {text[i : i + 2] for i in range(len(text) - 1)}
        return keywords


class LLMTaskCandidateExtractor:
    def __init__(
        self,
        provider: LLMProvider,
        fallback: RuleBasedTaskCandidateExtractor | None = None,
    ) -> None:
        self.provider = provider
        self.fallback = fallback or RuleBasedTaskCandidateExtractor()

    def extract(
        self,
        source: ProjectMemory | BusinessCapabilityModel,
    ) -> list[ExecutableTaskCandidate]:
        system_prompt = load_prompt("internal", "task_candidate_extractor.md")
        if isinstance(source, BusinessCapabilityModel):
            payload_json = source.model_dump_json(indent=2)
        else:
            payload_json = source.model_dump_json(indent=2)
        user_prompt = (
            'Return JSON only as an object with key "items".\n'
            f"Source model:\n{payload_json}\n"
        )
        try:
            payload = extract_json_object(self.provider.invoke(system_prompt, user_prompt))
            if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
                raise ValueError('Task candidate extractor response must be a JSON object with key "items"')
            return [ExecutableTaskCandidate.model_validate(item) for item in payload["items"]]
        except Exception:
            return self.fallback.extract(source)
