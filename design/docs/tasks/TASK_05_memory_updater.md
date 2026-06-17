# TASK 05: MemoryUpdater

## Goal

Implement deterministic merge behavior for ProjectMemory.

## Files to implement

```text
src/domain_discovery_engine/agents/memory_updater.py
tests/test_memory_updater.py
```

## Required function/class

Implement one clear entry point, for example:

```python
class MemoryUpdater:
    def merge_items(self, memory: ProjectMemory, items: list[MemoryItem]) -> ProjectMemory: ...
```

## Merge rules

1. Add new items into the matching ProjectMemory list based on `MemoryItem.type`.
2. If an equivalent item already exists, update evidence/confidence instead of duplicating.
3. User-confirmed facts must not be overwritten by AI-inferred candidates.
4. Rejected items must go to `rejected_items`.
5. Contradictions must go to `contradictions`.

## Equivalence rule for MVP

Use normalized label matching:

- strip spaces
- lowercase where applicable
- compare exact normalized labels

Do not implement semantic embedding similarity in MVP.

## Tests

Create tests that verify:

1. New concept is added to `memory.concepts`.
2. Duplicate label is not duplicated.
3. Confirmed user item is not downgraded by candidate inferred item.
4. Rejected item is routed to `rejected_items`.
