# Module: SimulationTester

## Responsibility

Run task-level simulations against the current DomainModel and detect missing information.

## Input

- DomainModel
- ProjectMemory

## Output

SimulationResult:

```yaml
scenarios: []
findings: []
unknowns: []
contradictions: []
```

## Method

For each important task, simulate the task step-by-step.

Ask:

- Who performs the task?
- What object is manipulated?
- What information is required to perform the task?
- What output is produced?
- What can go wrong?
- What rule prevents invalid behavior?

## Example

Task:

```text
過去の似た実験を探す
```

Break test:

```text
1. User enters search criteria.
2. System finds similar experiments.
3. User compares conditions and results.
4. User reuses a past experiment.
```

Detected unknowns:

```yaml
- 検索条件が未定義
- 類似判定基準が未定義
- 再利用の意味が未定義
```

## Design principle

The SimulationTester should try to break the current model, not validate it politely.
