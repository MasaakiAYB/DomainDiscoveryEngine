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
            constraints = [item.label for item in source.constraints]
            rules = [item.label for item in source.rules]
            criteria = [item.label for item in source.decision_criteria]
            procedures = [item.label for item in source.procedures]
            inputs = source.input_outputs
        else:
            existing = []
            tasks = source.tasks
            constraints = [item.label for item in source.constraints]
            rules = [item.label for item in source.business_rules]
            criteria = [item.label for item in source.decision_criteria]
            procedures = [item.label for item in source.procedures]
            inputs = source.input_outputs

        candidates = list(existing)
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
                    required_rules=rules,
                    required_decision_criteria=criteria,
                    required_procedures=procedures,
                    status=MemoryStatus.CANDIDATE,
                    source=MemorySource.AI_INFERRED,
                    evidence="derived from tasks and business capability knowledge",
                    confidence=0.6,
                )
            )
        return candidates

    def _match_io(self, label: str, io_specs) -> object | None:
        for item in io_specs:
            item_label = getattr(item, "label", "")
            if item_label and (item_label in label or label in item_label):
                return item
        return None


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
            "Return JSON only as a list of ExecutableTaskCandidate objects.\n"
            f"Source model:\n{payload_json}\n"
        )
        try:
            payload = extract_json_object(self.provider.invoke(system_prompt, user_prompt))
            if not isinstance(payload, list):
                raise ValueError("Task candidate extractor response must be a JSON list")
            return [ExecutableTaskCandidate.model_validate(item) for item in payload]
        except Exception:
            return self.fallback.extract(source)
