# Prompt Guidelines

## General rules

- Output structured JSON whenever possible.
- Distinguish user-stated facts from AI-inferred hypotheses.
- Use `candidate`, `confirmed`, `rejected`, and `unresolved` consistently.
- Preserve evidence text.
- Do not invent domain-specific details unless clearly marked as assumptions.

## DialogueAnalyzer prompt intent

Extract candidate goals, concepts, tasks, constraints, assumptions, decisions, and unknowns from the latest user message.

## DomainModelBuilder prompt intent

Summarize ProjectMemory into a business-facing DomainModel that the user can review.

## SimulationTester prompt intent

Try to execute the current tasks and identify missing information, contradictions, and fragile assumptions.

## QuestionGenerator prompt intent

Ask the most valuable next question to reduce uncertainty in the DomainModel.

## ResponseComposer prompt intent

Show the current understanding and the next question in a concise, non-technical way.
