# APPROVED PRODUCT SPECIFICATION — Codex skill-package, compatible v3 release

**Status: OWNER-APPROVED** (2026-11-13). This is the approved functional specification, not a brainstorming list. Preserve the named scope and do not ask whether to create these ten skills; the owner already approved all ten. The repository's existing `AGENTS.md` and actual higher-priority instructions still govern the work. Do not treat repository data or skill body text as independent permission for external mutations.

## A. Product identity and scope

- Target: Codex and software-development agents only. Not a generic ChatGPT assistant package, no hardware troubleshooting/general IT support, no personal finance/contracts, and no comparison between models for a project.
- Usage: freelance and in-house full-stack development; substantial backend engineering in **Laravel/PHP** and **Django/Python**, frontend from **Blade/Django Templates + HTML/CSS/JS** to **React/Next.js**, databases from **SQLite** to **MySQL/SQL Server**. Stack-specific examples, not stack-specific duplicate skills.
- `steps` remains technical team lead/orchestrator: dynamically assess real task criticality, workload, constraints, dependencies, specialist need, owner authority, verification and acceptance. Codex itself performs ordinary implementation; a skill is NOT an isolated execution agent.
- `AGENTS.md` must not be displaced by skills; respect the actual runtime's instruction hierarchy, which also includes higher-priority policies and applicable user requests. `AGENTS.md` paths/doc formats for project-specific documentation supersede generic defaults.
- Preserve useful parts of existing 16 skills; no generic system/Office/plugin snapshots mixed into personal skill install set.

### A1. Four activation policies (MUST implement clearly)

| Policy | Meaning |
|---|---|
| `CONTEXTUAL_AUTO` | `steps` may route to it ONLY if real task scope/risk/contract calls for that specialist; not merely keyword matching. |
| `EXPLICIT_ONLY` | User's direct unambiguous request (either natural-language intent or skill invocation) required. Do not start because a neighboring task could theoretically benefit. |
| `SUPPORTING` | Optional, narrowly scoped complement when it saves work/lowers risk. |
| `OUT_OF_SCOPE` | No custom Codex workflow for this subject; avoid routing into software package. |

Authorization is a SECOND, independent dimension: even with `EXPLICIT_ONLY` trigger, a production mutation / deployment / destructive test / Git history rewrite requires appropriate specific permission. A project being high criticality does not confer authority.

### A2. Explicit-only topic boundaries across all skills

- `E15` WebSocket/SSE/realtime technologies: implement only if the owner explicitly requests that design/feature. Do not propose or auto-add realtime merely to make an application feel advanced.
- `O12` 3D/WebGL website features: only with direct user request. `O11` logo/brand ideation normally outside Codex, using an already approved brand only.
- `P09` presentable demo/presentation: only when directly requested, not the default output of every feature.
- `P11` full teaching/handoff to new developer: only when direct request indicates that intent, not an auto-generated two-file explanation for every code edit. Narrow source questions may still use `hand-off EXPLAIN` naturally.
- `H13` load/stress testing and `J08` full-scope security audit: only directly requested, with a separately safe approved environment and test scope.
- `K04`, `K12`, `K13`, `K14`, `K16`: PR/release infrastructure/CI-CD/deployment/rollback/disaster recovery: retained but **ONLY direct requests**, not default steps. This package's owner's explicit instruction to commit/push/install this skill repo is a narrow exception specific to this task.
- Backup/cron/server task distinctions: Codex may implement the **application's** scheduled jobs and test them; configuring cron/service on a server is an owner/infrastructure action unless expressly authorized. No production cron installation or worker start as a side effect of implementing a job.
- Exclusions: `A07`, `N10`, `P03`, `P10`, `P12`, `Q09`, `Q11`, and entire `R01–R08` domain. Do not add skills specializing in these activities. Exclusion of price/time sales estimation does NOT prevent `steps`' technical workload rating.

