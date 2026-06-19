# NEXT TASK: Business Capability Model Hardening

## Context

This task follows the current Business Capability expansion already implemented in DomainDiscoveryEngine.

The repository already contains initial implementations for:

- BusinessCapabilityModel
- BusinessRule
- DecisionCriterion
- BusinessProcedure
- InputOutputSpec
- ExecutableTaskCandidate
- BusinessCapabilityBuilder
- TaskCandidateExtractor
- Business Capability workflow integration
- Japanese user-facing question generation

The current implementation is a good first MVP, but it still relies too much on pseudo-structured text inside `MemoryItem.description`.

This task hardens the implementation so that DDE can reliably structure business capability knowledge and produce executable task candidates.

---

## Important Execution Guidance for Codex

The model used for this task is GPT-5.4 with medium reasoning.

Therefore:

- Do not attempt a broad rewrite.
- Do not redesign the whole architecture.
- Prefer small, testable changes.
- Preserve backward compatibility.
- Implement in the recommended run order.
- Commit after each run if possible.
- If a task becomes ambiguous, choose the smallest implementation that satisfies the acceptance criteria.

---

## Main Objective

Improve DDE from:

```text
Business capability concepts stored partly as text
```

to:

```text
Business capability concepts stored as structured model data
```

The most important change is:

```text
Do not store machine-readable metadata in description strings.
Use MemoryItem.metadata instead.
```

---

## Documentation Policy

Human-facing documentation under `docs/` and `design/docs/` should be written primarily in Japanese.

However, formal schema names, class names, field names, file names, and prompt file names must remain in English.

Use fixed Japanese/English concept pairs:

```text
業務能力モデル（BusinessCapabilityModel）
業務ルール（BusinessRule）
判断基準（DecisionCriterion）
業務手順（BusinessProcedure）
入出力仕様（InputOutputSpec）
実行可能タスク候補（ExecutableTaskCandidate）
プロジェクトメモリ（ProjectMemory）
ドメインモデル（DomainModel）
未解決事項（Unknown）
制約（Constraint）
```

Do not use multiple Japanese terms for the same formal concept.

---

## Remove Annual Goal References

Do not mention:

```text
FY2026
2026年度目標
今年度目標
今年度の目標
annual goal
goal-setting
```

in README or design documents.

Rewrite such content as product/project direction.

Use:

```text
docs/project_direction.md
```

not:

```text
docs/fy2026_direction.md
```

---

# Recommended Implementation Plan

Because GPT-5.4 medium reasoning is being used, implement this in three small runs.

---

# Run A: Structured Metadata Foundation

## TASK-A1: Add metadata to MemoryItem

### Goal

Add a structured metadata field to MemoryItem.

### Update

```text
src/domain_discovery_engine/schemas/memory.py
```

### Add field

```python
metadata: dict[str, Any] = Field(default_factory=dict)
```

### Requirements

- Existing ProjectMemory JSON files without metadata must still load.
- Existing tests must pass.
- JSON serialization must include metadata when present.
- metadata must default to an empty dict.

---

## TASK-A2: Stop writing pseudo-metadata into description

### Goal

Newly generated memory items should not store machine-readable fields in description strings.

### Search for patterns like:

```text
rule_type:
criterion_type:
steps:
inputs:
outputs:
task_type:
required_inputs:
expected_outputs:
required_rules:
required_decision_criteria:
required_procedures:
```

If they are being written into `description`, move them to `metadata`.

### Example

Bad:

```python
MemoryItem(
    label="見積候補を評価する",
    description="task_type:unknown\nrequired_inputs:品名,仕様\nexpected_outputs:評価結果",
)
```

Good:

```python
MemoryItem(
    label="見積候補を評価する",
    description="見積候補を評価する",
    metadata={
        "task_type": "unknown",
        "required_inputs": ["品名", "仕様"],
        "expected_outputs": ["評価結果"],
    },
)
```

---

## TASK-A3: Update BusinessCapabilityBuilder to use metadata first

### Update

```text
src/domain_discovery_engine/agents/business_capability_builder.py
```

### Required behavior

When building:

- BusinessRule
- DecisionCriterion
- BusinessProcedure
- InputOutputSpec
- ExecutableTaskCandidate

read structured values from `MemoryItem.metadata`.

### Backward compatibility

Existing pseudo-metadata in `description` may still be parsed as fallback only.

Priority order:

```text
metadata value
↓
description fallback parser
↓
default value
```

### Required metadata keys

For BusinessRule:

```text
rule_type
```

For DecisionCriterion:

```text
criterion_type
```

