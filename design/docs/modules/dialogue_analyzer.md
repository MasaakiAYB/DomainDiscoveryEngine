# Module: DialogueAnalyzer

## Responsibility

Extract structured candidates from the latest user message.

## Input

- latest user message
- current ProjectMemory

## Output

DialogueExtraction:

```yaml
goals: []
concepts: []
tasks: []
relations: []
constraints: []
assumptions: []
decisions: []
unknowns: []
```

## Extraction rules

- Extract only what is reasonably supported by the user message.
- If something is inferred from general knowledge, mark source as `ai_inferred`.
- If the user explicitly states something, mark source as `user`.
- Do not treat inferred items as confirmed.
- Prefer small, atomic items.

## Example

User:

```text
実験条件と結果を記録して、過去の似た実験を探せるようにしたい
```

Extraction:

```yaml
goals:
  - label: 過去の似た実験を探せるようにする
    source: user

concepts:
  - label: 実験
    source: ai_inferred
  - label: 実験条件
    source: user
  - label: 実験結果
    source: user

tasks:
  - label: 実験条件と結果を記録する
    source: user
  - label: 過去の似た実験を探す
    source: user

unknowns:
  - label: 似た実験の判定基準
    source: ai_inferred
```
