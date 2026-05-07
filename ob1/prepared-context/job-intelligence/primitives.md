# Job Intelligence — Semantic Work Primitives

**Domain:** job-intelligence
**Source:** JustHireMe v0.1-alpha
**Type:** prepared-context / primitives
**Importance:** high
**Tags:** semantic-primitive, quality-gate, ranking, lead-normalization, profile-matching

---

## Primitive 1: Normalized Lead

| Field        | Value                                                                 |
|--------------|-----------------------------------------------------------------------|
| **Name**     | Normalized Lead                                                       |
| **Description** | A job or gig posting stripped to canonical form with dedup key, source metadata, and audit trail |
| **Inputs**   | Raw HTML/RSS/API response from any job source                        |
| **Outputs**  | Typed Lead object (see schema) committed to SQLite CRM                |
| **Quality Gates** | URL exists, posting has depth, freshness >0 days, no red flags  |
| **Risk**     | Low — read-only capture; reversible via `delete_lead(job_id)`         |
| **Reversibility** | Fully reversible (soft-delete in CRM)                          |
| **Agent Value** | Gives agents a stable, typed unit they can reason about and act on without re-scraping |

---

## Primitive 2: Quality Gate Decision

| Field        | Value                                                                 |
|--------------|-----------------------------------------------------------------------|
| **Name**     | Quality Gate Decision                                                 |
| **Description** | Deterministic pass/fail verdict on a raw lead with an explicit reason and penalty score |
| **Inputs**   | Raw lead dict `{url, title, company, description, posted_date}`       |
| **Outputs**  | `{pass: bool, reason: str, penalty_score: int}`                       |
| **Quality Gates** | All six criteria checked; any hard fail → immediate reject      |
| **Risk**     | Low — no state mutation on reject; approved leads write CRM status    |
| **Reversibility** | Decisions are logged; operator can override status manually     |
| **Agent Value** | Removes agent hallucination risk on lead quality; provides symbolic reason string the agent can relay to user |

**Six Criteria:**

| Check              | Type          | Failure Effect        |
|--------------------|---------------|-----------------------|
| `url_exists()`     | Hard reject   | Lead discarded        |
| `posting_depth()`  | Penalty       | Score reduced         |
| `freshness()`      | Penalty       | Score reduced         |
| `seniority_check()`| Hard reject   | Lead discarded        |
| `red_flags()`      | Penalty/Hard  | Reduced or discarded  |
| `context()`        | Penalty       | Score reduced         |

---

## Primitive 3: Fit Score

| Field        | Value                                                                 |
|--------------|-----------------------------------------------------------------------|
| **Name**     | Fit Score                                                             |
| **Description** | Composite 0–100 score expressing how well the candidate profile matches a job lead |
| **Inputs**   | Lead object + Kuzu candidate graph + LanceDB vector index             |
| **Outputs**  | `{score: int, reason: str, match_points: list[str], gaps: list[str]}` |
| **Components** | Deterministic rubric (source signal, quality, seniority) + optional LLM reasoning + semantic vector similarity + feedback learning |
| **Risk**     | Medium — score gates downstream actions (tailoring, auto-apply)       |
| **Reversibility** | Score can be recalculated; user can override via manual approve  |
| **Agent Value** | Gives agents an explainable, auditable number with evidence strings; not a black-box embedding |

**Score Assembly:**

```
Final Score = 
  source_signal_weight     (platform reputation)
+ quality_gate_penalty     (from gate decision)
+ seniority_alignment      (cap if over/under)
+ semantic_similarity      (LanceDB cosine)
+ llm_reasoning_bonus      (optional, step="evaluator")
+ feedback_adjustment      (learn from approve/reject history)
```

---

## Primitive 4: Profile Graph

| Field        | Value                                                                 |
|--------------|-----------------------------------------------------------------------|
| **Name**     | Profile Graph                                                         |
| **Description** | Kuzu graph encoding candidate's full work history as typed nodes and edges |
| **Inputs**   | Resume PDF, LinkedIn export ZIP, GitHub handle, portfolio URL         |
| **Outputs**  | Kuzu graph: Candidate → Experience, Project, Skill nodes              |
| **Quality Gates** | Dedup by title+company; skills normalized to canonical names     |
| **Risk**     | Medium — source of truth for scoring; bad ingestion → wrong scores   |
| **Reversibility** | Nodes can be deleted/edited via profile management UI           |
| **Agent Value** | GraphRAG proof-of-work — agents query Cypher to find concrete evidence ("Has candidate built something with FastAPI?") instead of relying on freeform resume text |

---

## Primitive 5: Skill / Project Vector

| Field        | Value                                                                 |
|--------------|-----------------------------------------------------------------------|
| **Name**     | Skill / Project Vector                                                |
| **Description** | Embedding of a candidate's skills and projects stored in LanceDB for semantic search |
| **Inputs**   | Profile graph nodes (skills text, project descriptions, experience summaries) |
| **Outputs**  | Float vector per entity in LanceDB table                              |
| **Quality Gates** | Embedding generated only after profile graph is committed        |
| **Risk**     | Low — read-only at query time; rebuilt on profile update              |
| **Reversibility** | Fully regenerable from graph                                    |
| **Agent Value** | Enables fuzzy matching ("knows Rust" ≈ "Cargo, tokio, actix-web") without exact keyword matching |

---

## Primitive 6: Tailored Application Package

| Field        | Value                                                                 |
|--------------|-----------------------------------------------------------------------|
| **Name**     | Tailored Application Package                                          |
| **Description** | Collection of generated artifacts for a specific job application  |
| **Inputs**   | Approved lead + profile graph + selected projects + job description   |
| **Outputs**  | Tailored resume PDF, cover letter PDF, cold email draft, LinkedIn note |
| **Quality Gates** | Lead must be in `approved` status; selected_projects must be set |
| **Risk**     | High — output is sent to external parties; errors (wrong name, wrong company) cause real embarrassment |
| **Reversibility** | Files can be regenerated; once sent externally, not reversible   |
| **Agent Value** | Fully structured output — agent doesn't guess format, it calls `generator.py` with typed inputs |

---

## Cross-Primitive Relationships

```
Profile Graph ──────────────────────────────────┐
    │ (Cypher proof-of-work queries)             │
    ▼                                            │
Fit Score ◄── Skill/Project Vectors (semantic)  │
    │                                            │
    ├── passes threshold ──► Tailored Package ◄──┘
    │
    └── fails threshold ──► Quality Gate Decision (logged)
                             │
                             ▼
                         Normalized Lead (status=discarded)
```

---

## Governance Notes

- **Authority boundary:** Score threshold for auto-apply is a user-configured setting. Agents below threshold must pause and surface to human.
- **Audit trail:** Every gate decision, score, and status change is written to SQLite `events` table.
- **Explainability invariant:** Every primitive exposes a human-readable `reason` string. No silent actions.
- **Freelance variant:** Same primitive set applies; key differences are no seniority rules, projects weighted 3x, and budget reality check added to Fit Score.