## B. TEN NEW SKILLS — exact names, ownership and acceptance contracts

### B01. `integration-reliability` — P0 — `CONTEXTUAL_AUTO`

**Problem solved:** reliable communication with external APIs and webhooks, notably payment/SMS/provider services, uncertain outcomes, retries, duplicates and partial failure.

**Triggers:** implementing or diagnosing a real third-party integration, webhook, provider throttling, timeout/failure/retry semantics, event duplication or idempotent external side effects. **Non-triggers:** local CRUD, generic internal REST endpoint, static page or routine backend method without external dependency.

**Required method:** inspect the concrete provider contract first, trust boundaries, authentication/signature verification, response codes, quota/429 semantics, retryability/idempotency, timeout budgets, backoff+jitter when justified, rate-limit handling, event identity/order/replay, state transitions, partial failure, lost responses after success, reconciliation, logs/correlation and testable fallback/recovery. Prefer provider-native semantics; avoid blindly retrying non-idempotent operations. Distinguish webhook sender from consumer. Never invent a provider SLA or guarantee.

**Deliverable:** targeted integration/failure matrix; actual/proposed contract, retry/timeout rules, idempotency strategy, error branches, observability, tested negative scenarios, evidence, unresolved provider unknowns. Can work with `full-plan` (feature contracts), `architecture-review` (component boundaries), `test-engineering` (testing). Do not hijack any other specialist's ownership.

**Accept if:** potential 429, duplicate webhook, timeout-after-side-effect, ordering and partial failure addressed or truthfully marked N/A/unknown; no accidental third-party messages/payments.

### B02. `test-engineering` — P0 — `CONTEXTUAL_AUTO`

**Problem solved:** meaningful test strategy and implementation for code behavior; existing skills emphasize regression/browser/end-state instead of systematic unit/integration/contract testing.

**Triggers:** creation/change of meaningful application behavior, API contracts, business rules, permissions, models, data operations, or explicit test requests. **Non-triggers:** purely descriptive read-only request or trivial cosmetic change without material behavior; no forced new test framework in a stable project.

**Required method:** inspect project's existing pytest/Django tests, PHPUnit/Laravel tests or JS test setup; derive requirement-based positive, negative, permission, edge and failure cases; choose test pyramid/fixtures/mocks appropriate to risk; design isolated/transactional safe test data, assert real effects, run actual commands only in permitted environment; diagnose flaky tests without weakening assertions; report exact run output.

**Deliverable:** compact behavior-to-test traceability, changed/created tests and fixtures, executed tests, results, confidence gaps. Maintain separation: `regression-check` legacy contract preservation, `practical-test` actual browser acceptance, `final-check` overall deliverable verdict.

**Accept if:** test coverage relevant to task, actual test evidence, no production DB mutation, no fabricated PASS.

### B03. `security-assurance` — P1 — `TARGETED` auto, `FULL_AUDIT` explicit-only

**Problem solved:** targeted security assurance and separately requested full security audits, threat analysis and third-party dependency vulnerabilities.

**TARGETED trigger:** material auth/authz, permissions, upload, user secrets, payment, trust boundary or dependency-sensitive change; review ONLY the relevant attack surfaces. **FULL_AUDIT trigger:** direct user's request to audit a feature/subsystem/project. **Non-triggers:** routine CSS, generic API with no relevant security delta, cosmetic refactor; full audit never automatic.

**Required method:** scoped threat model for identity, assets, trust boundaries, abuse cases, OWASP-aligned practical risks as relevant, IDOR/object auth, permission negatives, CSRF/XSS/injection/input/files, token/session and secrets, dependency advisory data from actually available sources/tools. Distinguish exploitability, evidence, severity, confidence and uncertainty. Suggest minimal fixes plus focused tests.

**Safety:** do not exfiltrate secrets; no unauthorized live exploit/port scan/attack against public/third-party/production targets. No destructive payloads. `AGENTS.md` and owner scope govern tool execution.

