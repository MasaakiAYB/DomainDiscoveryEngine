from __future__ import annotations

from domain_discovery_engine.agents.domain_model_builder import (
    LLMDomainModelBuilder,
    RuleBasedDomainModelBuilder,
)
from domain_discovery_engine.llm.provider import LLMProvider
from domain_discovery_engine.schemas.business_capability import (
    BusinessCapabilityModel,
    BusinessProcedure,
    BusinessRule,
    DecisionCriterion,
    ExecutableTaskCandidate,
    InputOutputSpec,
)
from domain_discovery_engine.schemas.memory import MemoryItem, ProjectMemory
from domain_discovery_engine.utils.json import extract_json_object
from domain_discovery_engine.utils.prompts import load_prompt


class RuleBasedBusinessCapabilityBuilder:
    def __init__(self) -> None:
        self.domain_model_builder = RuleBasedDomainModelBuilder()

    def build(self, memory: ProjectMemory) -> BusinessCapabilityModel:
        domain_model = self.domain_model_builder.build(memory)
        return BusinessCapabilityModel(
            purpose=[item.label for item in memory.goals],
            concepts=domain_model.concepts,
            tasks=domain_model.tasks,
            rules=[self._rule(item) for item in memory.business_rules],
            decision_criteria=[self._criterion(item) for item in memory.decision_criteria],
            procedures=[self._procedure(item) for item in memory.procedures],
            input_outputs=[self._input_output(item) for item in memory.input_outputs],
            constraints=domain_model.constraints,
            executable_task_candidates=[self._task_candidate(item) for item in memory.executable_task_candidates],
            unknowns=[item.label for item in memory.unknowns],
        )

    def _rule(self, item: MemoryItem) -> BusinessRule:
        return BusinessRule(
            id=item.id,
            label=item.label,
            description=item.description,
            rule_type=self._metadata_value(item, "rule_type", "validation"),
            status=item.status,
            source=item.source,
            evidence=item.evidence or None,
            confidence=item.confidence,
        )

    def _criterion(self, item: MemoryItem) -> DecisionCriterion:
        return DecisionCriterion(
            id=item.id,
            label=item.label,
            description=item.description,
            criterion_type=self._metadata_value(item, "criterion_type", "evaluation"),
            status=item.status,
            source=item.source,
            evidence=item.evidence or None,
            confidence=item.confidence,
        )

    def _procedure(self, item: MemoryItem) -> BusinessProcedure:
        return BusinessProcedure(
            id=item.id,
            label=item.label,
            description=item.description,
            steps=self._list_metadata_value(item, "steps"),
            status=item.status,
            source=item.source,
            evidence=item.evidence or None,
            confidence=item.confidence,
        )

    def _input_output(self, item: MemoryItem) -> InputOutputSpec:
        return InputOutputSpec(
            id=item.id,
            label=item.label,
            description=item.description,
            input_items=self._list_metadata_value(item, "input_items", fallback_key="inputs"),
            output_items=self._list_metadata_value(item, "output_items", fallback_key="outputs"),
            status=item.status,
            source=item.source,
            evidence=item.evidence or None,
            confidence=item.confidence,
        )

    def _task_candidate(self, item: MemoryItem) -> ExecutableTaskCandidate:
        return ExecutableTaskCandidate(
            id=item.id,
            label=item.label,
            description=item.description,
            task_type=self._metadata_value(item, "task_type", "unknown"),
            required_inputs=self._list_metadata_value(item, "required_inputs"),
            expected_outputs=self._list_metadata_value(item, "expected_outputs"),
            required_rules=self._list_metadata_value(item, "required_rules"),
            required_decision_criteria=self._list_metadata_value(item, "required_decision_criteria"),
            required_procedures=self._list_metadata_value(item, "required_procedures"),
            status=item.status,
            source=item.source,
            evidence=item.evidence or None,
            confidence=item.confidence,
        )

    def _metadata_value(self, item: MemoryItem, key: str, default: str) -> str:
        value = item.metadata.get(key)
        if isinstance(value, str) and value:
            return value
        if value is not None and not isinstance(value, (list, dict)):
            return str(value)
        return self._description_value(item.description, key, default)

    def _description_value(self, description: str, key: str, default: str) -> str:
        prefix = f"{key}:"
        for line in description.splitlines():
            if line.startswith(prefix):
                return line[len(prefix) :].strip() or default
        return default

    def _list_metadata_value(
        self,
        item: MemoryItem,
        key: str,
        *,
        fallback_key: str | None = None,
    ) -> list[str]:
        value = item.metadata.get(key)
        if isinstance(value, list):
            return [str(part) for part in value if str(part).strip()]
        if isinstance(value, str) and value:
            return [part.strip() for part in value.split("|") if part.strip()]
        raw = self._description_value(item.description, fallback_key or key, "")
        if not raw:
            return []
        return [part.strip() for part in raw.split("|") if part.strip()]


class LLMBusinessCapabilityBuilder:
    def __init__(
        self,
        provider: LLMProvider,
        fallback: RuleBasedBusinessCapabilityBuilder | None = None,
    ) -> None:
        self.provider = provider
        self.fallback = fallback or RuleBasedBusinessCapabilityBuilder()

    def build(self, memory: ProjectMemory) -> BusinessCapabilityModel:
        system_prompt = load_prompt("internal", "business_capability_builder.md")
        user_prompt = (
            "Return JSON only matching the BusinessCapabilityModel schema.\n"
            f"Project memory:\n{memory.model_dump_json(indent=2)}\n"
        )
        try:
            payload = extract_json_object(self.provider.invoke(system_prompt, user_prompt))
            if not isinstance(payload, dict):
                raise ValueError("Business capability builder response must be a JSON object")
            return BusinessCapabilityModel.model_validate(payload)
        except Exception:
            return self.fallback.build(memory)
