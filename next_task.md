# NEXT TASK (Phase 2)

## Objective

Move DomainDiscoveryEngine from a rule-based MVP to an LLM-assisted domain discovery system while preserving the existing architecture.

The current implementation successfully demonstrates:

- ProjectMemory
- DomainModel generation
- Simulation / Break Test
- Question generation

The next goal is to introduce an LLM abstraction layer and migrate the existing agents to use an Azure OpenAI based implementation.

Use the company OpenAI environment pattern demonstrated in `llm_match_catalog_item.py`.

Reference:
- AzureChatOpenAI
- langchain_core.messages
- dotenv based configuration
- Thread-local LLM instance reuse pattern where appropriate

Do NOT redesign the architecture.

---

# TASK-12: Introduce LLM Provider Layer

## Goal

Create a reusable LLM client abstraction.

## Files

Create:

- src/domain_discovery_engine/llm/provider.py

Create:

```python
class LLMProvider:
    def invoke(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        ...
```

Implementation requirements:

- Use AzureChatOpenAI
- Use environment variables
- Use dotenv
- Support model configuration
- Support temperature configuration
- Support reasoning effort configuration if available

Follow the implementation style used in the provided company example.

---

# TASK-13: Prompt Externalization

## Goal

Move agent prompts into dedicated prompt files.

## Files

Create:

- prompts/dialogue_analyzer.md
- prompts/domain_model_builder.md
- prompts/simulation_tester.md
- prompts/question_generator.md

Requirements:

- No prompts hardcoded in agent implementations
- Prompt files loaded dynamically
- Missing prompt file must raise explicit exception

---

# TASK-14: LLM Dialogue Analyzer

## Goal

Replace keyword extraction with structured LLM extraction.

## Output Schema

Return:

- goals
- concepts
- tasks
- constraints
- assumptions
- unknowns

Requirements:

- Output must be JSON
- Validate with existing schema layer
- Fallback gracefully when parsing fails

Do not remove current rule-based implementation.

Rename current implementation:

- RuleBasedDialogueAnalyzer

Create:

- LLMDialogueAnalyzer

---

# TASK-15: LLM Domain Model Builder

## Goal

Generate domain models through LLM reasoning.

Requirements:

Input:

- ProjectMemory

Output:

- DomainModel

Preserve existing schema contracts.

Do not modify DomainModel structure.

---

# TASK-16: LLM Simulation Tester

## Goal

Use an LLM to identify:

- missing concepts
- missing tasks
- missing constraints
- workflow inconsistencies

Output:

SimulationResult

Existing schema must remain unchanged.

---

# TASK-17: LLM Question Generator

## Goal

Generate user-facing clarification questions.

Requirements:

Questions must:

- be specific
- explain why the information is needed
- be answerable by business users

Bad example:

"Please provide specifications."

Good example:

"When searching past experiments, which attributes should define similarity? (sample, condition, operator, date, etc.)"

---

# TASK-18: Analyzer Strategy Selection

## Goal

Support runtime analyzer selection.

Create configuration:

```env
DDE_ANALYZER_MODE=rule_based
```

Supported:

- rule_based
- llm

Workflow must select implementation automatically.

---

# TASK-19: Docker Validation

## Goal

Verify all functionality works in Docker.

Acceptance Criteria

docker compose up

starts successfully.

CLI works inside container.

Prompt files are packaged correctly.

Environment variables are loaded correctly.

---

# Acceptance Criteria

All tests pass.

Existing functionality remains operational.

A user can run:

```bash
docker compose up
```

and execute a complete discovery session using:

- Rule-based mode
- LLM mode

without code changes.