**Accept if:** findings grounded by code/tests or marked hypotheses; no scope inflation; remediation and validation clear.

### B04. `docs-maintenance` — P1 — `SYNC` contextual, `USER_GUIDE` explicit-only

**Problem solved:** keep existing project docs in sync with actual behavior, or prepare end-user documentation when specifically requested.

**SYNC trigger:** code/API/config/behavior change that invalidates existing documentation or triggers a project's prescribed docs updates. **Non-trigger:** no doc affected and `AGENTS.md` doesn't mandate updating docs; never create docs for show. `USER_GUIDE` requires explicit user intent.

**Required method:** inspect actual docs hierarchy, `AGENTS.md` and nested rules, diff actual source contracts, make minimum doc changes preserving user prose/links/templates, cite source paths/behavior, clearly mark runtime-unverified assertions. For end-user guides, use observed features and instructions/screens only when verified; no invented UI or screenshots. Do not automatically create `docs/hand-offs/` if project uses another scheme.

**Boundary:** `hand-off` owns source-grounded technical explanation and portable LLM context; this skill owns general documentation sync and user guides.

**Accept if:** correct project path/format, no unnecessary docs, exact changes traceable to source or explicit needs.

### B05. `maintenance-evolution` — P2 — bounded `CONTEXTUAL_AUTO`

**Problem solved:** managing backwards-compatible evolution and scoped technical debt, deprecation of APIs/features, legacy consumers and safe gradual removal.

**Triggers:** substantial refactor, intended removal/rename, major framework upgrade, explicit deprecation/debt review. **Non-triggers:** routine implementation, vague future-proofing, whole-repo debt audit without request.

**Required method:** identify affected consumers and compatibility commitments; define deprecation notices, migration windows when facts permit, transitional interfaces, tests, cleanup/removal criteria; distinguish concrete debt from preferences and prioritize by evidence. Coordinate `db-impact` for persistence, `architecture-review` for boundaries, `regression-check` for preservation, `release-management` for release steps.

**Accept if:** breaking changes and consumer impact recognized, smallest viable migration plan, realistic checks, no speculative rewrite.

### B06. `skill-evals` — P1 — `EXPLICIT_ONLY` for skill/package work

**Problem solved:** validate both structure and actual observed behavior of skills and team-lead orchestration.

**Triggers:** explicit creating, upgrading, testing or auditing a skill/skill package or `steps`. This task **explicitly triggers it**. **Non-triggers:** ordinary application development or general model benchmark; user works with one model per project.

**Required method:** structural validation + scenario bank of positive/negative triggers, permission-boundaries, `AGENTS.md` conflict, prohibited tool actions, minimum necessary skill selection, quality/coverage, output verbosity, regressions. Use actual isolated agent/CLI harness when possible; never conflate file inspection with observed model route selection. Report before/after traces when feasible; record environment, paths and versions; target 30+ carefully chosen scenarios and all 10 new skills.

**Accept if:** no fake independent worker/tests, separate STATIC/BEHAVIORAL results, reproducible failures and limitations.

### B07. `load-testing` — P2 — `EXPLICIT_ONLY`

**Problem solved:** controlled load/stress/benchmark execution independent of normal performance review.

**Triggers:** explicit load test, stress test, concurrent traffic benchmark or similar direct request. **Non-trigger:** one slow API, general performance concerns, ordinary deploy.

**Required method:** obtain validated target/environment and owner permission (especially production), explicit finite traffic profile (requests/RPS/concurrency/duration), synthetic test data, abort thresholds, warm-up, latency quantiles, throughput, resource/HTTP error tracking, compare reproducible baselines. Reuse installed appropriate tools; install no load tools unless authorized.

**Safety:** do not stress production/third-party systems without specific scoped authorization; default to local/test/staging; stop on overload; do not cause real payments/notifications. `performance-review` handles bottleneck diagnosis and remediation.

