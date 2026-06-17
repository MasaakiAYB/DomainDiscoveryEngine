# Implementation Plan

## Phase 1: Schema and memory foundation

Deliverables:

- `schemas/memory.py`
- `schemas/domain_model.py`
- `memory/project_memory.py`
- `memory/json_store.py`

Acceptance criteria:

- Can create an empty ProjectMemory.
- Can add MemoryItems.
- Can persist and reload ProjectMemory as JSON.

## Phase 2: Dialogue extraction

Deliverables:

- `schemas/extraction.py`
- `agents/dialogue_analyzer.py`
- `prompts/dialogue_analyzer.md`

Acceptance criteria:

- Given a user message, outputs goals, concepts, tasks, constraints, and unknowns.
- Marks source and status correctly.

## Phase 3: Memory update

Deliverables:

- `agents/memory_updater.py`

Acceptance criteria:

- Merges extracted items into ProjectMemory.
- Deduplicates obvious duplicates.
- Does not overwrite confirmed facts with inferred candidates.

## Phase 4: Domain model building

Deliverables:

- `agents/domain_model_builder.py`
- `prompts/domain_model_builder.md`

Acceptance criteria:

- Converts ProjectMemory into a concise DomainModel.
- Includes unresolved questions.

## Phase 5: Simulation break tests

Deliverables:

- `schemas/simulation.py`
- `agents/simulation_tester.py`
- `prompts/simulation_tester.md`

Acceptance criteria:

- Generates task-level scenarios.
- Detects missing information.
- Produces unknowns that can be merged into ProjectMemory.

## Phase 6: Question generation

Deliverables:

- `schemas/question.py`
- `agents/question_generator.py`
- `prompts/question_generator.md`

Acceptance criteria:

- Produces one high-priority next question.
- Includes reason and examples.

## Phase 7: CLI MVP

Deliverables:

- `interfaces/cli.py`
- `core/workflow.py`

Acceptance criteria:

- User can run a multi-turn conversation.
- ProjectMemory is persisted.
- Current DomainModel and next question are printed every turn.
