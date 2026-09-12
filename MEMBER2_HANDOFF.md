# CityFlow — Member 2 Handoff

## Ownership

Member 2 owns the reasoning layer:
1. Intent understanding (parsing the user's question)
2. Connecting to Member 1's RAG retrieval layer
3. Multi-step reasoning: parse intent → retrieve → check edge cases → generate checklist
4. Edge-case handling (home-based, food service, night operations, signboard)
5. Grounded checklist generation (no invented requirements, fees, or timelines)
6. Fallback behavior when evidence is insufficient

This matches the team division: Member 2 owns intent understanding, multi-step reasoning, edge cases, and final checklist generation.

## Interface for Member 3 (UI) and Member 4 (QA/Integration)

```python
from agent import generate_checklist

result = generate_checklist("I want to open a small restaurant in Gulberg, Lahore. What do I need?")
```

Only one function needs to be called: `generate_checklist(question: str, k: int = 5)`. Everything else (intent parsing, calling Member 1's retriever, edge-case checks) happens internally.

## Output schema

`generate_checklist()` always returns a dict with this exact shape:

```python
{
    "sufficient_evidence": true or false,
    "summary": "one sentence summary of what this checklist covers",
    "checklist": [
        {
            "step": 1,
            "requirement": "string",
            "department": "string or null",
            "cost": "string or null",
            "timeline": "string or null",
            "source": "string (source document name)"
        }
    ],
    "notes": ["list of strings — edge-case flags or gaps in the evidence"]
}
```

### Field notes for Member 3 (UI display)
- `sufficient_evidence: false` means the checklist is intentionally empty — this is the fallback state. Display a clear "not enough information" message instead of an empty table.
- `department`, `cost`, and `timeline` can be `null` — the evidence doesn't always contain these. Display "Not specified" or hide the field rather than showing blank/null.
- `source` should be shown as a citation next to each requirement — this is a core project requirement (source citations for trust/accuracy).
- `notes` often contains useful caveats (e.g. "municipal trade licenses may also be required but aren't covered in these documents") — worth surfacing to the user, not just logging.

### Field notes for Member 4 (QA)
- Tested and working scenarios so far: normal restaurant registration, home-based food business, night operations, informal phrasing ("food stall" vs "restaurant"), and out-of-scope fallback (non-permit questions correctly return `sufficient_evidence: false`).
- If you find a question that should have evidence but returns `sufficient_evidence: false`, it's likely a retrieval-matching issue — flag it with the exact question text so we can check if it's a phrasing/embedding issue or a genuine knowledge_base gap.
- If a checklist item appears with a "made up" cost/timeline not present in `knowledge_base/`, that's a grounding failure — flag immediately with the exact question and output.

## Dependencies

In addition to Member 1's requirements, this module needs:
```
groq
```
Requires `GROQ_API_KEY` set as an environment variable (or Colab secret).

## Manual test

```bash
python agent.py
```
Runs a built-in sample question and prints the JSON output.

## Integration note

This module imports Member 1's pipeline directly:
```python
from rag.pipeline import Member1RAGPipeline
```
No changes were made to any file in `rag/`, `knowledge_base/`, `scripts/`, or `tests/` — this is a self-contained addition (`agent.py` at the repo root) with no structural changes to the existing project layout.
