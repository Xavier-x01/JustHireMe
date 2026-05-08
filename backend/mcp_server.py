"""Minimal MCP stdio server for JustHireMe's local job intelligence tools.

This deliberately avoids an SDK dependency so the repo can expose useful MCP
tools with the existing backend environment. It implements the JSON-RPC methods
needed by MCP clients: initialize, tools/list, and tools/call.
"""

from __future__ import annotations

import json
import sys
from typing import Any, Callable

from agents.evaluator import score as score_fit
from agents.lead_intel import (
    budget_from_text,
    company_from_text,
    location_from_text,
    signal_quality,
    tech_stack_from_text,
    urgency_from_text,
)
from agents.quality_gate import evaluate_lead_quality
from db.client import memory_capture, memory_recall, memory_update


Json = dict[str, Any]


def _text(value: Any) -> str:
    return str(value or "").strip()


def _tool_result(data: Any) -> Json:
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(data, ensure_ascii=False, indent=2, default=str),
            }
        ],
        "isError": False,
    }


def _error_result(message: str) -> Json:
    return {"content": [{"type": "text", "text": message}], "isError": True}


def _score_job_fit(args: Json) -> Json:
    posting = _text(args.get("posting"))
    candidate = args.get("candidate")
    if not posting:
        return _error_result("posting is required")
    if not isinstance(candidate, dict):
        return _error_result("candidate must be a JSON object")
    return _tool_result(score_fit(posting, candidate))


def _evaluate_lead(args: Json) -> Json:
    lead = args.get("lead")
    if not isinstance(lead, dict):
        return _error_result("lead must be a JSON object")
    quality = evaluate_lead_quality(
        lead,
        min_quality=int(args.get("min_quality") or 60),
        target_level=_text(args.get("target_level")) or "beginner",
        max_age_days=int(args.get("max_age_days") or 7),
    )
    return _tool_result(quality)


def _extract_lead_intel(args: Json) -> Json:
    text = _text(args.get("text"))
    if not text:
        return _error_result("text is required")
    return _tool_result(
        {
            "company": company_from_text(text),
            "location": location_from_text(text),
            "budget": budget_from_text(text),
            "urgency": urgency_from_text(text),
            "tech_stack": tech_stack_from_text(text),
            "signal_quality": signal_quality(text),
        }
    )


def _memory_capture(args: Json) -> Json:
    content = _text(args.get("content"))
    if not content:
        return _error_result("content is required")
    surface = _text(args.get("surface")) or "auto"
    try:
        result = memory_capture(
            surface=surface,
            content=content,
            summary=_text(args.get("summary")),
            tags=args.get("tags") if isinstance(args.get("tags"), list) else None,
            priority=int(args.get("priority") or 0),
        )
        return _tool_result(result)
    except ValueError as exc:
        return _error_result(str(exc))


def _memory_recall(args: Json) -> Json:
    query = _text(args.get("query")) or None
    try:
        return _tool_result(memory_recall(query=query))
    except Exception as exc:
        return _error_result(str(exc))


def _memory_update(args: Json) -> Json:
    item_id = _text(args.get("id"))
    if not item_id:
        return _error_result("id is required")
    kwargs: dict[str, Any] = {}
    if "status" in args:
        kwargs["status"] = _text(args["status"])
    if "content" in args:
        kwargs["content"] = _text(args["content"])
    if "summary" in args:
        kwargs["summary"] = _text(args["summary"])
    if "priority" in args:
        kwargs["priority"] = int(args["priority"])
    try:
        return _tool_result(memory_update(item_id, **kwargs))
    except ValueError as exc:
        return _error_result(str(exc))


TOOLS: dict[str, Callable[[Json], Json]] = {
    "score_job_fit": _score_job_fit,
    "evaluate_lead_quality": _evaluate_lead,
    "extract_lead_intel": _extract_lead_intel,
    "memory_capture": _memory_capture,
    "memory_recall": _memory_recall,
    "memory_update": _memory_update,
}


