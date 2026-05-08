# JustHireMe — Claude Agent Guide

## What this repo is

Local-first AI job intelligence workbench. Scrapes leads, runs a quality gate, scores fit against your profile graph, generates tailored applications. No cloud. All data stays on your machine.

Key directories:

| Path | Purpose |
|---|---|
| `backend/agents/` | All pipeline agents (scout, gate, evaluator, generator, …) |
| `backend/db/client.py` | SQLite + Kuzu + LanceDB access |
| `backend/mcp_server.py` | MCP stdio server — 6 tools |
| `backend/main.py` | FastAPI sidecar (REST + WebSocket) |
| `ob1/governed-state/` | Canonical governed truths and authority rules |
| `ob1/prepared-context/` | Semantic primitives, schemas, skill taxonomy |

---

## MCP Tools Reference

Start the server: `backend/.venv/bin/python backend/mcp_server.py`

### Job intelligence (existing)

| Tool | What it does |
|---|---|
| `score_job_fit` | Score a posting against a candidate profile JSON |
| `evaluate_lead_quality` | Deterministic quality gate (freshness, depth, seniority, red flags) |
| `extract_lead_intel` | Extract company, location, budget, urgency, stack from raw text |

### Structured memory (new)

| Tool | What it does |
|---|---|
| `memory_capture` | Save a thought to a named surface |
| `memory_recall` | Load full briefing or FTS search across all surfaces |
| `memory_update` | Archive, supersede, or edit a memory item by id |

---

## Memory Surfaces

| Surface | Use for | Lifespan |
|---|---|---|
| `north_star` | Goals, non-negotiables, what success looks like | Weeks–months |
| `active_project` | Current work items; archive when complete | Days–weeks |
| `decision` | Strategic choices and their rationale | Permanent |
| `brag` | Wins, shipped features, interview progress, closed deals | Permanent |
| `thinking` | Freeform notes, hypotheses, scratch ideas | ~7 days in briefings |

Use `surface: "auto"` and the system routes by keyword:
- "decided / chose / committed to / ruling out" → `decision`
- "shipped / won / accepted / hired / achieved" → `brag`
- "goal: / north star: / my mission" → `north_star`
- "working on / building / project: / milestone" → `active_project`
- everything else → `thinking`

---

## Usage Examples

### Start a session — load context
```json
{ "name": "memory_recall", "arguments": {} }
```
Returns north_star, active_projects, recent_decisions (14d), recent_brags (30d), recent thinking (7d).

### Capture a decision
```json
{
  "name": "memory_capture",
  "arguments": {
    "surface": "decision",
    "content": "Decided to focus exclusively on TypeScript roles for the next 60 days. Python-only roles score below threshold and dilute interview prep.",
    "tags": ["strategy", "typescript"],
    "priority": 8
  }
}
```

### Capture a win
```json
{
  "name": "memory_capture",
  "arguments": {
    "surface": "auto",
    "content": "Got a first-round interview at Acme for Senior Frontend Engineer. Cleared 3 stages so far."
  }
}
```
Routes to `brag` automatically.

### Set a north star goal
```json
{
  "name": "memory_capture",
  "arguments": {
    "surface": "north_star",
    "content": "Goal: land a remote TypeScript/React role at a Series A–B company by end of Q3. Target comp $130–160k.",
    "priority": 10
  }
}
```

### Track an active project
```json
{
  "name": "memory_capture",
  "arguments": {
    "surface": "auto",
    "content": "Working on adding GitHub ingestor to the profile pipeline. Milestone: merged by end of week."
  }
}
```
Routes to `active_project`.

### Search memory
```json
{
  "name": "memory_recall",
  "arguments": { "query": "TypeScript interview" }
}
```

### Archive a completed project
```json
{
  "name": "memory_update",
  "arguments": { "id": "a1b2c3d4e5f6g7h8i9j", "status": "archived" }
}
```

### Supersede an outdated decision
```json
{
  "name": "memory_update",
  "arguments": {
    "id": "old-decision-id",
    "status": "superseded"
  }
}
```
Then capture the replacement with `memory_capture`.

---

## Development patterns

### Agents
- Read the existing agent before changing it (`backend/agents/quality_gate.py`, `scoring_engine.py`, `evaluator.py`)
- Keep scoring deterministic; LLM is an optional bonus layer
- Every score and gate decision must surface a `reason` string

### Database
- `client.py` is the single access point for SQLite, Kuzu, and LanceDB
- New SQL tables go in `_init_sql()` executescript block
- FTS5 virtual tables: create separately in a try/except after executescript
- Memory items live in `memory_items` table; FTS index in `memory_fts`

### MCP server
- Stateless JSON-RPC over stdio — no SDK dependency
- Each tool is a plain function `(args: dict) -> dict` registered in `TOOLS`
- Return `_tool_result(data)` on success, `_error_result(msg)` on validation failure

### Tests
```bash
cd backend
python -m pytest tests/test_mcp_server.py -v
```

---

## Governed rules (from ob1/governed-state/)

- **GT-02**: Quality gate pass required before ranking; decisions are immutable with reason strings
- **GT-03**: Fit scores below 70 surface for human review only
- **GT-04**: Sending applications externally is the only irreversible action
- **AR-03**: Agents CANNOT send applications — human must approve
- **AR-05**: Score threshold changes require owner approval
- Ghost Mode (auto-apply) is OFF by default

---

## Running locally

```bash
# Backend sidecar
cd backend && uv run uvicorn main:app --reload --port 8000

# MCP server (for Claude / IDE agents)
backend/.venv/bin/python backend/mcp_server.py

# Frontend (Tauri dev)
npm run tauri dev
```

Claude config example:
```json
{
  "mcpServers": {
    "justhireme": {
      "command": "/path/to/JustHireMe/backend/.venv/bin/python",
      "args": ["/path/to/JustHireMe/backend/mcp_server.py"],
      "cwd": "/path/to/JustHireMe"
    }
  }
}
```
