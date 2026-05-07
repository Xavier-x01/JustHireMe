# Proposal: Job Intelligence Domain Module Integration

**Domain:** job-intelligence
**Source:** JustHireMe v0.1-alpha
**Type:** proposal (awaiting owner review)
**Status:** DRAFT — not yet governed-state
**Prepared:** 2026-05-07

---

## Summary

This proposal recommends absorbing JustHireMe as a **Job Intelligence domain module** inside any OB1 instance. It defines the governed truths to adopt, authority rules to establish, skill cards to register, and conflicts to resolve.

---

## 1. Recommended Governed Truths

The following statements are proposed for promotion to `governed-state/` after owner review:

| ID  | Statement                                                                           |
|-----|-------------------------------------------------------------------------------------|
| GT-01 | The canonical Lead schema is the JustHireMe Lead object (see `schemas/lead.json`). Any job lead captured in OB1 conforms to this schema. |
| GT-02 | A lead requires a Quality Gate pass before entering ranking. Gate decisions are immutable evidence and must store a `reason` string. |
| GT-03 | Fit scores below the owner-configured threshold (default: 70) are surfaced for review only, not acted upon autonomously. |
| GT-04 | The only irreversible action in the job intelligence pipeline is sending an application externally. All other CRM mutations are soft and reversible. |
| GT-05 | Profile graph (Kuzu) is the source of truth for candidate skills and project evidence. Free-form resume text is secondary. |
| GT-06 | Every autonomous agent action that writes to the CRM emits an event to the audit trail with a reason string. No silent mutations. |

---

## 2. Authority Rules

| Rule ID | Rule                                                                           | Scope              |
|---------|--------------------------------------------------------------------------------|--------------------|
| AR-01   | Agents may save, score, and gate leads without human approval.                 | Fully autonomous   |
| AR-02   | Agents may generate application PDFs only after a lead is in `approved` status. | Post-approval      |
| AR-03   | Agents may NOT send applications externally without explicit human instruction. | Hard boundary      |
| AR-04   | Profile graph mutations require either human upload or explicit agent instruction with source provenance. | Instructed only |
| AR-05   | Score threshold changes require owner approval and are written to governed-state. | Owner only        |
| AR-06   | Ghost Mode (auto-apply above threshold) must be explicitly enabled by the owner; it is off by default. | Opt-in           |

---

## 3. Skill Cards to Register

```yaml
# RankJobLead
name: RankJobLead
version: 1.0.0
trigger: "rank this job / score this lead / how well do I match [URL or title]"
inputs:
  - lead_url: string (or lead object)
  - candidate_profile: Profile (from governed-state)
outputs:
  - fit_score: FitScore
  - narrative: string
authority: agent-autonomous
reversible: true

# RunQualityGate
name: RunQualityGate
version: 1.0.0
trigger: "check this posting / gate this lead / is this job legit"
inputs:
  - raw_lead: dict {url, title, company, description, posted_date}
outputs:
  - decision: QualityGateDecision
authority: agent-autonomous
reversible: true

# GenerateApplicationPackage
name: GenerateApplicationPackage
version: 1.0.0
trigger: "generate my application / write my cover letter for [title at company]"
inputs:
  - lead: Lead (status must be 'approved')
  - selected_projects: list[string]
outputs:
  - resume_pdf_path: string
  - cover_letter_pdf_path: string
  - cold_email_draft: string
  - linkedin_note: string
authority: post-approval (human must have approved lead first)
reversible: true (files can be regenerated)

# MaintainProfileGraph
name: MaintainProfileGraph
version: 1.0.0
trigger: "update my profile / ingest my resume / add my GitHub"
inputs:
  - source: {type: 'pdf'|'linkedin_zip'|'github', data: bytes|string}
outputs:
  - graph_delta: {added_nodes: int, updated_nodes: int}
authority: instructed (requires explicit invocation)
reversible: soft (nodes editable post-ingest)

# ScanJobSources
name: ScanJobSources
version: 1.0.0
trigger: "scan for jobs / find new leads / run job search"
inputs:
  - source_urls: list[string]
  - kind: 'job'|'freelance'
outputs:
  - new_leads: list[Lead]
  - summary: string
authority: agent-autonomous (Sniper mode) or owner-scheduled (Ghost mode)
reversible: true (leads can be deleted)

# SuggestUpskilling
name: SuggestUpskilling
version: 1.0.0
trigger: "what should I learn / what skills am I missing"
inputs:
  - recent_fit_scores: list[FitScore]
outputs:
  - ranked_gaps: list[{skill: string, frequency: int, avg_penalty: float}]
authority: agent-autonomous (read-only analysis)
reversible: true
```

---

## 4. Potential Conflicts / Duplications

| Conflict                     | Risk   | Proposed Resolution                                               |
|------------------------------|--------|-------------------------------------------------------------------|
| Skills surface duplication   | Medium | Treat JustHireMe skill nodes as job-intelligence view; map to canonical ob1 skills via `prepared-context/job-intelligence/skill-mapping.md` (not yet created — recommend as follow-up) |
| Identity vs profile graph    | Medium | Profile graph is a job-seeking lens, not a general identity record. Keep scoped to job-intelligence domain; do not merge with ob1 identity |
| LLM provider config          | Low    | Align JustHireMe per-step model config with ob1 preferred provider settings during integration |
| Evidence vs output files     | Low    | Generated PDFs go to `output/job-intelligence/`, not `evidence/`  |
| MCP tool naming collisions   | Low    | Prefix all JustHireMe MCP tools with `job.` to namespace them     |

---

## 5. Governed State Recommendation

**Owner action required — approve, modify, or reject each item:**

- [ ] **Adopt GT-01 through GT-06** as governed truths for job-intelligence domain
- [ ] **Adopt AR-01 through AR-06** as authority rules
- [ ] **Register skill cards** RankJobLead, RunQualityGate, GenerateApplicationPackage, MaintainProfileGraph, ScanJobSources, SuggestUpskilling
- [ ] **Set score threshold** (default: 70) as a governed setting
- [ ] **Confirm Ghost Mode is off** by default in this ob1 instance
- [ ] **Resolve skill taxonomy conflict** — create `skill-mapping.md` to align JustHireMe free-form skills with ob1 canonical skill ontology
- [ ] **Decide scope** of profile graph relative to existing identity surfaces in this ob1 instance

---

## Appendix: File Inventory

```
ob1/
├── evidence/
│   └── justhireme/
│       └── raw/
│           └── repo-overview.md        ← high-fidelity repo summary
├── prepared-context/
│   └── job-intelligence/
│       ├── primitives.md               ← 6 semantic work primitives
│       ├── workflows.md                ← 5 pipeline workflows
│       ├── mapping-to-ob1.md           ← surface + authority mapping
│       └── schemas/
│           ├── lead.json               ← Lead JSON Schema
│           ├── fit-score.json          ← FitScore JSON Schema
│           └── quality-gate-decision.json ← QualityGateDecision JSON Schema
└── proposals/
    └── job-intelligence-integration.md ← this file
```
