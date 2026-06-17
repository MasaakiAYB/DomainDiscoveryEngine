# TASK 04: JSON memory store

## Goal

Implement JSON persistence for ProjectMemory.

## Files to implement

```text
src/domain_discovery_engine/memory/store.py
src/domain_discovery_engine/memory/json_store.py
tests/test_json_store.py
```

## Required behavior

`store.py` should define a protocol or abstract base class with:

```python
save(memory: ProjectMemory) -> None
load(project_id: str) -> ProjectMemory | None
exists(project_id: str) -> bool
```

`json_store.py` should implement it using one JSON file per project.

## Storage format

Suggested path:

```text
.data/projects/{project_id}/project_memory.json
```

## Tests

Create tests that verify:

1. Save then load preserves all fields.
2. Loading a missing project returns `None`.
3. `exists()` works.
4. Store creates parent directories automatically.
