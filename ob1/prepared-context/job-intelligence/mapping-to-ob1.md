# Mapping: JustHireMe Primitives → Open Brain (OB1) Surfaces

**Domain:** job-intelligence
**Type:** prepared-context / mapping

---

## Primitive-to-Surface Mapping

| JustHireMe Primitive      | OB1 Surface              | Integration Pattern                                      |
|---------------------------|--------------------------|----------------------------------------------------------|
| Normalized Lead           | evidence/               | Lead objects as typed evidence atoms                     |
| Quality Gate Decision     | evidence/ + events log   | Decisions as reviewable evidence with reason strings     |
| Fit Score                 | prepared-context/        | Scores + match_points compressed into skill cards        |
| Profile Graph             | governed-state/          | Candidate profile as owner-approved durable truth        |
| Skill / Project Vector    | prepared-context/        | Embeddings support semantic search across ob1 corpus     |
| Tailored Application Pkg  | evidence/ (output)       | Generated artifacts linked to their source lead          |
| Feedback Events           | governed-state/          | User approve/reject signals as authority assertions      |
| Source Adapter Contract   | skills/ (operators)      | Each adapter = one callable operator skill card          |
| MCP Server                | mcp/ (tools layer)       | Already MCP-native — connect directly to ob1 agent       |
| WebSocket Events          | runtime/ (observation)   | Real-time pipeline state visible to ob1 runtime          |

---

## Suggested New Operators / Skill Cards

| Skill Card Name              | Trigger                                  | Output                                               |
|------------------------------|------------------------------------------|------------------------------------------------------|
| `RankJobLead`                | Given a lead URL or raw posting          | FitScore object with match_points and gaps           |
| `GenerateApplicationPackage` | Given an approved lead + profile         | Resume PDF + cover letter PDF + outreach drafts      |
| `MaintainProfileGraph`       | Given resume / LinkedIn / GitHub input   | Updated Kuzu graph + refreshed LanceDB vectors       |
| `RunQualityGate`             | Given a raw lead dict                    | QualityGateDecision with pass/fail + reason          |
| `ScanJobSources`             | Given source URLs + skill profile        | List of new discovered leads (Normalized Lead[])     |
| `ExplainFitScore`            | Given a job_id                           | Narrative summary of score components for the user   |
| `SuggestUpskilling`          | Given gaps from FitScore[]               | Ranked list of skills to close most gaps fastest     |

---

## Authority Mapping

| Action                        | Who Can Authorize         | Reversibility | Notes                                  |
|-------------------------------|---------------------------|---------------|----------------------------------------|
| Save new lead to CRM          | Agent (auto)              | Full          | Delete via `delete_lead(job_id)`       |
| Run quality gate              | Agent (auto)              | Full          | Re-run anytime                         |
| Score a lead                  | Agent (auto)              | Full          | Re-score anytime                       |
| Generate PDF artifacts        | Agent (after approval)    | Full locally  | Re-generate anytime                    |
| Approve a lead (status change)| Human (Sniper) or Agent (Ghost above threshold) | Soft | Status can be changed back |
| Send application externally   | Human only (default)      | None          | Actuator opt-in; irreversible          |
| Modify profile graph          | Human or Agent via ingest | Soft          | Nodes editable in profile UI           |
| Change score threshold        | Owner only                | Immediate     | Settings mutation                      |

---

## Alignment with Semantic Work Primitive Philosophy

*(Referencing Nate B Jones — "Your AI Fails At Real Work")*

| Concept                    | JustHireMe Implementation                                      |
|----------------------------|----------------------------------------------------------------|
| Access layer               | Scout agent + Playwright (browser), RSS, ATS APIs              |
| Meaning layer              | Quality gate decisions, fit scores, match_points/gaps strings  |
| Authority layer            | Status enum, threshold settings, Ghost vs Sniper modes         |
| Reversibility              | All CRM mutations are soft; application send is the only hard action |
| Reviewability              | Every score has reason string; events table is full audit trail |
| Composability              | Source adapter contract; skill cards chain via operator pattern |
| Explainability invariant   | No silent actions; every gate/score surfaces a reason string   |

The key gap (acknowledged): the `reason` string is LLM-generated prose, not a structured semantic object. Structured reasons (typed gap objects, authority tags on match_points) would make the meaning layer richer and more agent-navigable.

---

## Potential Conflicts with Existing OB1 Patterns

| Conflict Area           | Risk Level | Resolution                                                   |
|-------------------------|------------|--------------------------------------------------------------|
| Profile as governed-state | Medium   | Profile graph may conflict with existing identity/skills surfaces — treat JustHireMe profile as a job-intelligence view, not a canonical identity |
| Skill taxonomy          | Low–Medium | JustHireMe skills are free-form strings; map to ob1 canonical skill ontology in prepared-context layer |
| Evidence vs Output      | Low        | Generated PDFs are outputs, not evidence — keep in separate output/ surface |
| LLM step config         | Low        | JustHireMe per-step model config may need to align with ob1 preferred provider settings |
