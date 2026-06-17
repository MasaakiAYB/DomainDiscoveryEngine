# DomainDiscoveryEngine

DomainDiscoveryEngine, abbreviated as `DDE`, is the upstream domain-discovery component of a future intent-driven system generation platform.
It does not generate or deploy applications.
Its responsibility is to converge user dialogue into a structured DomainModel.

## MVP Scope

- Analyze user dialogue
- Extract goals, concepts, tasks, constraints, assumptions, decisions, and unknowns
- Maintain `ProjectMemory` as the current understanding state
- Build a reviewable `DomainModel`
- Detect missing information by simulation-style break tests
- Ask one prioritized next question

## Out Of Scope

- Domain-to-IR generation
- Application code generation
- Deployment and hosting automation
- Production authentication, authorization, and observability

## Main Pipeline

```text
User Dialogue
  -> DialogueAnalyzer
  -> MemoryUpdater
  -> ProjectMemory
  -> DomainModelBuilder
  -> SimulationTester
  -> QuestionGenerator
  -> ResponseComposer
```

## Larger Architecture

```text
User Dialogue
  -> DomainDiscoveryEngine
  -> DomainModel
  -> Future Domain-to-IR Generator
  -> Future Application Generator
  -> Future Deployment Engine
```

## Expected Output

The expected output of DDE is a structured, reviewable `DomainModel` plus unresolved questions that help converge the domain understanding.
