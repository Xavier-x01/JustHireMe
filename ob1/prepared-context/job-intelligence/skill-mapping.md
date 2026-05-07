# Skill Taxonomy Mapping: JustHireMe → OB1 Canonical

**Domain:** job-intelligence
**Source:** JustHireMe v0.1-alpha (`backend/agents/scoring_engine.py::TECH_CATEGORY`, `backend/agents/generator.py`)
**Type:** prepared-context / skill-mapping
**Resolves:** Open follow-up in `governed-state/job-intelligence.md`

---

## Overview

JustHireMe uses two parallel skill category systems that must be unified for OB1:

| System | Location | Usage |
|--------|----------|-------|
| **Internal `cat` tags** | `TECH_CATEGORY` dict in `scoring_engine.py` | Semantic scoring, role matching, adjacency logic |
| **Resume display groupings** | `generator.py` category map | PDF section headers for human readers |
| **Ingestor fallbacks** | `ingestor.py`, `github_ingestor.py`, `linkedin_parser.py` | Default tags for unclassified skills |

This file defines the **OB1 canonical skill ontology** and maps every known JustHireMe category token to it.

---

## OB1 Canonical Skill Categories

| OB1 Canonical ID | Display Name              | Description                                                    |
|------------------|---------------------------|----------------------------------------------------------------|
| `language`       | Languages                 | Programming languages (Python, TypeScript, Go, Rust…)          |
| `frontend`       | Frontend & UI             | Browser-side frameworks, CSS tooling, HTML (React, Vue, Svelte…) |
| `backend`        | Backend & APIs            | Server frameworks, API patterns (FastAPI, Node.js, GraphQL…)   |
| `mobile`         | Mobile                    | Native and cross-platform mobile (Flutter, Swift, Kotlin…)     |
| `desktop`        | Desktop                   | Desktop app runtimes (Tauri, Electron)                         |
| `data`           | Data & Databases          | SQL/NoSQL databases, ORMs, data pipelines (PostgreSQL, Redis…) |
| `ai`             | AI & ML                   | LLMs, vector stores, ML frameworks, agentic libraries          |
| `infra`          | Infrastructure & DevOps   | Cloud, containers, IaC, CI/CD, Linux (AWS, Docker, Terraform…) |
| `realtime`       | Realtime & Media          | WebRTC, audio/video pipelines (LiveKit, Deepgram)              |
| `testing`        | Testing & QA              | Test automation, browser automation (Playwright)               |
| `automation`     | Automation                | General-purpose scripting, workflow automation                 |
| `product`        | Product & Payments        | Billing, payments, SaaS primitives (Stripe)                    |
| `enterprise`     | Enterprise Systems        | ERP, CRM, enterprise platforms (SAP, Salesforce, ServiceNow)   |
| `cms`            | CMS & Web Platforms       | Content management systems (WordPress)                         |
| `general`        | General / Unclassified    | Fallback for skills not yet mapped to a canonical category     |
| `portfolio`      | Portfolio (ingest source) | Skills extracted from portfolio sites; reclassify on review    |
| `github`         | GitHub (ingest source)    | Skills extracted from GitHub repos; reclassify on review       |

---

## JustHireMe → OB1 Category Token Mapping

### Scoring Engine `TECH_CATEGORY` (authoritative)