For BusinessProcedure:

```text
steps
```

For InputOutputSpec:

```text
input_items
output_items
```

For ExecutableTaskCandidate:

```text
task_type
required_inputs
expected_outputs
required_rules
required_decision_criteria
required_procedures
```

---

## TASK-A4: Update TaskCandidateExtractor to emit metadata-compatible candidates

### Update

```text
src/domain_discovery_engine/agents/task_candidate_extractor.py
```

### Requirements

- Do not encode structured information into description strings.
- Return ExecutableTaskCandidate objects with proper fields.
- When creating or updating MemoryItem objects, place structured values in metadata.

---

## TASK-A5: Add tests for metadata migration

### Add or update tests

Cover:

1. MemoryItem accepts metadata
2. ProjectMemory without metadata still loads
3. BusinessCapabilityBuilder prefers metadata over description pseudo-metadata
4. description fallback still works for old data
5. New generated executable task candidate data does not require parsing description

---

## Run A Acceptance Criteria

Run A is complete when:

- All tests pass
- MemoryItem has metadata
- BusinessCapabilityBuilder uses metadata first
- Existing description fallback still works
- New generated data does not rely on description parsing

Stop after Run A if tests become unstable.

---

# Run B: Task Candidate and Simulation Hardening

## TASK-B1: Improve task-to-rule/criterion/procedure linking

### Goal

Avoid attaching all rules, criteria, and procedures to every executable task candidate.

### Update

```text
src/domain_discovery_engine/agents/task_candidate_extractor.py
```

### Required behavior

Use a simple deterministic relevance rule.

A rule/criterion/procedure/input-output item is relevant to a task when at least one condition is true:

1. Its id is explicitly referenced in task metadata.
2. Its label appears in task label or description.
3. A meaningful keyword overlaps between task label/description and item label/description.
4. There is only one task candidate and only one business context.

If no relevance can be established, do not attach it automatically.

Instead, leave the corresponding required_* field empty and allow SimulationTester to raise an unknown.

### Keep it simple

Do not use embeddings.
Do not add vector search.
Do not call LLM for relevance matching in this task.

---

## TASK-B2: Use stable ids for references

### Goal

ExecutableTaskCandidate references should use ids, not free-form labels, where possible.

### Required fields

```python
required_rules: list[str]
required_decision_criteria: list[str]
required_procedures: list[str]
```

These should contain ids of related items where possible.

If legacy data only has labels, preserve labels as fallback.

---

## TASK-B3: Make SimulationTester check executable task completeness generically

### Update

```text
src/domain_discovery_engine/agents/simulation_tester.py
```

### Required generic checks

For each executable task candidate:

- if required_inputs is empty, create unknown: 入力情報が未定義
- if expected_outputs is empty, create unknown: 出力情報が未定義
- if required_rules is empty, create unknown: 業務ルールが未定義
- if required_decision_criteria is empty, create unknown: 判断基準が未定義
- if task has review/判断/評価 semantics but no review condition, create unknown: レビュー条件が未定義

### Keep existing domain-specific checks

Do not remove existing experiment/reservation/purchasing checks yet.

But generic executable-task completeness checks must run for all candidates.

---

## TASK-B4: Update QuestionGenerator priority

### Update

```text
src/domain_discovery_engine/agents/question_generator.py
```

### Priority order

1. missing decision criteria
2. missing business rules
3. missing required inputs
4. missing expected outputs
5. missing review or exception conditions
6. lower-level UI or implementation format

### User-facing language

Questions must be Japanese by default.

Do not expose internal names such as:

```text
BusinessCapabilityModel
ExecutableTaskCandidate
schema
IR
metadata
```

Good:

```text
見積候補を評価するとき、どの情報を必ず入力として使いますか？
例: 品名、仕様、単位、数量、候補カタログ、過去実績など
```

---

## TASK-B5: Normalize LLM task candidate output format

### Update

```text
src/domain_discovery_engine/agents/task_candidate_extractor.py
prompts/internal/task_candidate_extractor.md
```

### Required output format

LLM output must be a JSON object:

```json
{
  "items": [
    {
      "label": "見積候補を評価する",
      "description": "候補カタログを仕様・単位・価格差などで評価する",
      "task_type": "unknown",
      "required_inputs": ["見積明細", "候補カタログ"],
      "expected_outputs": ["評価結果", "レビュー対象"],
      "required_rules": [],
      "required_decision_criteria": [],
      "required_procedures": []
    }
  ]
}
```

Do not ask LLM to return a top-level JSON list.

---

## TASK-B6: Add tests for generic task completeness

