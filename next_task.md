# NEXT TASK: Reposition DDE as a Business Capability Discovery Engine

## Objective

Update DomainDiscoveryEngine to reflect the revised FY2026 direction.

The project should no longer be positioned only as a "domain model builder for system generation".

It should be positioned as:

> A generic engine that structures business knowledge from dialogue and converts it into executable task candidates.

The target of democratization is not "systems" but "business capabilities".

A business capability means reusable executable knowledge, including:

- judgment criteria
- business procedures
- business rules
- constraints
- domain concepts
- task decomposition
- operational know-how

The downstream forms may include:

- Skill
- MCP Tool
- API
- Workflow
- Agent
- UI

However, this task must NOT implement downstream conversion yet.

The scope of this task is to extend the current DDE model so it can represent business capability knowledge and executable task candidates.

---

## Current Project Context

The current implementation already includes:

- ProjectMemory
- DomainModel
- DialogueAnalyzer
- MemoryUpdater
- DomainModelBuilder
- SimulationTester
- QuestionGenerator
- Rule-based mode
- LLM mode
- Prompt externalization
- Japanese user-facing behavior
- Docker runtime
- Azure OpenAI provider layer

Keep the current architecture.

Do not rewrite the whole project.

Extend it carefully.

---

## Revised Positioning

### Before

```text
Dialogue
↓
Domain Model
↓
System IR
↓
Application Generation
```

### After

```text
Dialogue
↓
Business Knowledge Structuring
↓
Business Capability Model
↓
Executable Task Candidates
↓
Skill / MCP Tool / API / Workflow / Agent / UI
```

DDE is responsible for the first three steps:

```text
Dialogue
↓
Business Knowledge Structuring
↓
Business Capability Model
↓
Executable Task Candidates
```

DDE is NOT responsible for generating Skills, MCP tools, APIs, workflows, agents, or UIs in this phase.

---

## Key Conceptual Change

The term "Domain" in DomainDiscoveryEngine should be interpreted broadly.

It does not only mean an application domain model.

It means the user's business domain knowledge and capability structure.

The existing DomainModel can remain, but it should become one part of a broader BusinessCapabilityModel.

---

# TASK-31: Add Business Capability Model Schema

## Goal

Add schemas for representing reusable business capability knowledge.

## Create

```text
src/domain_discovery_engine/schemas/business_capability.py
```

## Required classes

Create Pydantic models for the following.

### BusinessRule

Represents a rule that constrains or governs business execution.

Fields:

```python
id: str
label: str
description: str
rule_type: str  # e.g. validation, eligibility, exception, priority, calculation, compliance
status: str     # candidate, confirmed, rejected, unresolved
source: str     # user, ai_inferred, simulation
evidence: str | None
confidence: float
```

### DecisionCriterion

Represents a judgment criterion used by humans or agents.

Fields:

```python
id: str
label: str
description: str
criterion_type: str  # e.g. selection, evaluation, rejection, ranking, review
status: str
source: str
evidence: str | None
confidence: float
```

### BusinessProcedure

Represents a business procedure or work step sequence.

Fields:

```python
id: str
label: str
description: str
steps: list[str]
status: str
source: str
evidence: str | None
confidence: float
```

### InputOutputSpec

Represents required inputs and expected outputs.

Fields:

```python
id: str
label: str
description: str
input_items: list[str]
output_items: list[str]
status: str
source: str
evidence: str | None
confidence: float
```

### ExecutableTaskCandidate

Represents a candidate task that could later become a Skill, MCP Tool, API, Workflow, Agent, or UI.

Fields:

```python
id: str
label: str
description: str
task_type: str  # skill, mcp_tool, api, workflow, agent, ui, unknown
required_inputs: list[str]
expected_outputs: list[str]
required_rules: list[str]
required_decision_criteria: list[str]
required_procedures: list[str]
status: str
source: str
evidence: str | None
confidence: float
```

### BusinessCapabilityModel

Represents the full business capability structure.

Fields:

```python
purpose: list[str]
concepts: list[Any]  # reuse existing concept structure if available
tasks: list[Any]     # reuse existing task structure if available
rules: list[BusinessRule]
decision_criteria: list[DecisionCriterion]
procedures: list[BusinessProcedure]
input_outputs: list[InputOutputSpec]
constraints: list[Any]
executable_task_candidates: list[ExecutableTaskCandidate]
unknowns: list[Any]
```

## Requirements

- Use existing enum/status conventions if they already exist.
- Do not break existing DomainModel tests.
- DomainModel must remain available.
- BusinessCapabilityModel is an extension, not a replacement yet.

---

# TASK-32: Extend ProjectMemory

## Goal

ProjectMemory must be able to store business capability knowledge.

## Update

```text
src/domain_discovery_engine/schemas/memory.py
```

