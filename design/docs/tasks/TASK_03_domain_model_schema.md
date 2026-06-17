# TASK 03: DomainModel schema

## Goal

Implement the user-reviewable domain model data contracts.

## Files to implement

```text
src/domain_discovery_engine/schemas/domain_model.py
tests/test_domain_model_schema.py
```

## Required models

- `DomainModelItemStatus`
- `DomainConcept`
- `DomainRelation`
- `DomainTask`
- `DomainConstraint`
- `DomainModel`

## Required status values

```text
candidate
confirmed
unresolved
```

## Required fields

`DomainConcept`:

```python
id: str
name: str
description: str = ""
status: DomainModelItemStatus = DomainModelItemStatus.CANDIDATE
source_memory_item_ids: list[str] = []
```

`DomainRelation`:

```python
id: str
subject: str
predicate: str
object: str
description: str = ""
status: DomainModelItemStatus = DomainModelItemStatus.CANDIDATE
source_memory_item_ids: list[str] = []
```

`DomainTask`:

```python
id: str
name: str
description: str = ""
actor: str | None = None
status: DomainModelItemStatus = DomainModelItemStatus.CANDIDATE
source_memory_item_ids: list[str] = []
```

`DomainConstraint`:

```python
id: str
label: str
description: str = ""
status: DomainModelItemStatus = DomainModelItemStatus.CANDIDATE
source_memory_item_ids: list[str] = []
```

`DomainModel`:

```python
project_id: str
title: str = ""
purpose: list[str] = []
concepts: list[DomainConcept] = []
relations: list[DomainRelation] = []
tasks: list[DomainTask] = []
constraints: list[DomainConstraint] = []
assumptions: list[str] = []
decisions: list[str] = []
unresolved_questions: list[str] = []
```

## Tests

Create tests that verify:

1. DomainModel can be created with concepts, relations, and tasks.
2. List defaults are not shared.
3. Model can round-trip through `model_dump()` and `model_validate()`.
