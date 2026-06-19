# NEXT TASK: Run C Fix - Documentation Formatting and Checks

## Context

Run C has mostly been implemented.

Confirmed as implemented:

- CLI displays Business Capability sections
- `docs/project_direction.md` exists
- `docs/business_capability_model.md` exists
- README contains Japanese overview
- Business Capability direction is reflected in documentation

Remaining issues:

1. Markdown files are too compressed into very few lines, making review and maintenance difficult.
2. Documentation validation tests are missing.
3. GitHub repository About description is still old, but this must be updated manually outside code.

This task is intentionally small.

Do not implement new features.

---

## Important Execution Guidance

The model used for implementation is GPT-5.4 with medium reasoning.

Therefore:

- Keep the scope small.
- Do not redesign the architecture.
- Do not touch BusinessCapabilityModel logic unless required by tests.
- Do not modify LLM prompts unless necessary.
- Do not start Run D or evaluation framework work.
- Prefer simple deterministic tests.

---

# TASK-CF1: Reformat Japanese Markdown Documents

## Goal

Make human-facing Markdown documents readable and maintainable.

## Files to update

```text
README.md
docs/project_direction.md
docs/business_capability_model.md
```

If `design/docs/` exists and contains related design documents, apply the same formatting policy there as well.

## Requirements

- Write human-facing explanations primarily in Japanese.
- Use normal Markdown line breaks and sections.
- Avoid storing an entire document in one very long line.
- Keep official schema/class names in English inside parentheses.
- Preserve command examples and code blocks.

## Required concept pairs

Use these fixed Japanese/English pairs consistently:

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

## Example formatting

Good:

```markdown
# プロジェクトの方向性

DomainDiscoveryEngineは、対話から業務知識を構造化する前段エンジンです。

## 整理する情報

- 業務ルール（BusinessRule）
- 判断基準（DecisionCriterion）
- 業務手順（BusinessProcedure）
- 入出力仕様（InputOutputSpec）
- 実行可能タスク候補（ExecutableTaskCandidate）
```

Bad:

```markdown
# プロジェクトの方向性 DomainDiscoveryEngineは、対話から業務知識を構造化する前段エンジンです。## 整理する情報 - 業務ルール（BusinessRule） - 判断基準（DecisionCriterion） ...
```

---

# TASK-CF2: Add Documentation Validation Tests

## Goal

Add lightweight tests to prevent documentation drift.

## Create

```text
tests/test_documentation_policy.py
```

## Test requirements

Add tests that verify:

1. `docs/project_direction.md` exists.
2. `docs/business_capability_model.md` exists.
3. `README.md` exists.
4. These files do not contain annual-goal references.
5. These files contain required fixed Japanese/English concept pairs.
6. Markdown files are not compressed into too few lines.

## Annual-goal forbidden terms

Documentation must not contain:

```text
FY2026
2026年度目標
今年度目標
今年度の目標
annual goal
goal-setting
```

Apply this check to:

```text
README.md
docs/project_direction.md
docs/business_capability_model.md
```

If `design/docs/` exists, also check Markdown files under it.

## Required concept-pair checks

At minimum, check that the documentation contains:

```text
業務能力モデル（BusinessCapabilityModel）
業務ルール（BusinessRule）
判断基準（DecisionCriterion）
実行可能タスク候補（ExecutableTaskCandidate）
```

These do not all need to appear in every file, but they must appear across the documentation set.

## Markdown readability check

Add a simple line-count check.

For example:

- `docs/project_direction.md` should have at least 10 lines.
- `docs/business_capability_model.md` should have at least 20 lines.
- `README.md` should have at least 20 lines.

Do not over-engineer this.

The goal is to prevent one-line Markdown documents.

---

# TASK-CF3: Keep README User-Facing but Precise

## Goal

README should be understandable for Japanese users while preserving implementation precision.

## Requirements

README should include:

- Short Japanese overview
- Project positioning
- What DDE extracts
- Business Capability direction
- CLI usage
- Docker usage if already present
- Prompt/language policy if already present

Use fixed concept pairs.

Do not mention annual goals.

Do not remove existing command examples unless they are incorrect.

---

# TASK-CF4: Add Manual Note for GitHub About Description

## Goal

Document that GitHub repository About description must be updated manually.

## Update one of:

```text
docs/project_direction.md
```

or

```text
README.md
```

Add a short note for maintainers:

```markdown
## Repository metadata note

GitHubのAbout説明はコード変更では更新されません。
必要に応じて、リポジトリ設定から以下のような説明へ手動更新してください。

対話から業務知識を構造化し、業務能力モデルと実行可能タスク候補へ整理するエンジン。
```

## Important

This is documentation only.

Do not try to update GitHub repository settings from code.

---

# TASK-CF5: Run Tests

## Required command

```bash
pytest
```

All tests must pass.

---

# Non-goals

Do NOT implement:

- Run D
- evaluation framework
- Skill generation
- MCP Tool generation
- API generation
- Workflow execution
- Agent runtime
- UI generation
- IR generation
- Neo4j
- vector search
- embedding search
- new LLM provider behavior
- new schema redesign

---

# Acceptance Criteria

This fix is complete when:

1. `pytest` passes.
2. `README.md` is readable Markdown with proper line breaks.
3. `docs/project_direction.md` is readable Japanese Markdown with proper line breaks.
4. `docs/business_capability_model.md` is readable Japanese Markdown with proper line breaks.
5. `tests/test_documentation_policy.py` exists.
6. Documentation tests check annual-goal forbidden terms.
7. Documentation tests check fixed Japanese/English concept pairs.
8. Documentation tests prevent one-line Markdown documents.
9. No documentation mentions FY2026 or annual goal planning.
10. GitHub About update is documented as a manual repository-setting task.