Add memory sections:

```python
business_rules
decision_criteria
procedures
input_outputs
executable_task_candidates
```

Each should use the existing MemoryItem style if possible.

## Requirements

- Existing fields must remain unchanged.
- Existing tests must continue to pass.
- JSON serialization/deserialization must work.
- Existing saved ProjectMemory files should still load if possible.

---

# TASK-33: Add Business Capability Builder

## Goal

Create a builder that transforms ProjectMemory into BusinessCapabilityModel.

## Create

```text
src/domain_discovery_engine/agents/business_capability_builder.py
```

## Required behavior

Input:

```python
ProjectMemory
```

Output:

```python
BusinessCapabilityModel
```

The builder should collect:

- goals -> purpose
- concepts -> concepts
- tasks -> tasks
- constraints -> constraints
- business_rules -> rules
- decision_criteria -> decision_criteria
- procedures -> procedures
- input_outputs -> input_outputs
- executable_task_candidates -> executable_task_candidates
- unknowns -> unknowns

## LLM mode

If the current architecture supports LLM mode, add an LLM implementation.

The prompt should be internal English.

It must preserve Japanese business labels.

## Rule-based mode

Add a minimal rule-based implementation that maps ProjectMemory fields directly.

---

# TASK-34: Update Dialogue Analyzer Extraction Targets

## Goal

DialogueAnalyzer should extract business capability related information.

## Update both rule-based and LLM analyzer outputs to include:

- business_rules
- decision_criteria
- procedures
- input_outputs
- executable_task_candidates

## Example Japanese input

```text
購買見積を評価するとき、単価だけでなく仕様一致、単位整合、過去実績との差分を見て判断したい。
明らかに対象外の候補は除外し、判断が難しいものはレビュー対象にしたい。
```

Expected extracted items:

```text
BusinessRule:
- 対象外候補は除外する
- 判断が難しいものはレビュー対象にする

DecisionCriterion:
- 仕様一致
- 単位整合
- 過去実績との差分
- 単価

ExecutableTaskCandidate:
- 見積候補を評価する
- レビュー対象を抽出する
```

---

# TASK-35: Add Task Candidate Extraction

## Goal

Create explicit executable task candidates from structured business knowledge.

## Create

```text
src/domain_discovery_engine/agents/task_candidate_extractor.py
```

## Required behavior

Input:

```python
ProjectMemory or BusinessCapabilityModel
```

Output:

```python
list[ExecutableTaskCandidate]
```

## Task candidate generation rules

A task candidate should be generated when the model has:

- an action or task
- required input candidates
- expected output candidates
- at least one rule, criterion, procedure, or constraint

## Candidate task types

Use one of:

```text
skill
mcp_tool
api
workflow
agent
ui
unknown
```

Default to:

```text
unknown
```

Do not over-classify.

## Important

Do NOT implement actual Skill / MCP / API generation.

Only generate candidates.

---

# TASK-36: Update Simulation Tester

## Goal

SimulationTester should test business capability completeness, not only application/domain model completeness.

It should check whether an executable task candidate has enough information to be implemented later.

## Required checks

For each executable task candidate, check:

- Are required inputs defined?
- Are expected outputs defined?
- Are business rules defined?
- Are decision criteria defined?
- Are exception cases or review conditions defined?
- Are unclear terms captured as unknowns?

If information is missing, add unknowns.

## Example unknowns

```text
レビュー対象とする閾値が未定義
仕様一致の判定基準が未定義
単位換算可能と判断する条件が未定義
```

---

# TASK-37: Update Question Generator

## Goal

QuestionGenerator should ask clarification questions related to business capability extraction.

It should prioritize questions that make task execution possible.

## Question priorities

High priority:

- missing decision criteria
- missing business rules
- missing required inputs
- missing expected outputs
- missing exception handling
- missing review condition

Lower priority:

- UI preference
- implementation format
- downstream tool type

## User-facing language

Questions must be Japanese by default.

Do not mention internal terms like:

- BusinessCapabilityModel
- schema
- executable task candidate
- IR

Bad:

```text
ExecutableTaskCandidateの入力を定義してください。
```

Good:

```text
見積候補を評価する際、入力として最低限必要な情報は何ですか？
例: 品名、仕様、単位、数量、候補カタログ、過去実績など
```

---

# TASK-38: Update Prompts

## Update internal prompts

Move or update these prompts:

```text
prompts/internal/dialogue_analyzer.md
prompts/internal/domain_model_builder.md
prompts/internal/simulation_tester.md
```

Add or update:

```text
prompts/internal/business_capability_builder.md
prompts/internal/task_candidate_extractor.md
```

Internal prompts should be English.

They must state:

