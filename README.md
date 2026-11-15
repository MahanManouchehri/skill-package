# skill-package v3.1.1

A verifiable collection of **26 personal Codex skills** for freelance and in-house software development: Laravel/PHP, Django/Python, server templates, React/Next.js and SQLite/MySQL/SQL Server are examples, not mandated frameworks. Skills supply instructions; Codex performs coding and real tools supply capabilities.

## Patch scope

Version 3.1.1 preserves every installable skill byte and the 26/16/5 inventory. It restores licensed UI authoring tools outside the runtime payload, strengthens native evaluation isolation/preflight, and fixes Windows liveness/path safety. Full UI discovery now executes 153 tests, including the previously unimportable modules; the default frozen relevance gate runs all 90 cases offline. See [UI provenance](UI_AUTHORING_PROVENANCE.md), [Windows evidence and safe commands](WINDOWS_COMPATIBILITY.md), and [current validation](VALIDATION.md). Historical evidence remains unchanged under `evals/evidence/`; new results live under `evals/evidence/v3.1.1/`.

## Distribution

- `skills/`: **16 retained/upgraded + 10 new** installable personal skills.
- `managed/plugin-skills/`: **16 original audit-only entries** and full plugin-relative supporting resources. Never install these into personal roots or plugin caches.
- `skills-manifest.json`: compatible schema version 1; metadata, exact files and deterministic SHA-256 tree hashes. Historical source paths/hashes are provenance, not destinations or claims of equality after this upgrade.
- `package-integrity.json`: hashes every distribution file except itself and `.git/`. These are change detectors, not signatures or independent authentication.
- Five historical system-skill exclusions remain recorded. The destination runtime supplies system skills; this installer never modifies system or plugin content.

## Skills

| Skill | Purpose and activation boundary |
|---|---|
| `apple-design` | Design or review fluid gestures, interruptible spring motion, drag/swipe/sheet behavior, velocity handoff and reduced-motion alternatives. Use for concrete interaction and motion work; skip routine page styling, bundle optimization or imposing an Apple visual identity. |
| `architecture-review` | Independently review a concrete implementation plan, system design, or defined technical approach before implementation. Use for requested reviews or consequential structural decisions routed by steps; skip early ideation, routine edits, generic code review and implementation. |
| `backup-recovery` **new** | Design backup and recovery runbooks, verify backup integrity or rehearse/execute a restore only on direct request with appropriate scope. Ordinary database changes, migrations, application jobs and feature delivery do not trigger a backup service or production restore. |
| `compatible-response` | Apply to every Codex user-facing response and output from any skill, across all projects. Adapt presentation to the content and maximize information density without losing essential details. |
| `db-impact` | Analyze the complete blast radius of a proposed database change before it is executed. Use for migrations, schema/data changes, and production-impact reviews; do not use for ordinary read-only data queries. |
| `devil` | Independently stress-test consequential technical decisions, concrete plans, architectures, migrations, refactors, and implementation strategies. Use when adversarial review would materially improve a decision by challenging assumptions, evidence, failure modes, reversibility, blast radius, or alternatives; do not use for routine coding, factual questions, trivial edits, or ordinary low-risk implementation. |
| `docs-maintenance` **new** | Synchronize existing project documentation with real code, API or configuration changes, and write end-user guides when directly requested. Follow project documentation paths; skip unaffected docs and delegate source-code explanation or developer handoff to hand-off. |
| `final-check` | Audit an apparently completed implementation against the user's original request before declaring it finished. Use for explicit final verification and substantial implementation tasks; do not use as a generic code review or repeatedly during development. |
| `full-plan` | Plan meaningful feature behavior, actors, invariants, failure modes and acceptance before implementation, including precise API contracts when needed. Use for new or changed workflows or explicit planning requests; skip trivial internal or cosmetic edits. |
| `hand-off` | Explain actual repository source, callers, architecture and behavior in Persian or English. Use EXPLAIN/EXPLORE for source questions; create developer and LLM handoff documents only for an explicit invocation or clear request for complete knowledge transfer. Skip generic theory, documentation sync and implementation-only work. |
| `integration-reliability` **new** | Design, implement or diagnose reliable third-party API and webhook integrations, including timeouts, retries, 429s, duplicates and uncertain external effects. Use for a real provider dependency, not internal CRUD or an ordinary local REST endpoint. |
| `load-testing` **new** | Plan and run bounded load, stress or concurrent-traffic benchmarks only when directly requested, with a validated target, authority and finite traffic profile. A slow endpoint or routine performance review does not request load generation. |
| `maintenance-evolution` **new** | Plan or implement bounded compatibility-preserving evolution, substantial refactors, deprecations, removals and major framework upgrades; assess scoped technical debt when requested. Skip routine implementation, small TODO cleanup and speculative future-proofing. |
| `multiple-pov` | Run a one-time, evidence-first brainstorming and multi-perspective design review before planning or implementing materially new systems, features, substantial workflows, architecture changes, major business logic, integrations, data-model changes, significant or risky refactors, migrations, or other substantial product/engineering work. Do not repeat the full review for the same materially unchanged task, user clarifications, approved implementation follow-ups, simple fixes, or small UI/content changes; use a focused delta review only after a material scope pivot or an explicit request to review again.
 |
