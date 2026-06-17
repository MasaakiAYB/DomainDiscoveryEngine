# Testing Strategy

## What to test

The MVP should test behavior, not just functions.

## Unit tests

### MemoryItem validation

- confidence must be between 0 and 1
- status must be valid
- source must be valid

### ProjectMemory update

- adds new items
- deduplicates similar items
- preserves confirmed items
- records contradictions instead of overwriting

### DomainModelBuilder

- excludes rejected items
- includes unresolved high-priority questions
- uses business language

### QuestionGenerator

- selects one high-priority question
- does not ask implementation-specific questions too early

## Example-based tests

Use examples under `examples/`.

For each example:

- conversation.md
- expected_memory.yaml
- expected_domain_model.yaml

Run regression tests to ensure model behavior does not drift.

## Manual evaluation checklist

For each test scenario, ask:

1. Are the key concepts captured?
2. Are the key tasks captured?
3. Are assumptions separated from facts?
4. Are important missing details detected?
5. Is the next question useful?
6. Would a business user recognize the model as their domain?