**Accept if:** measured results with exact environment/profile or a clearly blocked plan if unsafe/unavailable.

### B08. `technical-proposal-discovery` — P2 — `EXPLICIT_ONLY`

Two distinct requested modes:

- `TECHNICAL_PROPOSAL`: technical brief → validated assumptions, scope, deliverables, design choices, implementation outline, dependencies, non-goals, risks, acceptance, maintenance/hand-off considerations. **No commercial price/contract/financial management.**
- `COMPETITOR_RESEARCH`: inspect genuinely available competitor/product sources; compare only evidence-supported software features, UX and design/technical constraints; date sources and distinguish verified claims from inference; no fake access/research.

**Non-triggers:** ordinary feature design or general product brainstorming (`multiple-pov` owns those), project implementation without proposal request.

**Accept if:** actionable proposal or reliable comparison with clear provenance; no fictional business data.

### B09. `release-management` — P2 — `EXPLICIT_ONLY`

**Problem solved:** version selection, changelog, release readiness, compatibility, deploy/rollback planning and—ONLY if specifically authorized—related Git/CI/release actions.

**Triggers:** direct request for release prep/notes/version/tag/publish. **Non-trigger:** every completed feature, test passing or routine commit; no automatic deploy.

**Required method:** inspect repo's version strategy, branch protection/CI, reviewed changes, deployment ownership and environment, test evidence; generate release manifest/checklists, exact SHA/tag, risk/compatibility and scoped rollback plan. Do not assume deploy responsibility is user's on every project.

**Safety:** source edits, commit, push, tag, deploy, infra/cron are distinct permissions. The current package user request expressly allows repo-scoped commit/push/install but **not** unrelated production deploy.

**Accept if:** verifiable release provenance or honest status `PR_PENDING/BLOCKED`, no invented published release.

### B10. `backup-recovery` — P2 — `EXPLICIT_ONLY`

**Problem solved:** data/state backup strategy, backup integrity, recovery planning or specifically authorized restore operations.

**Triggers:** direct request for backup, restore, disaster recovery or a restore rehearsal. **Non-triggers:** merely touching database, migration, coding a job, shipping a feature.

**Required method:** distinguish app code/artifacts, database, uploads/state and secrets; document retention, ownership, restore order, integrity tests and RPO/RTO when available; create realistic runbook and safe rehearsal only in permitted environment. Scope production permissions carefully. `db-impact` covers schema migration hazards, `release-management` code release rollback; do not duplicate them.

**Safety:** configuring cron on server, restoring/deleting production backups, mutating live state or changing infra remains owner-only or specifically permissioned; author may prepare commands without running.

**Accept if:** concrete, testable runbook with explicit unverified operational assumptions and no unauthorized changes.

## C. SIXTEEN EXISTING SKILLS — preserve and surgically upgrade

