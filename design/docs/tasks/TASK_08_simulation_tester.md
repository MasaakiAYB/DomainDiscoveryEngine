# TASK 08: SimulationTester

## Goal

Run simple break tests against the current DomainModel and produce missing information as unknowns.

## Files to implement

```text
src/domain_discovery_engine/schemas/simulation.py
src/domain_discovery_engine/agents/simulation_tester.py
src/domain_discovery_engine/prompts/simulation_tester.md
tests/test_simulation_tester.py
```

## Required schemas

`SimulationFinding`:

```python
id: str
scenario: str
finding_type: str  # missing_info | contradiction | risk
message: str
related_task: str | None = None
generated_unknown: MemoryItem | None = None
```

`SimulationResult`:

```python
findings: list[SimulationFinding] = []
unknowns: list[MemoryItem] = []
contradictions: list[MemoryItem] = []
```

## Required entry point

```python
class SimulationTester:
    def run(self, domain_model: DomainModel, memory: ProjectMemory) -> SimulationResult: ...
```

## MVP break-test heuristics

If a task contains words like `探す`, `検索`, or `search`, ensure there is some unknown/constraint/concept about search criteria. If not, generate unknown:

```text
検索条件が未定義
```

If a task contains `似た` or `類似`, ensure there is some unknown/constraint/decision about similarity criteria. If not, generate unknown:

```text
類似判定基準が未定義
```

If a task contains `予約`, ensure there are concepts or constraints related to time/date and duplicate prevention. If not, generate appropriate unknowns.

## Tests

Create tests that verify:

1. Similar experiment search generates unknown for similarity criteria.
2. Search task generates unknown for search criteria.
3. Generated unknowns have source `simulation` and status `unresolved`.