| `natural-persian-writing` | Produce, rewrite, translate, review, or summarize meaningful Persian prose that sounds natural, preserves meaning, and matches its audience and purpose. Use for any Persian content: personal and formal letters, email, business, marketing, academic, legal and policy text, creative writing, translation, support, UI, technical documentation, and conversation. Do not activate merely because Persian appears in source code, data, an identifier, or text that is not being changed. |
| `performance-review` | Evidence-driven software performance review for recent changes, endpoints, imports/exports, and explicitly requested audits. Use to identify real bottlenecks and scalable improvements; do not use for speculative micro-optimization. |
| `practical-test` | Perform real browser acceptance tests for implemented user flows when directly requested or routed by steps with a confirmed safe running target. Use for observable UI behavior; skip static code review and implementation fixes. |
| `regression-check` | Verify that a completed change preserved important existing behavior within its realistic blast radius. Use after implementation, refactoring, bug fixes, database changes, or dependency updates; do not use for pure planning work. |
| `release-management` **new** | Prepare versions, release notes, provenance and deployment or rollback plans when directly requested, and execute specifically authorized release actions. Passing tests, a finished feature or a routine commit does not request publication, CI changes or deployment. |
| `root-cause` | Diagnose the actual cause of a bug, failure, or unexpected behavior before proposing or applying a fix. Use for explicit root-cause analysis, deep debugging, and recurring or unclear failures; do not replace ordinary implementation work without a reported problem. |
| `security-assurance` **new** | Review the relevant security surfaces of material auth, permissions, upload, secrets, payment, trust-boundary or dependency changes. A full feature or project security audit requires a direct request; routine CSS and unrelated local changes do not trigger it. |
| `skill-evals` **new** | Evaluate Codex skill structure and observed routing or workflow behavior when the user explicitly creates, upgrades, tests or audits a skill, package or steps. Do not use for ordinary application development or comparisons between AI models. |
| `steps` | Coordinate software development, bugs, refactors and engineering verification with proportionate governance, risk assessment and the minimum relevant specialists. Use for implementation work unless bypassed or a directly requested specialist owns the task. Exclude general IT support, commercial/legal advice and multi-model benchmarks; routine changes must not trigger full audits, release or load testing. |
| `technical-proposal-discovery` **new** | Produce a technical proposal or an evidence-backed competitor software comparison only on direct request. Distinguish proposal scope and deliverables from ordinary feature brainstorming; exclude commercial pricing, contracts and financial management. |
| `test-engineering` **new** | Design and implement meaningful unit, integration and contract tests for changed application behavior, APIs, business rules, permissions and data operations. Use existing project tooling; skip descriptive read-only work and trivial cosmetics without a behavior change. |
| `ui-ux-pro-max` | Use searchable local UI/UX data for meaningful interface design, accessibility, layout, typography, interaction and stack-specific implementation. Detect and preserve project tokens/frameworks; skip backend-only work and full design-system generation for trivial cosmetic edits. |

## Routing and authority

`steps` coordinates the minimum sufficient workflow. `CONTEXTUAL_AUTO` needs a concrete scope/risk/contract; `SUPPORTING` is a narrow complement; `EXPLICIT_ONLY` needs unambiguous direct natural-language intent or invocation; `OUT_OF_SCOPE` has no custom workflow. Activation and execution authority are independent.

Full audits, load tests, release/deploy/CI infrastructure, backup/recovery, technical proposals/competitor research, full teaching handoffs, WebSocket/SSE, WebGL/3D and presentable demos require direct intent. Implementing application jobs does not authorize server cron or starting workers. Source edits, Git writes, deployment and production data operations remain separate scopes.

Metadata remains discoverable, including explicit-only workflows, so natural-language requests can find them. This is an instruction-level policy, not runtime enforcement. Installation alone does not guarantee every request passes through `steps`. An optional project rule can make coordination deliberate:

```text
For software implementation tasks, use the steps skill to coordinate proportionate work and verification.
```

Add such a rule only under your project's governance; the installer never edits AGENTS.md. General IT/hardware support, personal finance/contracts, commercial estimates, logo ideation and multi-model comparisons are outside this package. Existing approved branding and technical workload estimates remain usable.

## Install or upgrade

Give Codex this prompt:

```text
Install all 26 personal skills from MahanManouchehri/skill-package v3.1.1. Read the manifest, resolve and verify the published commit SHA, use skill-installer at that exact ref into clean staging, verify every hash, and promote only approved names. For an upgrade, inspect active user roots and duplicates, make verified backups and use the tested journal/rollback tool. Preserve unrelated/system/plugin files and AGENTS.md. Report actual discovery and refresh requirements.
```

See [INSTALL_FOR_CODEX.md](INSTALL_FOR_CODEX.md) for staging/promotion and [RESTORE.md](RESTORE.md) for rollback/Windows fallback. The official installer refuses collisions and must not directly overwrite old skills. Python tooling requires Python 3 and [PyYAML](scripts/requirements.txt). PowerShell 5.1/7 execution and Windows-specific limits are separately identified in validation; do not infer runtime support from static review.

## Verification

```sh
python3 -B scripts/package_tools.py verify --package-root .
python3 -B -m unittest discover -s tests -p test_package_tools.py -v
python3 -B -m unittest discover -s evals -p test_runner.py -v
```

Keep environments/reports outside the distribution and remove owned generated caches before building. [VALIDATION.md](VALIDATION.md) and `validation-results.json` distinguish current checks from historical evidence, discovery from behavior, and unavailable checks from passes. The complete [60-case bank](evals/cases.json), [matrix](evals/MATRIX.md) and [runner](evals/README.md) are included. Routing/planning checks are not full framework/browser or production acceptance.

See [CHANGELOG.md](CHANGELOG.md), [AUDIT.md](AUDIT.md) and [PORTABILITY.md](PORTABILITY.md) for compatibility, provenance, dependencies and limitations.