| JustHireMe Skill         | JustHireMe `cat` | OB1 Canonical    |
|--------------------------|------------------|------------------|
| Python                   | language         | `language`       |
| TypeScript               | language         | `language`       |
| JavaScript               | language         | `language`       |
| C++                      | language         | `language`       |
| C#                       | language         | `language`       |
| Java                     | language         | `language`       |
| PHP                      | language         | `language`       |
| Ruby                     | language         | `language`       |
| Go                       | language         | `language`       |
| Rust                     | language         | `language`       |
| SQL                      | data             | `data`           |
| React                    | frontend         | `frontend`       |
| Next.js                  | frontend         | `frontend`       |
| Vite                     | frontend         | `frontend`       |
| Tailwind                 | frontend         | `frontend`       |
| HTML                     | frontend         | `frontend`       |
| CSS                      | frontend         | `frontend`       |
| Vue                      | frontend         | `frontend`       |
| Angular                  | frontend         | `frontend`       |
| Svelte                   | frontend         | `frontend`       |
| Flutter                  | mobile           | `mobile`         |
| Swift                    | mobile           | `mobile`         |
| Kotlin                   | mobile           | `mobile`         |
| Android                  | mobile           | `mobile`         |
| iOS                      | mobile           | `mobile`         |
| Node.js                  | backend          | `backend`        |
| Express                  | backend          | `backend`        |
| NestJS                   | backend          | `backend`        |
| FastAPI                  | backend          | `backend`        |
| Django                   | backend          | `backend`        |
| Flask                    | backend          | `backend`        |
| Laravel                  | backend          | `backend`        |
| Ruby on Rails            | backend          | `backend`        |
| REST API                 | backend          | `backend`        |
| GraphQL                  | backend          | `backend`        |
| WebSockets               | backend          | `backend`        |
| Firebase                 | backend          | `backend`        |
| WordPress                | cms              | `cms`            |
| PostgreSQL               | data             | `data`           |
| MySQL                    | data             | `data`           |
| MongoDB                  | data             | `data`           |
| Redis                    | data             | `data`           |
| Prisma                   | data             | `data`           |
| Drizzle                  | data             | `data`           |
| Supabase                 | data             | `data`           |
| Data Pipeline            | data             | `data`           |
| Qdrant                   | ai               | `ai`             |
| Pinecone                 | ai               | `ai`             |
| ChromaDB                 | ai               | `ai`             |
| LanceDB                  | ai               | `ai`             |
| Vector DB                | ai               | `ai`             |
| RAG                      | ai               | `ai`             |
| LLM                      | ai               | `ai`             |
| AI Agents                | ai               | `ai`             |
| OpenAI                   | ai               | `ai`             |
| Anthropic                | ai               | `ai`             |
| LangChain                | ai               | `ai`             |
| LangGraph                | ai               | `ai`             |
| Machine Learning         | ai               | `ai`             |
| NLP                      | ai               | `ai`             |
| Computer Vision          | ai               | `ai`             |
| PyTorch                  | ai               | `ai`             |
| TensorFlow               | ai               | `ai`             |
| Groq                     | ai               | `ai`             |
| Automation               | automation       | `automation`     |
| Docker                   | infra            | `infra`          |
| Kubernetes               | infra            | `infra`          |
| Terraform                | infra            | `infra`          |
| AWS                      | infra            | `infra`          |
| GCP                      | infra            | `infra`          |
| Azure                    | infra            | `infra`          |
| Vercel                   | infra            | `infra`          |
| CI/CD                    | infra            | `infra`          |
| Linux                    | infra            | `infra`          |
| LiveKit                  | realtime         | `realtime`       |
| Deepgram                 | realtime         | `realtime`       |
| Playwright               | testing          | `testing`        |
| Stripe                   | product          | `product`        |
| Tauri                    | desktop          | `desktop`        |
| Electron                 | desktop          | `desktop`        |
| SAP                      | enterprise       | `enterprise`     |
| ABAP                     | enterprise       | `enterprise`     |
| Salesforce               | enterprise       | `enterprise`     |
| ServiceNow               | enterprise       | `enterprise`     |

---

### Ingestor Fallback Tokens → OB1 Canonical

| JustHireMe `cat` token | Source                        | OB1 Canonical | Action Required              |
|------------------------|-------------------------------|---------------|------------------------------|
| `general`              | linkedin_parser, ingestor     | `general`     | Reclassify on profile review |
| `portfolio`            | portfolio_ingestor            | `portfolio`   | Reclassify on profile review |
| `github`               | github_ingestor               | `github`      | Reclassify on profile review |

Skills tagged `general`, `portfolio`, or `github` are ingest-time fallbacks. They should be reclassified to a canonical OB1 category during profile review or via the `MaintainProfileGraph` skill card.

---

### Generator Display Groupings → OB1 Canonical

The generator uses a separate display-layer map for PDF section headers. This mapping is for resume rendering only and does not override the OB1 canonical taxonomy.

| Generator Display Header    | Maps from `cat` tokens                                    | OB1 Canonical categories included              |
|-----------------------------|-----------------------------------------------------------|------------------------------------------------|
| Languages                   | `language`, `languages`, `lang`                           | `language`                                     |
| Frameworks & Libraries      | `framework`, `frontend`, `backend`, `library`             | `frontend`, `backend`, `mobile`, `desktop`     |
| Databases & Data Tools      | `database`, `data`, `db`                                  | `data`, `ai` (vector stores)                   |
| Tools & Platforms (default) | anything not matched above                                | `infra`, `testing`, `automation`, `product`, `enterprise`, `realtime`, `cms` |
| Cloud & DevOps (optional)   | Added by LLM if JD demands it                             | `infra`                                        |

---

## Adjacency Blocklist (Scoring)

The scoring engine prevents false-positive skill adjacency matches for these OB1 categories:

```
language, frontend, mobile, desktop, cms, enterprise
```

Rationale: knowing Python does not imply knowing JavaScript even though both are `language`; knowing React does not imply knowing Vue even though both are `frontend`. The blocklist prevents the evaluator from giving adjacency credit across these groups.

---

## Governance Notes

- **Source of truth for scoring:** `TECH_CATEGORY` in `scoring_engine.py`. Any new skill added to JustHireMe should be added here first, then reflected in this mapping.
- **New skills procedure:** Add to `TECH_CATEGORY` → choose the closest OB1 canonical category → add a row to the table above → re-run scoring engine tests.
- **Ingest fallbacks (`general`, `portfolio`, `github`):** Are accepted as valid stored values but should not be used as scoring inputs without reclassification.
- **Display groupings** in `generator.py` are presentation-layer only and do not need to match OB1 canonical IDs exactly.