TOOL_DEFINITIONS: list[Json] = [
    {
        "name": "score_job_fit",
        "description": "Score a job posting against a candidate profile using JustHireMe's explainable fit rubric.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "posting": {"type": "string", "description": "Raw job posting text."},
                "candidate": {"type": "object", "description": "Candidate profile JSON using JustHireMe profile fields."},
            },
            "required": ["posting", "candidate"],
            "additionalProperties": False,
        },
    },
    {
        "name": "evaluate_lead_quality",
        "description": "Run the deterministic lead quality gate before saving or ranking a scraped job lead.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "lead": {"type": "object", "description": "Lead object with title, company, url, description, location, posted_date, and source_meta."},
                "min_quality": {"type": "integer", "minimum": 0, "maximum": 100, "default": 60},
                "target_level": {"type": "string", "default": "beginner"},
                "max_age_days": {"type": "integer", "minimum": 1, "maximum": 365, "default": 7},
            },
            "required": ["lead"],
            "additionalProperties": False,
        },
    },
    {
        "name": "extract_lead_intel",
        "description": "Extract lightweight company, location, budget, urgency, stack, and signal quality from raw lead text.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Raw job or lead text."}
            },
            "required": ["text"],
            "additionalProperties": False,
        },
    },
    {
        "name": "memory_capture",
        "description": (
            "Save a thought, goal, decision, win, or project note to persistent memory. "
            "Use surface='auto' to let the system route by content keywords, or specify one of: "
            "north_star, active_project, decision, brag, thinking."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "Full text of the memory item."},
                "surface": {
                    "type": "string",
                    "description": "Memory surface. Use 'auto' for keyword-based routing.",
                    "enum": ["auto", "north_star", "active_project", "decision", "brag", "thinking"],
                    "default": "auto",
                },
                "summary": {"type": "string", "description": "Optional <=120 char summary. Auto-truncated from content if omitted."},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Optional tag list."},
                "priority": {"type": "integer", "minimum": 0, "maximum": 10, "default": 0, "description": "Higher = shown first in briefings."},
            },
            "required": ["content"],
            "additionalProperties": False,
        },
    },
    {
        "name": "memory_recall",
        "description": (
            "Load structured memory context. Without a query returns all active items grouped by surface "
            "(north_star, active_projects, recent_decisions, recent_brags, thinking). "
            "With a query performs full-text search and returns matching items in query_results."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Optional full-text search query. Omit for full briefing."},
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "memory_update",
        "description": "Archive, supersede, or edit an existing memory item by its id.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "description": "Memory item id returned by memory_capture."},
                "status": {
                    "type": "string",
                    "enum": ["active", "archived", "superseded"],
                    "description": "New status. Use 'archived' to remove from briefings.",
                },
                "content": {"type": "string", "description": "Replacement content."},
                "summary": {"type": "string", "description": "Replacement summary."},
                "priority": {"type": "integer", "minimum": 0, "maximum": 10, "description": "Updated priority."},
            },
            "required": ["id"],
            "additionalProperties": False,
        },
    },
]


def _handle(request: Json) -> Json | None:
    method = request.get("method")
    req_id = request.get("id")

    try:
        if method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "justhireme", "version": "0.1.0"},
            }
        elif method == "notifications/initialized":
            return None
        elif method == "tools/list":
            result = {"tools": TOOL_DEFINITIONS}
        elif method == "tools/call":
            params = request.get("params") or {}
            name = params.get("name")
            args = params.get("arguments") or {}
            if name not in TOOLS:
                raise ValueError(f"Unknown tool: {name}")
            result = TOOLS[name](args if isinstance(args, dict) else {})
        else:
            raise ValueError(f"Unsupported method: {method}")
        return {"jsonrpc": "2.0", "id": req_id, "result": result}
    except Exception as exc:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32603, "message": str(exc)},
        }


def main() -> None:
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            request = json.loads(line)
            response = _handle(request)
        except Exception as exc:
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": str(exc)},
            }
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
