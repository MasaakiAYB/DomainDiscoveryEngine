# Module: ResponseComposer

## Responsibility

Create a user-facing response from the current model state.

## Input

- DomainModel
- unresolved unknowns
- selected question

## Output

Natural language response.

## Response format

Recommended MVP response:

```text
現在の理解では、このシステムは...

重要な概念は...

まだ未確認なのは...

次に確認したいこと:
...
```

## Rules

- Be transparent about AI assumptions.
- Do not pretend candidate items are confirmed.
- Show the current model compactly.
- Ask only one high-priority question by default.
