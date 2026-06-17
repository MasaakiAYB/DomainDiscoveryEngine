# TASK 09: QuestionGenerator

## Goal

Convert unknowns into one high-priority user-friendly question.

## Files to implement

```text
src/domain_discovery_engine/schemas/question.py
src/domain_discovery_engine/agents/question_generator.py
src/domain_discovery_engine/prompts/question_generator.md
tests/test_question_generator.py
```

## Required schemas

`QuestionPriority` enum:

```text
high
medium
low
```

`Question`:

```python
id: str
text: str
reason: str
priority: QuestionPriority
target_unknown_ids: list[str]
examples: list[str] = []
```

`QuestionSet`:

```python
candidate_questions: list[Question] = []
selected_question: Question | None = None
```

## Required entry point

```python
class QuestionGenerator:
    def generate(self, memory: ProjectMemory, domain_model: DomainModel, simulation_result: SimulationResult | None = None) -> QuestionSet: ...
```

## MVP priority rules

High priority:

- Unknown affects a core goal.
- Unknown affects task execution.
- Unknown comes from simulation break test.

Medium priority:

- Unknown affects concept details.

Low priority:

- Future implementation detail.

## Required wording rule

Questions must be answerable by a non-engineer.

Bad:

```text
類似判定基準を定義してください。
```

Good:

```text
「似た実験」を探すとき、何が近いものを似ていると判断しますか？ 例: 試料、実験条件、測定値、目的、担当者
```

## Tests

Create tests that verify:

1. A similarity unknown produces the good-style question above or equivalent.
2. Only one selected question is returned.
3. Selected question references target unknown ids.
