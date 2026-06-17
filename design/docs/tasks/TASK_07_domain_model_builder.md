# TASK 07: DomainModelBuilder

## Goal

Convert ProjectMemory into a user-reviewable DomainModel.

## Files to implement

```text
src/domain_discovery_engine/agents/domain_model_builder.py
src/domain_discovery_engine/prompts/domain_model_builder.md
tests/test_domain_model_builder.py
```

## Required entry point

```python
class DomainModelBuilder:
    def build(self, memory: ProjectMemory) -> DomainModel: ...
```

## Mapping rules

- `memory.goals` -> `domain_model.purpose`
- `memory.concepts` -> `domain_model.concepts`
- `memory.relations` -> `domain_model.relations`
- `memory.tasks` -> `domain_model.tasks`
- `memory.constraints` -> `domain_model.constraints`
- `memory.assumptions` -> `domain_model.assumptions`
- `memory.decisions` -> `domain_model.decisions`
- `memory.unknowns` -> `domain_model.unresolved_questions`

## Status rule

- Confirmed memory items become confirmed domain model items.
- Candidate memory items may be included as candidate.
- Rejected memory items must not be included.

## Tests

Create tests that verify:

1. Concepts are mapped.
2. Unknowns appear as unresolved questions.
3. Rejected items do not appear.
