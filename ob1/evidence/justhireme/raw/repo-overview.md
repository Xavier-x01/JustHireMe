# JustHireMe — Raw Evidence Capture

**Source:** JustHireMe v0.1-alpha (vasu-devs/justhireme)
**Domain:** job-intelligence
**Type:** evidence
**Importance:** high
**Tags:** semantic-primitive, quality-gate, ranking, lead-normalization, profile-matching, agentic-workflow
**Captured:** 2026-05-07

---

## Project Identity

**Tagline:** Local-first, open-source AI job intelligence workbench.
**Core claim:** Automates the full job-seeking pipeline — scrape → gate → rank → customize → track — entirely on device with no cloud sync.

## Four-Stage Pipeline

```
1. Scrape      → Scout agent pulls from ATS boards, RSS, HN, Reddit, APIs, custom URLs
2. Gate        → Quality gate filters stale, thin, spammy, senior-only, unpaid postings
3. Rank        → Multi-factor fit score (deterministic rubric + optional LLM + vectors + feedback)
4. Customize   → Tailored resume PDF, cover letter PDF, founder/cold email, LinkedIn outreach
```

## Execution Modes

| Mode        | Description                                                   |
|-------------|---------------------------------------------------------------|
| Ghost Mode  | Fully autonomous — scans every 6h, applies without approval   |
| Sniper Mode | Human-in-the-loop — pauses after evaluation for manual review |

## Tech Stack

| Layer     | Technology                                               |
|-----------|----------------------------------------------------------|
| Frontend  | React 19 + TypeScript + Vite + Tailwind + Framer Motion  |
| Backend   | Python 3.13 + FastAPI + WebSockets                       |
| Desktop   | Tauri 2 (Rust parent process)                            |
| CRM DB    | SQLite                                                   |
| Graph DB  | Kuzu (candidate profile graph)                           |
| Vector DB | LanceDB (semantic embeddings)                            |
| Agents    | LangGraph DAGs                                           |
| Optional  | Ollama (local LLMs), Playwright (browser automation)     |

## Lead Object Schema (SQLite `leads` table)

```json
{
  "job_id": "md5_hash_of_url",
  "title": "Senior Backend Engineer",
  "company": "Acme Corp",
  "url": "https://...",
  "platform": "greenhouse|lever|scout|hn_hiring|...",
  "status": "discovered|evaluating|tailoring|approved|applied|rejected|discarded|matched|bidding|proposal_sent|awarded|completed",
  "score": 87,
  "reason": "Strong FastAPI/Python match, but missing Kubernetes",
  "match_points": ["Built Waldo RAG pipeline", "FastAPI production experience"],
  "gaps": ["Kubernetes / container orchestration"],
  "description": "...",
  "asset_path": "/path/to/tailored_resume.pdf",
  "cover_letter_path": "/path/to/cover_letter.pdf",
  "selected_projects": "Waldo (RAG), Vaani (voice agent)",
  "kind": "job|freelance",
  "budget": "$500-1000 or hourly $50-80",
  "created_at": "2026-05-07T..."
}
```

## Candidate Graph Schema (Kuzu)

```
Nodes:
  Candidate   {id, name, summary}
  Experience  {role, company, period, description}
  Project     {title, stack, repo_url, impact}
  Skill       {name, category}
  JobLead     {job_id, title, company, url, platform}

Edges:
  Candidate  -[WORKED_AS]->  Experience
  Candidate  -[BUILT]->      Project
  Experience -[UTILIZES]->   Skill
  Project    -[UTILIZES]->   Skill
  JobLead    -[REQUIRES]->   Skill
```

## Agent Modules

| Agent                | Location                             | Role                                              |
|----------------------|--------------------------------------|---------------------------------------------------|
| Ingestor             | agents/ingestor.py                   | Resume/LinkedIn/GitHub → Kuzu graph               |
| LinkedIn Parser      | agents/linkedin_parser.py            | LinkedIn data export ZIP → structured entities    |
| GitHub Ingestor      | agents/github_ingestor.py            | GitHub repos → project objects with stack+impact  |
| Scout                | agents/scout.py                      | Multi-source scraping → normalized leads          |
| Free Scout           | agents/free_scout.py                 | No-API scraping fallback                          |
| Quality Gate         | agents/quality_gate.py               | Filter bad leads before ranking                   |
| Evaluator            | agents/evaluator.py                  | GraphRAG proof-of-work scoring (0–100)            |
| Semantic             | agents/semantic.py                   | LanceDB vector similarity matching               |
| Scoring Engine       | agents/scoring_engine.py             | Multi-factor final score assembly                 |
| Feedback Ranker      | agents/feedback_ranker.py            | Learn from approve/reject signals                 |
| Generator            | agents/generator.py                  | PDF resume, cover letter, outreach drafts         |
| Actuator             | agents/actuator.py                   | Experimental Playwright form filling (lab only)   |
| Query Gen            | agents/query_gen.py                  | Profile → LLM-generated site: search queries      |
| Freelance Scout      | agents/freelance_scout.py            | Upwork RSS, Freelancer API, Toptal/Arc/Contra     |
| Freelance Query Gen  | agents/freelance_query_gen.py        | No seniority queries; proof-of-work focus         |
| Freelance Evaluator  | agents/freelance_evaluator.py        | Projects weighted 3x; budget reality check        |

## Quality Gate Criteria

```python
url_exists()      # Reject if URL missing
posting_depth()   # Penalize thin snippets
freshness()       # Penalize stale jobs (>30 days)
seniority_check() # Reject senior-only if candidate is mid/junior
red_flags()       # Penalize unpaid, commission, homework, exposure
context()         # Penalize missing company or unclear source

Returns: {pass: bool, reason: str, penalty_score: 0-100}
```

## WebSocket Event Types

```python
{"type": "agent",         "event": "scout_start",  "msg": "..."}
{"type": "agent",         "event": "scout_done",   "msg": "Found 42 leads"}
{"type": "agent",         "event": "eval_scored",  "msg": "Scored X = 87/100"}
{"type": "LEAD_UPDATED",  "data": {job_id, title, company, score, reason, ...}}
{"type": "FREELANCE_LEAD_UPDATED", "data": {...}}
```

## Source Adapter Contract

```python
def run(urls: list[str], ...) -> list[dict]:
    # Scrape (Playwright / RSS / API)
    # Parse to normalized lead dict
    # url_exists() dedup check
    # save_lead() if new
    # Return list of new leads
```

## MCP Server

`backend/mcp_server.py` — exposes agent tools as MCP-callable endpoints, enabling external agents (Claude, Cursor, etc.) to trigger pipeline stages programmatically.

## Roadmap Milestones

| Version | Focus                                                     |
|---------|-----------------------------------------------------------|
| v0.1    | OSS release: scraper → ranker → vector → customizer       |
| v0.2    | Source ecosystem: more ATS adapters, quality dashboards   |
| v0.3    | Ranking benchmarks, feedback learning, semantic UI        |
| Future  | OS keychain, cross-platform, hosted source catalog        |
