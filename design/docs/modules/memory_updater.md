# Module: MemoryUpdater

## Responsibility

Merge newly extracted or simulated items into ProjectMemory.

## Input

- current ProjectMemory
- DialogueExtraction or SimulationResult

## Output

- updated ProjectMemory

## Merge rules

1. If an equivalent item already exists, update confidence/evidence rather than creating a duplicate.
2. User-confirmed facts have priority over AI-inferred candidates.
3. Rejected items should not be re-added unless the user explicitly reopens them.
4. Contradictions should become contradiction items, not silent overwrites.
5. Unknowns should be deduplicated and prioritized later by QuestionGenerator.

## Equivalence examples

These likely refer to the same concept:

- 実験結果
- 結果データ
- 測定結果

But do not automatically merge if meaning may differ.

## Key design rule

ProjectMemory is an audit trail of understanding, not just the latest summary.