Add tests for:

1. ExecutableTaskCandidate with missing inputs generates unknown
2. Missing outputs generates unknown
3. Missing decision criteria generates unknown
4. Missing business rules generates unknown
5. QuestionGenerator asks Japanese questions for missing business capability information
6. Unrelated rules are not attached to unrelated task candidates

---

## Run B Acceptance Criteria

Run B is complete when:

- All tests pass
- Task candidates do not receive unrelated rules/criteria/procedures by default
- SimulationTester detects generic completeness gaps
- QuestionGenerator prioritizes business capability gaps
- LLM task candidate output uses `{"items": [...]}`

Stop after Run B if tests become unstable.

---

# Run C: CLI and Documentation Hardening

## TASK-C1: Improve CLI output

### Update

```text
src/domain_discovery_engine/interfaces/cli.py
```

### Add display sections

```text
業務ルール（BusinessRule）
判断基準（DecisionCriterion）
業務手順（BusinessProcedure）
入出力仕様（InputOutputSpec）
実行可能タスク候補（ExecutableTaskCandidate）
未解決事項（Unknown）
```

### Requirements

- Output must be readable by Japanese business users.
- Preserve Japanese business labels.
- Do not show raw JSON by default.
- Do not expose internal metadata by default.

---

## TASK-C2: Add Japanese project direction doc

### Create or update

```text
docs/project_direction.md
```

### Must include

- DomainDiscoveryEngineは、対話から業務知識を構造化する前段エンジンである
- 業務能力は、業務ルール（BusinessRule）、判断基準（DecisionCriterion）、業務手順（BusinessProcedure）、制約（Constraint）、ノウハウを含む
- DDEは、業務能力モデル（BusinessCapabilityModel）と実行可能タスク候補（ExecutableTaskCandidate）を整理する
- Skill / MCP Tool / API / Workflow / Agent への変換は、このフェーズでは対象外

### Must not include

- FY2026
- 2026年度目標
- 今年度目標
- annual goal
- goal-setting

---

## TASK-C3: Add Japanese business capability model doc

### Create or update

```text
docs/business_capability_model.md
```

### Required sections

```markdown
# 業務能力モデル（BusinessCapabilityModel）

## 目的

## 構成要素

## 業務ルール（BusinessRule）

## 判断基準（DecisionCriterion）

## 業務手順（BusinessProcedure）

## 入出力仕様（InputOutputSpec）

## 実行可能タスク候補（ExecutableTaskCandidate）

## ドメインモデル（DomainModel）との関係

## 対象外
```

Keep official schema/class names in English inside parentheses.

---

## TASK-C4: Update README human-facing sections

### Requirements

- Add Japanese overview section.
- Keep package/command examples as-is.
- Explain the new Business Capability direction.
- Use fixed Japanese/English concept pairs.
- Do not mention annual goals.

---

## TASK-C5: Remove annual goal references

### Search and remove or rewrite

```text
FY2026
2026年度目標
今年度目標
今年度の目標
annual goal
goal-setting
```

Do not create `docs/fy2026_direction.md`.

---

## TASK-C6: Add docs tests or lightweight checks

Add tests or simple assertions that verify:

1. `docs/project_direction.md` exists
2. `docs/business_capability_model.md` exists
3. Docs do not contain annual goal references
4. Docs contain fixed concept pairs such as `業務能力モデル（BusinessCapabilityModel）`
5. README does not contain annual goal references

---

## Run C Acceptance Criteria

Run C is complete when:

- All tests pass
- CLI shows business capability sections
- docs are Japanese-centered
- formal class/schema names remain English
- annual goal references are removed
- README reflects project direction without FY2026/annual goal references

---

# Global Non-goals

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
- Vector search
- Embedding-based relevance matching

---

# Final Acceptance Criteria

The overall task is complete when:

1. All tests pass
2. Existing DomainModel behavior remains available
3. BusinessCapabilityModel remains available
4. MemoryItem supports structured metadata
5. BusinessCapabilityBuilder uses metadata first
6. description pseudo-metadata is only backward compatibility fallback
7. TaskCandidateExtractor does not blindly attach unrelated rules/criteria/procedures
8. SimulationTester performs generic executable task completeness checks
9. QuestionGenerator asks Japanese clarification questions about business capability gaps
10. CLI displays business capability information clearly
11. docs/project_direction.md exists and is Japanese-centered
12. docs/business_capability_model.md exists and is Japanese-centered
13. README is updated for Japanese users
14. No documentation mentions FY2026 or annual goal planning
15. No downstream artifact generation is implemented
