# Module: QuestionGenerator

## Responsibility

Convert unresolved unknowns into user-friendly follow-up questions.

## Input

- ProjectMemory
- DomainModel
- SimulationResult

## Output

- list of candidate questions
- selected next question

## Question schema

```python
class Question(BaseModel):
    id: str
    text: str
    reason: str
    priority: str
    target_unknown_ids: list[str]
    examples: list[str] = []
```

## Good question style

Bad:

```text
類似判定基準を定義してください。
```

Good:

```text
「似た実験」を探すとき、何が近いものを似ていると判断しますか？
例: 試料、実験条件、測定値、目的、担当者
```

## Prioritization rules

Ask first about unknowns that affect:

1. Core goal
2. Core task execution
3. Key concept relationships
4. Constraints that prevent invalid behavior
5. Future implementation details

Do not ask too many questions at once.

For MVP, output one main question plus optional examples.
