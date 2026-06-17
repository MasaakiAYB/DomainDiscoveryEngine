# TASK 06: DialogueExtraction schema and analyzer interface

## Goal

Create the structured extraction contract and a testable analyzer interface.

## Files to implement

```text
src/domain_discovery_engine/schemas/extraction.py
src/domain_discovery_engine/agents/dialogue_analyzer.py
src/domain_discovery_engine/prompts/dialogue_analyzer.md
tests/test_dialogue_analyzer.py
```

## Required schema

`DialogueExtraction` should contain:

```python
goals: list[MemoryItem] = []
concepts: list[MemoryItem] = []
tasks: list[MemoryItem] = []
relations: list[MemoryItem] = []
constraints: list[MemoryItem] = []
assumptions: list[MemoryItem] = []
decisions: list[MemoryItem] = []
unknowns: list[MemoryItem] = []
```

## Analyzer design

Implement `DialogueAnalyzer` with a method:

```python
analyze(message: str, memory: ProjectMemory) -> DialogueExtraction
```

For MVP, this may be a rule-based stub or an LLM-backed implementation behind a clean interface.

## Required MVP behavior

Without any LLM dependency, the analyzer should handle the example message:

```text
実験条件と結果を記録して、過去の似た実験を探せるようにしたい
```

Expected extraction must include:

- goal: `過去の似た実験を探せるようにする`
- concepts: `実験条件`, `実験結果`
- tasks: `記録する`, `探す`
- unknown: `似た実験の判定基準`

## Tests

Create tests using the above example.
