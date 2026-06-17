# Workflow Design

## One-turn workflow

```text
Input: user_message, project_memory

1. Analyze user message
2. Merge extracted items into ProjectMemory
3. Build DomainModel
4. Run simulation and break tests
5. Merge simulation findings into ProjectMemory
6. Generate candidate questions
7. Select next question
8. Compose response
9. Persist ProjectMemory and DomainModel
```

## LangGraph-style node design

```text
START
  ↓
analyze_user_message
  ↓
update_project_memory_from_extraction
  ↓
build_domain_model
  ↓
run_simulation_tests
  ↓
update_project_memory_from_simulation
  ↓
generate_questions
  ↓
compose_response
  ↓
END
```

## State shape

```python
class State:
    messages: list
    latest_user_message: str
    project_memory: ProjectMemory
    extraction: DialogueExtraction | None
    domain_model: DomainModel | None
    simulation_result: SimulationResult | None
    candidate_questions: list[Question]
    response: str | None
```

## Stopping condition for MVP

The MVP does not need automatic completion detection.

However, it should expose convergence hints:

- number of unresolved high-priority unknowns
- number of confirmed core concepts
- number of confirmed core tasks
- whether the current model has been explicitly accepted by the user

## Model break test principle

The system should not only ask checklist questions.

It should simulate actual task execution and detect where the current model fails.

Example:

```text
Task: Search similar past experiments
Break test:
- Is the searchable target defined?
- Are search keys defined?
- Is similarity criteria defined?
- Is the output of search defined?
- Is reuse behavior defined?
```