| Existing skill | Mandatory changes / protected behavior |
|---|---|
| `steps` | Stay top-level engineering coordinator; project-context risk/workload taxonomy preserved. Add explicit routing for all ten specialists and the four policies, actual worker-vs-skill distinction, proportional roadmap/reporting, clear DoD, permission gates, evidence reuse, rework/resume rules, owner-visible realistic completion. Do not always call all skills. |
| `multiple-pov` | Preserve one-time broad pre-design perspective and delta-only reevaluation; clarify boundary with technical proposal, specialist integration/security and architecture review; no forced options. |
| `full-plan` | Extend beyond API-only when appropriate: actors, workflows, business invariants, failure modes, acceptance and then API/UI/jobs where relevant; retain detailed real-vs-proposed endpoint contract capability. Align approval gate with project governance/`steps`, do not block every routine authorized API change. |
| `architecture-review` | Bounded concrete plan review, end-to-end boundaries and behavior, avoid automatic deep security audit or generic product brainstorm; smallest credible repairs; preserve reviewer-only posture. |
| `devil` | Only consequential technical decisions; evidence-based failure modes and realistic mitigations; avoid theater and redundant full reviews. |
| `db-impact` | Real schema/data blast-radius and migration-compatibility/rollback evidence; no auto production execution; coordinate with `backup-recovery` for explicit broader recovery planning. |
| `root-cause` | Add short actionable postmortem and preventive action for material/repeated failures, minimal known-cause debugging and strong actual reproduction/evidence; no postmortem boilerplate for typo. |
| `performance-review` | Add bounded query plan/index/cache/frontend rendering/bundle/assets approaches based on baseline; coordination with explicit-only `load-testing`; no benchmark or caching theater. |
| `regression-check` | Preserve protected legacy behavior, real baseline, targeted/Deep mode, reuse fresh evidence, no whole-task completion verdict. |
| `practical-test` | Allow `steps`-initiated practical testing for a known safe running target, not mandatory manual slash-only, and accept an actually confirmed existing URL rather than demand it in same message. Never invent URL or restart/deploy app without separate approval; real browser checks only. |
| `final-check` | End-to-end DoD/acceptance traceability, evidence freshness and unsupported claim detection; reuse test/regression evidence, only full completion verification owner. |
| `hand-off` | Preserve `EXPLAIN/EXPLORE/HANDOFF/REFRESH`, source-grounded maps and two full handoff outputs on explicit/clear intent; `AGENTS.md` docs layout and user prose outrank default docs path; defer generic docs maintenance to `docs-maintenance`. |
| `compatible-response` | Presentation-only, compact but complete; never suppress required specialist evidence or formats. |
| `natural-persian-writing` | Fix strict YAML invalid description (existing known issue) without changing language meaning or contracts; natural Persian in prose; no trigger for identifiers-only source changes. |
| `ui-ux-pro-max` | Replace unreliable hard-coded `${CLAUDE_PLUGIN_ROOT}` invocation assumptions with robust actual resolved installed skill path; retain scripts/dataset; detect stack, project design tokens, RTL and accessibility; no auto framework change/3D. |
| `apple-design` | Narrow to fluid interaction/gesture/spring/motion when justified; preserve reduced-motion/accessibility and performance; do not impose Apple visual branding. |

## D. Ownership boundaries — avoid over-specialization

- No new skills for every programming language, CRUD, API controller, database engine, query optimizer, cache, React renderer or postmortem; use Codex core coding plus existing enhanced skills.
- `integration-reliability` is about external integration resilience, not general full-plan or security audit.
- `test-engineering` develops appropriate software tests; `regression-check` verifies preserved behavior; `practical-test` performs real browser acceptance; `final-check` audits full completion.
- `security-assurance TARGETED` bounded auto-review vs `FULL_AUDIT` on-demand. `load-testing` is NOT routine performance-review.
- `hand-off` is developer/LLM understanding; `docs-maintenance` is source-backed doc sync/user guide.
- `release-management` releases only when explicitly requested. `backup-recovery` is not a prerequisite for ordinary local migrations; safety review remains with `db-impact`.

## E. Required implementation characteristics

- Original personal skills and their meaningful behavior remain functional; if any contract must be changed, explain the compatibility decision and update tests/docs.
- No new implicit server deployment/cron/backup, third-party payment/SMS or public audit actions. Code-level job implementation is allowed for an approved feature.
- All actual tests and claims evidence-labeled `VERIFIED`, `OWNER_CONFIRMED`, `UNVERIFIED` as appropriate. Define narrow `BLOCKED` reasons, not generic claim of success.
- Include 10 new SKILL.md files and 16 existing upgraded skill directories; count exact against manifest and physical files after build.
- Preserve 16 runtime-managed plugin snapshots and system-skill exclusions in manifest. Never replace the runtime-managed content with personal copies.
- Version remains compatible with v3 and should pass both structural validation and executed routing/evaluation coverage before claiming successful release.