- Preserve Japanese user-provided labels
- Extract business rules
- Extract decision criteria
- Extract procedures
- Extract input/output information
- Extract executable task candidates
- Do not generate downstream artifacts yet

## Update user-facing prompts

Update:

```text
prompts/user_facing/question_generator.md
```

It must generate Japanese clarification questions that help complete executable task candidates.

---

# TASK-39: Update Workflow

## Goal

Add business capability extraction to the existing workflow.

## Existing workflow

```text
DialogueAnalyzer
↓
MemoryUpdater
↓
DomainModelBuilder
↓
SimulationTester
↓
QuestionGenerator
```

## New workflow

```text
DialogueAnalyzer
↓
MemoryUpdater
↓
DomainModelBuilder
↓
BusinessCapabilityBuilder
↓
TaskCandidateExtractor
↓
SimulationTester
↓
QuestionGenerator
```

## Requirements

- Existing DomainModel output must remain available.
- New BusinessCapabilityModel output must be available.
- CLI should display a concise summary of executable task candidates.
- Existing tests must still pass.

---

# TASK-40: Update CLI Output

## Goal

CLI should show business capability output in addition to domain model output.

## Add display sections

```text
Business Rules
Decision Criteria
Procedures
Executable Task Candidates
Unresolved Questions
```

## Requirements

- Japanese labels must be preserved.
- Output should be readable by Japanese business users.
- Do not show raw JSON by default.

---

# TASK-41: Add Example Scenarios

## Create examples

```text
examples/purchasing_estimate_evaluation/
  conversation.md
  expected_business_capability.yaml

examples/system_understanding_documentation/
  conversation.md
  expected_business_capability.yaml

examples/data_analysis_support/
  conversation.md
  expected_business_capability.yaml
```

## Scenario 1: Purchasing Estimate Evaluation

Must include:

- judgment criteria
- exclusion rules
- review conditions
- candidate matching task

## Scenario 2: System Understanding / Documentation Generation

Must include:

- code structure understanding
- module extraction
- dependency explanation
- documentation generation task

## Scenario 3: Data Analysis Support

Must include:

- input dataset
- analysis objective
- preprocessing
- visualization
- insight generation

---

# TASK-42: Add Tests

## Required tests

Add tests for:

1. BusinessCapabilityModel schema
2. ProjectMemory extended fields
3. BusinessCapabilityBuilder
4. TaskCandidateExtractor
5. DialogueAnalyzer extraction of business rules and decision criteria
6. SimulationTester unknown generation for incomplete executable tasks
7. QuestionGenerator Japanese questions for missing criteria
8. CLI displays executable task candidates
9. Existing DomainModel behavior remains backward compatible

---

# TASK-43: Update README and Design Docs

## README updates

Update README to reflect the new positioning.

Add:

```text
DomainDiscoveryEngine structures business knowledge from dialogue and turns it into executable task candidates.
```

Explain that DDE is the front-stage engine of a future business capability assetization platform.

## Design docs

Update or create:

```text
docs/business_capability_model.md
docs/fy2026_direction.md
```

`docs/fy2026_direction.md` should summarize:

- The target of democratization is business capability, not systems
- Business capability consists of rules, procedures, criteria, constraints, and know-how
- DDE handles the front-stage generic model
- Downstream conversion to Skill/MCP/API/Workflow/Agent is out of scope for this phase

---

# Non-goals

Do NOT implement:

- Skill generation
- MCP Tool generation
- API generation
- Workflow execution
- Agent runtime
- UI generation
- IR generation
- Deployment of generated artifacts
- Neo4j
- Knowledge graph database
- Full evaluation framework

---

# Acceptance Criteria

The implementation is complete when:

1. All tests pass
2. Existing DomainModel behavior remains available
3. BusinessCapabilityModel schema exists
4. ProjectMemory can store rules, decision criteria, procedures, input/output specs, and executable task candidates
5. DialogueAnalyzer can extract business capability information
6. BusinessCapabilityBuilder can produce BusinessCapabilityModel
7. TaskCandidateExtractor can produce ExecutableTaskCandidate objects
8. SimulationTester can detect missing information for executable task candidates
9. QuestionGenerator asks Japanese clarification questions related to missing business capability information
10. CLI displays executable task candidates
11. README reflects the revised FY2026 positioning
12. No downstream artifact generation is implemented

---

# Recommended Codex Scope

This is a relatively large conceptual shift.

If Codex performance is unstable, split into two runs.

## Run A

Implement:

- TASK-31
- TASK-32
- TASK-33
- TASK-35
- TASK-42 partial tests for schemas/builders

## Run B

Implement:

- TASK-34
- TASK-36
- TASK-37
- TASK-38
- TASK-39
- TASK-40
- TASK-41
- TASK-43

If possible, Run A should be done first and committed before Run B.
