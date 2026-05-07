# Job Intelligence — Workflow Definitions

**Domain:** job-intelligence
**Source:** JustHireMe v0.1-alpha
**Type:** prepared-context / workflows

---

## Workflow 1: Full Job Scan Pipeline

```
User: "Scan for Jobs"
        │
        ▼
┌─────────────────────┐
│   Query Generation  │  profile + raw URLs → LLM → site: search queries
│   query_gen.py      │
└────────┬────────────┘
         │ queries: list[str]
         ▼
┌─────────────────────┐
│   Scout             │  Playwright / RSS / API → LLM extraction → raw leads
│   scout.py          │
└────────┬────────────┘
         │ raw leads: list[dict]
         ▼
┌─────────────────────┐
│   Quality Gate      │  6-check filter → pass/fail/penalty
│   quality_gate.py   │
└────────┬────────────┘
         │ clean leads: list[Lead]
         ▼
┌─────────────────────┐
│   Evaluator         │  GraphRAG (Kuzu Cypher + LanceDB) → FitScore
│   evaluator.py      │
└────────┬────────────┘
         │ scored leads
         ▼
┌─────────────────────┐
│   Scoring Engine    │  multi-factor assembly → final score 0-100
│   scoring_engine.py │
└────────┬────────────┘
         │ ranked leads
         ▼
    [Sniper Mode]          [Ghost Mode]
    Pause for review  OR   Auto-approve above threshold
         │
         ▼
┌─────────────────────┐
│   Generator         │  tailored resume + cover letter + outreach PDFs
│   generator.py      │
└─────────────────────┘
```

**State transitions:**
```
discovered → evaluating → tailoring → approved → applied → interviewing → accepted
                                                          → rejected
           → discarded  (quality gate fail or user reject)
```

---

## Workflow 2: Profile Ingestion

```
User uploads resume PDF / LinkedIn ZIP / GitHub handle
        │
        ├── PDF ──────────► ingestor.py
        ├── LinkedIn ZIP ──► linkedin_parser.py
        ├── GitHub ────────► github_ingestor.py
        └── Portfolio ─────► portfolio_ingestor.py
                │
                ▼
         Entity extraction (LLM, step="ingestor")
                │
         ┌──────┴──────┐
         ▼             ▼
    Kuzu graph     LanceDB vectors
    (Candidate,    (skill + project
     Skills,        embeddings)
     Projects,
     Experience)
```

---

## Workflow 3: Freelance Scan (Parallel to Job Scan)

Same as Workflow 1 with these substitutions:

| Component          | Job Variant              | Freelance Variant                      |
|--------------------|--------------------------|----------------------------------------|
| Query Generator    | query_gen.py             | freelance_query_gen.py (no seniority)  |
| Scout              | scout.py                 | freelance_scout.py (Upwork/Freelancer) |
| Evaluator          | evaluator.py             | freelance_evaluator.py (projects 3x)  |
| Budget Check       | N/A                      | budget reality check added             |
| Status Flow        | discovered→applied       | discovered→matched→bidding→awarded     |

---

## Workflow 4: Feedback Learning Loop

```
User approves lead ──► events table: {type: "approve", job_id, score}
User rejects lead  ──► events table: {type: "reject", job_id, score}

Next scan:
  feedback_ranker.py reads events
  ↓
  Adjusts score weights for similar leads
  (same platform, same skill cluster, same company size)
```

---

## Workflow 5: Application Package Generation (Customizer)

```
Lead approved (status = "approved")
        │
        ▼
generator.py receives:
  - lead object (title, company, description, gaps)
  - profile (name, projects, experience, skills)
  - selected_projects (user-chosen or auto-ranked by evaluator)
        │
        ▼
LLM generates tailored content (step="generator"):
  - Resume: emphasize selected_projects, reorder skills to match JD keywords
  - Cover letter: 3 paragraphs, project evidence, company-specific hook
  - Cold email: 150 words, founder-tone, 1 proof point, CTA
  - LinkedIn note: 300 chars, 1 project name, genuine hook
        │
        ▼
PDFs rendered → asset_path, cover_letter_path written to lead record
```

---

## Runtime Boundaries

| Boundary            | Controlled By        | Notes                                              |
|---------------------|----------------------|----------------------------------------------------|
| Auto-apply threshold | User settings        | Score > N → auto-apply in Ghost Mode               |
| Scan interval        | User settings        | Default 6h in Ghost Mode                           |
| LLM provider/model   | Per-step config      | scout, evaluator, ingestor, generator each settable |
| Source adapter list  | User settings (URLs) | Pluggable via source adapter contract              |
| Browser automation   | Opt-in only          | Actuator agent is experimental, off by default    |

---

## IPC Architecture (Tauri ↔ Python)

```
Tauri (Rust)  ◄──► WebSocket (real-time logs + lead updates)
              ◄──► REST (command-and-control: start/stop scan, approve/reject)

Python FastAPI listens on dynamically discovered port.
Tauri discovers port at startup and holds it for the session.
```
