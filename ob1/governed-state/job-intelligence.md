# Governed State: Job Intelligence Domain

**Domain:** job-intelligence
**Source:** JustHireMe v0.1-alpha
**Approved by owner:** 2026-05-07
**Status:** ACTIVE

---

## Governed Truths

| ID    | Statement                                                                                     |
|-------|-----------------------------------------------------------------------------------------------|
| GT-01 | The canonical Lead schema is the JustHireMe Lead object (`schemas/lead.json`). Any job lead captured in OB1 conforms to this schema. |
| GT-02 | A lead requires a Quality Gate pass before entering ranking. Gate decisions are immutable evidence and must store a `reason` string. |
| GT-03 | Fit scores below 70 are surfaced for review only, not acted upon autonomously. Score threshold: **70**. |
| GT-04 | The only irreversible action in the job intelligence pipeline is sending an application externally. All other CRM mutations are soft and reversible. |
| GT-05 | Profile graph (Kuzu) is the source of truth for candidate skills and project evidence. Free-form resume text is secondary. |
| GT-06 | Every autonomous agent action that writes to the CRM emits an event to the audit trail with a reason string. No silent mutations. |

---

## Authority Rules

| Rule  | Rule Statement                                                                    | Scope              |
|-------|-----------------------------------------------------------------------------------|--------------------|
| AR-01 | Agents may save, score, and gate leads without human approval.                    | Fully autonomous   |
| AR-02 | Agents may generate application PDFs only after a lead is in `approved` status.   | Post-approval      |
| AR-03 | Agents may NOT send applications externally without explicit human instruction.   | Hard boundary      |
| AR-04 | Profile graph mutations require either human upload or explicit agent instruction with source provenance. | Instructed only |
| AR-05 | Score threshold changes require owner approval and are written to governed-state.  | Owner only         |
| AR-06 | Ghost Mode (auto-apply above threshold) is OFF by default. Must be explicitly enabled by owner. | Opt-in |

---

## Registered Skill Cards

| Skill Card                   | Authority          | Reversible |
|------------------------------|--------------------|------------|
| `RankJobLead`                | Agent-autonomous   | Yes        |
| `RunQualityGate`             | Agent-autonomous   | Yes        |
| `GenerateApplicationPackage` | Post-approval only | Yes        |
| `MaintainProfileGraph`       | Instructed only    | Soft       |
| `ScanJobSources`             | Agent-autonomous   | Yes        |
| `SuggestUpskilling`          | Agent-autonomous   | Yes        |

---

## Governed Settings

| Setting            | Value     | Notes                                      |
|--------------------|-----------|--------------------------------------------|
| `score_threshold`  | 70        | Leads below this require human review      |
| `ghost_mode`       | false     | Off by default; owner must explicitly enable |
| `mcp_tool_prefix`  | `job.`    | All JustHireMe MCP tools namespaced `job.` |
| `output_surface`   | `output/job-intelligence/` | Generated PDFs go here, not `evidence/` |

---

## Conflict Resolutions (Adopted)

| Conflict                  | Resolution                                                                          |
|---------------------------|-------------------------------------------------------------------------------------|
| Skills surface duplication | JustHireMe skill nodes are a job-intelligence view only; not merged with ob1 canonical identity. Follow-up: create `skill-mapping.md`. |
| Identity vs profile graph  | Profile graph is scoped to job-intelligence domain. Not a general identity record.  |
| LLM provider config        | Align JustHireMe per-step model config with ob1 preferred provider at integration time. |
| Evidence vs output files   | Generated PDFs → `output/job-intelligence/`, not `evidence/`.                      |
| MCP tool naming            | All JustHireMe MCP tools prefixed `job.` to avoid collisions.                      |

---

## Open Follow-ups

- [x] ~~Create `prepared-context/job-intelligence/skill-mapping.md`~~ — **Done.** 90-skill mapping table covering `TECH_CATEGORY`, ingestor fallbacks, and generator display groupings. Adjacency blocklist documented.
