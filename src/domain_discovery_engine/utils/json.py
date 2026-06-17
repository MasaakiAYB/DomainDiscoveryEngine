from __future__ import annotations

import json


def extract_json_object(text: str) -> dict | list:
    stripped = text.strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        start = min((idx for idx in (stripped.find("{"), stripped.find("[")) if idx != -1), default=-1)
        if start == -1:
            raise
        end = max(stripped.rfind("}"), stripped.rfind("]"))
        if end == -1 or end <= start:
            raise
        return json.loads(stripped[start : end + 1])
