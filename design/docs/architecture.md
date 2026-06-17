# Architecture

## Overview

DomainDiscoveryEngine is a dialogue-driven domain model convergence engine.

It maintains an evolving ProjectMemory and uses that memory to build, test, and refine a DomainModel.

```text
User Message
  ↓
DialogueAnalyzer
  ↓
MemoryUpdater
  ↓
ProjectMemory
  ↓
DomainModelBuilder
  ↓
SimulationTester
  ↓
QuestionGenerator
  ↓
ResponseComposer
  ↓
Assistant Response
```

## Main workflow

Each user message triggers one workflow turn.

1. `DialogueAnalyzer` extracts structured candidates.
2. `MemoryUpdater` merges extracted candidates into `ProjectMemory`.
3. `DomainModelBuilder` generates a reviewable `DomainModel`.
4. `SimulationTester` runs task-level simulations and break tests.
5. `MemoryUpdater` adds newly discovered unknowns or contradictions.
6. `QuestionGenerator` selects the next best question.
7. `ResponseComposer` formats the response.

## Why ProjectMemory exists

Conversation history is not enough.

The system needs an explicit memory structure that separates:

- confirmed facts
- AI hypotheses
- rejected options
- unresolved questions
- decisions
- assumptions
- contradictions

Without this separation, later agents may treat guesses as facts.

## DomainModel versus ProjectMemory

`ProjectMemory` is the internal evolving memory.

`DomainModel` is the current external-facing business model synthesized from ProjectMemory.

ProjectMemory may contain rejected items, uncertainty, evidence, and historical reasoning.
DomainModel should be concise and user-reviewable.

## DomainModel versus System IR

DomainModel is business-facing.

System IR is implementation-facing.

DDE only outputs DomainModel. It should not decide database tables, API endpoints, frontend components, or deployment configuration.
