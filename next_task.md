# NEXT TASK: Prompt Language Policy and Japanese User Experience

## Objective

Update DomainDiscoveryEngine so that it uses English prompts for internal LLM reasoning while preserving a Japanese user experience.

The target users are Japanese business users. They will describe their business ideas in Japanese and expect clarification questions and summaries in Japanese.

However, internal LLM prompts for domain modeling, extraction, and simulation should remain in English because these prompts use software engineering and domain modeling concepts such as:

- Domain Model
- Concept
- Task
- Constraint
- Assumption
- Decision
- Unknown
- Simulation Test
- Break Test
- Acceptance Criteria

The system must clearly separate:

1. Internal prompt language
2. Schema/internal data structure language
3. User-facing output language

Do not redesign the DDE architecture.

---

## Background

The current implementation already has:

- Rule-based and LLM modes
- Prompt externalization
- AzureChatOpenAI based LLMProvider
- Docker support
- ProjectMemory
- DomainModel
- SimulationTester
- QuestionGenerator

The next step is to define and enforce the language policy.

The company OpenAI environment should continue to use the existing AzureChatOpenAI implementation style already introduced in the project, consistent with the provided internal example.

---

## Language Policy

### 1. Internal schemas must stay English

Keep schema field names and class names in English.

Examples:

```python
ProjectMemory
MemoryItem
DomainModel
Concept
Task
Constraint
Assumption
Decision
Unknown
SimulationResult
ClarifyingQuestion
```

Do not translate schema fields into Japanese.

Bad:

```python
class 業務概念:
    ...
```

Good:

```python
class Concept:
    ...
```

---

### 2. Internal prompts should be English by default

The following prompts should remain English:

- dialogue_analyzer.md
- domain_model_builder.md
- simulation_tester.md

Reason:

These agents operate on structured concepts used in software engineering and domain modeling. English prompts are expected to be more stable for these internal tasks.

---

### 3. User-facing prompts should produce Japanese

The following prompts must explicitly instruct the LLM to produce Japanese output:

- question_generator.md
- response_composer.md, if implemented

The generated clarification questions must be natural Japanese.

Bad:

```text
Please define the similarity criteria.
```

Good:

```text
過去の実験を探すとき、何が近いものを「似ている」と判断しますか？
例: 試料、実験条件、測定値、目的、担当者など
```

---

### 4. User-provided domain labels must preserve original Japanese

If the user says:

```text
実験条件と結果を記録したい
```

The extracted concepts should preserve Japanese labels:

```json
{
  "concepts": [
    {
      "label": "実験条件"
    },
    {
      "label": "実験結果"
    }
  ]
}
```

Do not translate domain labels to English unless explicitly requested.

Bad:

```json
{
  "label": "experiment condition"
}
```

Good:

```json
{
  "label": "実験条件"
}
```

---

## TASK-25: Add Prompt Language Policy Document

### Create

```text
docs/prompt_language_policy.md
```

### Content requirements

Document the following:

- Internal prompts are English by default
- User-facing outputs are Japanese by default
- Schema names remain English
- Domain labels from user input must preserve original language
- Japanese users are the primary target users
- Future multilingual support should be handled via configuration, not by changing schemas

---

## TASK-26: Reorganize Prompt Directory

### Goal

Make prompt language separation explicit.

### Required structure

```text
prompts/
  internal/
    dialogue_analyzer.md
    domain_model_builder.md
    simulation_tester.md

  user_facing/
    question_generator.md
    response_composer.md
```

If `response_composer.md` is not implemented yet, create it as a placeholder prompt.

### Requirements

- Update prompt loading code to use the new paths
- Tests must pass
- Existing LLM mode must still work
- Rule-based mode must still work

---

## TASK-27: Update Prompt Files

### dialogue_analyzer.md

Must be written in English.

Must explicitly instruct:

- Analyze Japanese or English user input
- Extract structured items
- Preserve user language for labels and descriptions
- Return JSON only
- Do not invent confirmed facts
- Separate inferred assumptions from user-confirmed facts

### domain_model_builder.md

Must be written in English.

Must explicitly instruct:

- Build a domain model from ProjectMemory
- Preserve Japanese business terms
- Do not translate user-provided labels
- Distinguish confirmed items from candidate items
- Keep unresolved issues visible

### simulation_tester.md

Must be written in English.

Must explicitly instruct:

- Run business scenario simulation
- Identify missing concepts, tasks, constraints, and relations
- Generate unknowns, not final answers
- Preserve Japanese labels

### question_generator.md

Can be written in Japanese or bilingual.

Must explicitly instruct:

- Generate Japanese clarification questions
- Use polite but concise Japanese
- Ask one high-priority question at a time unless multiple are strongly related
- Explain briefly why the question matters
- Include concrete examples where helpful
- Avoid technical jargon such as "Domain Model", "Entity", "IR", "Schema"

### response_composer.md

If implemented, must explicitly instruct:

- Summarize current understanding in Japanese
- Show confirmed items and unresolved items separately
- Avoid exposing internal implementation details
- Do not mention LLM, schema, JSON, or internal prompts to the business user

---

## TASK-28: Add User Locale Configuration

### Goal

Make user-facing output language configurable.

### Add environment variable

```env
DDE_USER_LOCALE=ja-JP
```

Default:

```text
ja-JP
```

### Update

- `.env.example`
- AppConfig
- README
- Docker documentation if present

### Behavior

If `DDE_USER_LOCALE=ja-JP`, clarification questions must be generated in Japanese.

Future locales can be added later. Do not implement full multilingual support now.

---

## TASK-29: Add Tests for Japanese User Experience

### Create or update tests

Add tests that verify:

1. Japanese user input remains Japanese in extracted labels
2. QuestionGenerator returns Japanese text
3. Internal schema fields remain English
4. Prompt files exist in the new directory structure
5. `DDE_USER_LOCALE` defaults to `ja-JP`

### Example test input

```text
実験条件と結果を記録して、過去の似た実験を探せるようにしたい
```

### Expected examples

Concept labels should include:

```text
実験条件
実験結果
実験
```

Question should be Japanese, for example:

```text
過去の実験を探すとき、何を基準に「似ている」と判断しますか？
```

The exact wording does not need to match, but it must be Japanese and user-facing.

---

## TASK-30: Update README

Add a section:

```markdown
## Prompt and Language Policy
```

Include:

- The target user language is Japanese
- Internal prompts use English for technical stability
- User-facing questions and summaries are Japanese
- User-provided business terms are preserved in their original language
- `DDE_USER_LOCALE=ja-JP` controls user-facing language

---

## Non-goals

Do not implement:

- IR generation
- Application generation
- Deployment engine beyond existing Docker runtime
- Full multilingual UI
- Translation of all internal prompts into Japanese
- Schema renaming into Japanese
- Database migration
- Knowledge graph storage
- Neo4j integration

---

## Acceptance Criteria

The implementation is complete when:

1. All tests pass
2. Rule-based mode still works
3. LLM mode still works
4. Prompt directories are separated into `internal/` and `user_facing/`
5. Japanese user input is preserved in labels
6. Clarification questions are generated in Japanese by default
7. README clearly explains the language policy
8. `.env.example` includes `DDE_USER_LOCALE=ja-JP`
9. Docker execution still works

---

## Recommended Codex Scope

For the next Codex run, implement only:

- TASK-25
- TASK-26
- TASK-27
- TASK-28
- TASK-29
- TASK-30

Do not start evaluation framework work yet.

Focus only on prompt language policy and Japanese user experience.
