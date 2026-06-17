# ProjectMemory Schema

ProjectMemory is the internal state of understanding.

It should preserve uncertainty, evidence, source, and status.

## MemoryItem

```python
from enum import Enum
from pydantic import BaseModel, Field
from typing import Literal

class MemoryItemType(str, Enum):
    GOAL = "goal"
    CONCEPT = "concept"
    TASK = "task"
    RELATION = "relation"
    CONSTRAINT = "constraint"
    ASSUMPTION = "assumption"
    DECISION = "decision"
    UNKNOWN = "unknown"
    REJECTED = "rejected"
    CONTRADICTION = "contradiction"

class MemoryStatus(str, Enum):
    CANDIDATE = "candidate"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    UNRESOLVED = "unresolved"

class MemorySource(str, Enum):
    USER = "user"
    AI_INFERRED = "ai_inferred"
    SIMULATION = "simulation"

class MemoryItem(BaseModel):
    id: str
    type: MemoryItemType
    label: str
    description: str = ""
    status: MemoryStatus = MemoryStatus.CANDIDATE
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    source: MemorySource
    evidence: str = ""
    related_item_ids: list[str] = []
```

## ProjectMemory

```python
class ProjectMemory(BaseModel):
    project_id: str
    title: str = ""
    goals: list[MemoryItem] = []
    concepts: list[MemoryItem] = []
    tasks: list[MemoryItem] = []
    relations: list[MemoryItem] = []
    constraints: list[MemoryItem] = []
    assumptions: list[MemoryItem] = []
    decisions: list[MemoryItem] = []
    unknowns: list[MemoryItem] = []
    rejected_items: list[MemoryItem] = []
    contradictions: list[MemoryItem] = []
```

## Design rule

Never overwrite a user-confirmed item with an AI-inferred item.

If conflict occurs, create a contradiction item and ask the user.
