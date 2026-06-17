# TASK 02: ProjectMemory schema

## Goal

Implement the core memory data contracts.

## Files to implement

```text
src/domain_discovery_engine/schemas/memory.py
tests/test_memory_schema.py
```

## Required models

Implement exactly these concepts:

- `MemoryItemType`
- `MemoryStatus`
- `MemorySource`
- `MemoryItem`
- `ProjectMemory`

## Required enum values

`MemoryItemType`:

```text
goal
concept
task
relation
constraint
assumption
decision
unknown
rejected
contradiction
```

`MemoryStatus`:

```text
candidate
confirmed
rejected
unresolved
```

`MemorySource`:

```text
user
ai_inferred
simulation
```

## Required fields

`MemoryItem`:

```python
id: str
type: MemoryItemType
label: str
description: str = ""
status: MemoryStatus = MemoryStatus.CANDIDATE
confidence: float  # 0.0 to 1.0
source: MemorySource
evidence: str = ""
related_item_ids: list[str] = []
```

`ProjectMemory`:

```python
project_id: str
title: str = ""
goals: list[MemoryItem] = []
concepts: list[MemoryItem] = []
tasks: list[MemoryItem] = []
relations: list[MemoryItem] = []
constraints: list[MemoryItem] = []
assumptions: list[MemoryItem] = []
decisions: list[MemoryItem] = []
unknowns: list[MemoryItem] = []
rejected_items: list[MemoryItem] = []
contradictions: list[MemoryItem] = []
```

## Implementation notes

- Use Pydantic v2.
- Avoid mutable default bugs. Use `Field(default_factory=list)`.
- Enforce confidence range with validation.

## Tests

Create tests that verify:

1. Empty `ProjectMemory` can be created.
2. `MemoryItem.confidence` rejects values below 0 or above 1.
3. List defaults are not shared across instances.
