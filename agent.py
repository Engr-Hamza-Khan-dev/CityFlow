"""
CityFlow — Member 2 (AI/Agent Engineer) reasoning pipeline.

Pipeline: parse_intent -> retrieve (Member 1) -> check_edge_cases -> generate_checklist

This module owns NO retrieval logic itself. It only calls
rag.pipeline.Member1RAGPipeline.retrieve() and reasons over the results.
"""

import json
import os
from typing import Any, Dict, List, Optional

from groq import Groq
from rag.pipeline import Member1RAGPipeline

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
GROQ_MODEL = "openai/gpt-oss-120b"  # confirm current model name in Groq console

rag = Member1RAGPipeline()
rag.ensure_index()  # builds the FAISS index on first run if it doesn't exist


# ---------------------------------------------------------------------------
# Step 1: Intent parsing
# ---------------------------------------------------------------------------

INTENT_PROMPT = """You are an intent parser for a Lahore small-business permit assistant.
Given a user's question, extract structured details. Respond with ONLY valid JSON,
no preamble, no markdown fences.

JSON shape:
{{
  "business_type": "string or null (e.g. restaurant, retail shop, home-based, food truck)",
  "location_hint": "string or null (area/zone in Lahore if mentioned)",
  "concern": "one of: new_registration, renewal, requirements, cost, timeline, general",
  "special_conditions": ["list of relevant flags from: home_based, food_service, night_operations, signboard, none"]
}}

User question: {question}
"""


def parse_intent(question: str) -> Dict[str, Any]:
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": INTENT_PROMPT.format(question=question)}],
        temperature=0,
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: treat as a generic query if the model didn't return clean JSON
        return {
            "business_type": None,
            "location_hint": None,
            "concern": "general",
            "special_conditions": [],
        }


# ---------------------------------------------------------------------------
# Step 2: Retrieval (delegates entirely to Member 1)
# ---------------------------------------------------------------------------

def retrieve_evidence(question: str, intent: Dict[str, Any], k: int = 5) -> List[Dict[str, Any]]:
    # Build a slightly enriched query using parsed intent, still just a string
    # to Member 1's retrieve() -- we don't touch their internals.
    query_parts = [question]
    if intent.get("business_type"):
        query_parts.append(intent["business_type"])
    for cond in intent.get("special_conditions", []):
        if cond and cond != "none":
            query_parts.append(cond.replace("_", " "))

    enriched_query = " ".join(query_parts)
    return rag.retrieve(enriched_query, k=k)


# ---------------------------------------------------------------------------
# Step 3: Edge-case flags (kept simple and explicit for hackathon scope)
# ---------------------------------------------------------------------------

def check_edge_cases(intent: Dict[str, Any]) -> List[str]:
    """Return human-readable notes to feed into the checklist prompt."""
    notes = []
    conditions = intent.get("special_conditions", [])

    if "home_based" in conditions:
        notes.append("This is a home-based business — check for any zoning or residential-use restrictions.")
    if "food_service" in conditions:
        notes.append("This involves food service — check for Punjab Food Authority health/sanitary requirements in addition to the general trade license.")
    if "night_operations" in conditions:
        notes.append("This involves night operations — check for any operating-hours restrictions or additional approvals.")
    if "signboard" in conditions:
        notes.append("A signboard/advertisement may be involved — check for separate signboard permit requirements.")

    return notes


# ---------------------------------------------------------------------------
# Step 4: Checklist generation (grounded strictly in retrieved evidence)
# ---------------------------------------------------------------------------

CHECKLIST_PROMPT = """You are CityFlow, an assistant that turns official Lahore government
documents into a clear permit checklist for small business owners.

STRICT RULES:
- Only use information present in the EVIDENCE below. Do not invent requirements, fees, or timelines.
- If the evidence does not contain enough information to answer, set "sufficient_evidence" to false
  and leave the checklist empty -- do not guess.
- Every checklist item must cite its source (from the evidence's "source" field).

Respond with ONLY valid JSON, no preamble, no markdown fences.

JSON shape:
{{
  "sufficient_evidence": true or false,
  "summary": "one sentence summary of what this checklist covers",
  "checklist": [
    {{
      "step": 1,
      "requirement": "string",
      "department": "string or null",
      "cost": "string or null",
      "timeline": "string or null",
      "source": "string (from evidence source field)"
    }}
  ],
  "notes": ["any edge-case notes relevant to this business"]
}}

User question: {question}

Edge case notes to consider: {edge_notes}

EVIDENCE:
{evidence_text}
"""


def format_evidence(evidence: List[Dict[str, Any]]) -> str:
    if not evidence:
        return "(no evidence retrieved)"
    lines = []
    for item in evidence:
        lines.append(f"- Source: {item['source']}\n  Text: {item['text']}")
    return "\n".join(lines)


def generate_checklist(question: str, k: int = 5) -> Dict[str, Any]:
    intent = parse_intent(question)
    evidence = retrieve_evidence(question, intent, k=k)
    edge_notes = check_edge_cases(intent)

    if not evidence:
        return {
            "sufficient_evidence": False,
            "summary": "No relevant information found in the knowledge base for this question.",
            "checklist": [],
            "notes": edge_notes,
        }

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{
            "role": "user",
            "content": CHECKLIST_PROMPT.format(
                question=question,
                edge_notes="; ".join(edge_notes) if edge_notes else "none",
                evidence_text=format_evidence(evidence),
            ),
        }],
        temperature=0,
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "sufficient_evidence": False,
            "summary": "The system could not generate a valid checklist from the available information.",
            "checklist": [],
            "notes": edge_notes,
        }

    return result


# ---------------------------------------------------------------------------
# Quick manual test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_question = "I want to open a small restaurant in Gulberg, Lahore. What do I need?"
    result = generate_checklist(test_question)
    print(json.dumps(result, indent=2))
