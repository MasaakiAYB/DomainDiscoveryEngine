# DomainDiscoveryEngine Architecture

## DialogueAnalyzer

Responsibility
Extract structured candidates from the latest user message.

Input
Latest user message and current `ProjectMemory`.

Output
`DialogueExtraction`.

Must not do
Must not treat AI inference as user-confirmed fact.

## MemoryUpdater

Responsibility
Merge extracted or simulated items into `ProjectMemory`.

Input
Current `ProjectMemory` and new `MemoryItem` values.

Output
Updated `ProjectMemory`.

Must not do
Must not silently overwrite user-confirmed items with weaker AI-inferred candidates.

## ProjectMemory

Responsibility
Represent the current understanding state of the project.

Input
Structured memory items from analysis and simulation.

Output
A normalized working memory for downstream modules.

Must not do
Must not be treated as raw conversation history.

## DomainModelBuilder

Responsibility
Build a concise, user-reviewable `DomainModel` from `ProjectMemory`.

Input
`ProjectMemory`.

Output
`DomainModel`.

Must not do
Must not include rejected items as active facts.

## SimulationTester

Responsibility
Try to execute plausible user tasks against the current model to find missing information.

Input
`DomainModel` and `ProjectMemory`.

Output
`SimulationResult` including findings, unknowns, and contradictions when applicable.

Must not do
Must not validate the model politely; it should probe for missing information and failure cases.

## QuestionGenerator

Responsibility
Turn unresolved unknowns into one prioritized, business-friendly next question.

Input
`ProjectMemory`, `DomainModel`, and optional `SimulationResult`.

Output
`QuestionSet`.

Must not do
Must not ask implementation-specific questions too early.

## ResponseComposer

Responsibility
Format the current model state and next question into a user-facing response.

Input
`DomainModel`, unresolved questions, and selected next question.

Output
User-facing response text.

Must not do
Must not present candidate or inferred items as confirmed facts.

## DiscoveryWorkflow

Responsibility
Orchestrate one discovery turn across the pipeline.

Input
User message and current `ProjectMemory`.

Output
Updated workflow state including memory, domain model, simulation result, and question set.

Must not do
Must not redesign downstream systems or generate application code.

## Key Constraints

- `ProjectMemory` is the current understanding state, not raw chat history.
- AI-inferred and user-confirmed items must remain distinguishable through fields such as source, status, confidence, and evidence.
- `SimulationTester` should detect missing information by trying to execute plausible user tasks against the current `DomainModel`.
