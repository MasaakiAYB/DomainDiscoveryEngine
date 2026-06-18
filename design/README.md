# DomainDiscoveryEngine

DomainDiscoveryEngine, abbreviated as `DDE`, is the upstream business knowledge structuring component of a future capability democratization platform.
It does not generate or deploy downstream artifacts.
Its responsibility is to converge user dialogue into a structured business capability model and executable task candidates.

## MVP Scope

- Analyze user dialogue
- Extract goals, concepts, tasks, constraints, assumptions, decisions, and unknowns
- Maintain `ProjectMemory` as the current understanding state
- Build a reviewable `DomainModel`
- Build a broader `BusinessCapabilityModel`
- Identify reusable executable task candidates
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
  -> Business Capability Model
  -> Executable Task Candidates
  -> Future Skill / MCP Tool / API / Workflow / Agent / UI Conversion
```

## Expected Output

The expected output of DDE is a structured, reviewable `DomainModel`, a broader `BusinessCapabilityModel`, executable task candidates, and unresolved questions that help converge the business understanding.
