# TASK 10: Workflow and CLI MVP

## Goal

Wire the components into a one-turn and multi-turn CLI workflow.

## Files to implement

```text
src/domain_discovery_engine/core/state.py
src/domain_discovery_engine/core/workflow.py
src/domain_discovery_engine/interfaces/cli.py
tests/test_workflow.py
```

## Required state

`DiscoveryState` should include:

```python
project_id: str
latest_user_message: str | None
project_memory: ProjectMemory
domain_model: DomainModel | None
simulation_result: SimulationResult | None
question_set: QuestionSet | None
```

## Required workflow

One turn must execute:

```text
user message
→ DialogueAnalyzer.analyze
→ MemoryUpdater.merge_items
→ DomainModelBuilder.build
→ SimulationTester.run
→ MemoryUpdater.merge_items(simulation unknowns)
→ DomainModelBuilder.build again
→ QuestionGenerator.generate
```

## CLI behavior

CLI should:

1. Ask for or create a project id.
2. Load existing ProjectMemory if present.
3. Accept user input.
4. Run one workflow turn.
5. Print:
   - current purpose
   - concepts
   - tasks
   - unresolved questions
   - selected next question
6. Save ProjectMemory.
7. Continue until user enters `/exit`.

## Acceptance criteria

- Running the CLI allows a basic conversation.
- ProjectMemory is saved and loaded across sessions.
- The example message produces concepts and a next question.
