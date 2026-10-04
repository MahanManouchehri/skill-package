---
name: multiple-pov
description: >
  Run a one-time, evidence-first brainstorming and multi-perspective design review before planning or implementing materially new systems, features, substantial workflows, architecture changes, major business logic, integrations, data-model changes, significant or risky refactors, migrations, or other substantial product/engineering work. Do not repeat the full review for the same materially unchanged task, user clarifications, approved implementation follow-ups, simple fixes, or small UI/content changes; use a focused delta review only after a material scope pivot or an explicit request to review again.
---

# multiple_pov — Multiple POV Design Gate

Use this skill as a **one-time pre-implementation brainstorming and design-review gate**. Its question is: *Are we solving the right problem in the right way?* It complements, and never replaces, implementation planning, code review, security review, QA, or testing.

The first invocation produces a decision-oriented review and then stops. It must not produce code, migrations, an implementation plan, or a task breakdown. After the user responds, incorporate the decisions and continue through the repository's normal planning or implementation workflow without running the full review again.

## Gate decision

Before reviewing, classify the request.

### Trigger

Run the gate for materially new work whose implementation depends on unresolved product, business, data, security, workflow, integration, or architecture decisions. Typical triggers include:

- a new system, subsystem, feature, API, integration, automation, state machine, permission/authentication model, background job, queue, or event-driven workflow;
- a substantial workflow or major business-logic change;
- a material data-model change or migration whose design is not already approved;
- an architectural or high-risk refactor;
- planning any of the above.

When uncertain, ask: **Could choosing the wrong design now create meaningful user harm, security/data risk, operational burden, rework, or hard-to-reverse coupling?** If yes, run the gate.

### Do not trigger

Do not auto-trigger for:

- a simple bug fix with known behavior, typo, copy edit, formatting, rename, or small CSS/UI adjustment;
- implementing a known validation rule;
- debugging an implementation defect;
- writing tests for approved behavior;
- executing an already approved migration under the repository's separate authorization rules;
- continuing an approved plan or implementing a previously reviewed feature;
- a small follow-up, user clarification, answer to review questions, or implementation detail that does not materially alter the design.

A seemingly small fix may trigger only if inspection reveals a genuinely material product or design decision. State that discovery; do not silently broaden scope.

## One-shot state and task identity

Treat the current scope as having the behavioral state `MULTIPLE_POV_REVIEWED = true` after the first full review is delivered. No persistent file or machine state is required.

It remains the same task while these are materially unchanged:

- primary objective and business outcome;
- principal actors and core workflow;
- system boundary and fundamental architecture;
- data ownership and security model;
- major external integrations.

For the same task:

1. Allow exactly one full review.
2. Treat any user response—decision, clarification, partial answer, correction, or added detail—as continuation, not a new gate.
3. Summarize confirmed decisions and explicit assumptions, then proceed to planning or implementation.
4. Never restart the review merely because the same idea is reworded or more implementation detail appears.

The prohibited loop is `review → user answer → full review again`. Only an unresolved `BLOCKER` may prevent implementation after the user's response.

## Material scope change and delta review

A new review is allowed only for a genuinely new task, an explicit request for another review, or a material pivot such as:

- changing the main objective, core workflow, fundamental architecture, or data ownership;
- adding a principal actor or major integration;
- fundamentally changing authentication, authorization, or the security boundary;
- moving from local to distributed operation;
- introducing sensitive or regulated data;
- introducing a destructive migration or another hard-to-reverse data operation.

Prefer a **Delta Multiple POV Review**: identify the changed premise, preserve prior decisions that still hold, and review only affected perspectives, risks, unknowns, alternatives, and consequences. Do not repeat unaffected analysis.

## First-review workflow

### 1. Establish evidence

Before criticizing architecture, code, schema, or existing behavior:

- read applicable `AGENTS.md` and repository governance;
- inspect the smallest relevant set of code, models/schema, tests, configuration, and documentation;
- find existing concepts and constraints that could be reused;
- use confirmed decisions from the conversation.

Do not ask the user for information available through reasonable repository inspection. Respect all separate authorization gates. In particular, analysis of a possible database change does not authorize editing models, generating/applying migrations, or changing persistent data.

### 2. Reframe without hijacking the request

Distinguish, when useful:

```text
Underlying problem
User's proposed solution
Realistic alternative solutions
```

Ask internally whether the request describes the actual goal or one mechanism for achieving it. Preserve the user's stated objective and do not reinterpret it without evidence.

### 3. Separate epistemic status

Maintain a clear distinction:

- **Known:** confirmed by the user, repository evidence, or prior decisions.
- **Assumed:** plausible but unconfirmed; say why the assumption is reasonable.
- **Unknown:** missing information that could affect a decision.

Never present an assumption as fact. Attach confidence only when uncertainty is meaningful:

- `High confidence`
- `Medium confidence`
- `Low confidence` — phrase as a hypothesis or question, not a fact.

### 4. Brainstorm before converging

Treat brainstorming as first-class work. Explore only useful possibilities:

- a simpler, safer, cheaper, more maintainable, incremental, configurable, or repository-native route;
- reuse of an existing concept instead of adding a new source of truth;
- an MVP that delivers most value with materially less complexity;
- forgotten actors, scenarios, future constraint changes, and responsibilities placed in the wrong component;
- what is being hard-coded now that is likely to change in six months or two years.

Do not manufacture options to fill a list. Do not recommend microservices, event sourcing, CQRS, Kafka, Redis, distributed locks, queues, extra services, or elaborate patterns merely as “best practice.” Prefer the simplest design that safely satisfies known requirements and existing repository constraints.

### 5. Identify concrete strengths

Explicitly preserve what is sound: decisions that reduce complexity, improve UX, align with existing architecture, enforce a useful invariant, or deliver clear product value. Explain why each strength matters; generic praise is not a finding.

### 6. Scan relevant perspectives

Internally scan the catalog below, but surface only perspectives with material findings. Avoid theoretical noise and severity inflation.

- **User / UX / Accessibility / Localization:** benefit, expectations, friction, discoverability, happy path, loading/empty/error states, validation, recovery/undo, destructive actions, navigation, keyboard/accessibility, responsive behavior, language, RTL/LTR, timezone, date, currency, and number formats.
- **Product / Business / Stakeholders:** actual value, success criteria, scope, adoption, overlap, business invariants, cost, policy, staff workflow, and impacts on end users, customers, operators, admins, managers, support, finance, developers, and external partners.
- **Architecture / Domain model:** boundaries, ownership, coupling, cohesion, dependency direction, responsibility placement, entities, aggregates, terminology, lifecycle, invariants, illegal states, and synchronous versus asynchronous behavior.
- **Data / Database:** source of truth, integrity, constraints, uniqueness, referential integrity, nullable/duplicate/stale state, deletion semantics, history, transactions, migrations, and existing records.
- **State machine:** allowed and forbidden transitions, terminal states, retries, cancellation, re-entry, overrides, and races.
- **API / Integration:** contract, validation, authorization, idempotency, errors, versioning, pagination, backward compatibility, retries, timeouts, rate limits, auth, webhook duplication/ordering, fallback, dependency change, and vendor lock-in.
- **Security / Privacy / Abuse:** authentication, authorization, privilege escalation, IDOR, injection, mass assignment, replay, CSRF, secrets, exposure, enumeration, malicious input/files, collection necessity, minimization, retention, deletion, logging/backups, third-party exposure, and abuse by bots, compromised users, employees, or admins. Report only concrete, context-supported security concerns.
- **Concurrency / Reliability / Recovery:** duplicate submission/execution, races, lost updates, ordering, atomicity, partial success, crashes, dependency or database failure, safe retry, compensation, rollback, manual recovery, and lost responses after successful operations.
- **Performance / Scalability / Cost:** query count and N+1, indexes, payload, latency, CPU/memory/network/storage, hot paths, cache behavior, dataset/user/tenant/traffic growth, queue load, third-party limits, and development/infrastructure/support cost. Avoid premature optimization.
- **Maintainability / Developer experience / Testing:** complexity, readability, duplication, abstractions, hidden dependencies, future modification cost, debugging, reproducibility, configuration, documentation, happy/negative/edge cases, permissions, transitions, migrations, concurrency, failures, and integration tests.
- **Operations / Observability / Deployment / Rollback:** configuration, operational controls, incidents, logs, metrics, tracing, audit records, correlation IDs, admin/failure visibility, deployment order, rolling compatibility, feature flags, downtime, code/data rollback, irreversible operations, and compatibility with old app versions.
- **Migration / Backward compatibility:** mapping existing and invalid legacy records, verification, dual behavior, old clients/APIs/records/integrations/reports/URLs/scripts/automations, and rollback.
- **Delivery / Future change / Reporting:** critical path, MVP, avoidable scope, risky unknowns, hard-to-reverse choices, appropriate versus unnecessary flexibility, historical reconstruction, metrics, audit, and analytics.
- **Legal / Compliance:** consider only when supported by the domain or evidence; never invent a legal requirement.

### 7. Apply specialized checks when relevant

- **AI / LLM:** hallucination, prompt injection, data leakage, tool abuse, nondeterminism, evaluation, fallback, cost, and latency.
- **Payments:** duplicate payment, idempotency, reconciliation, rounding, refunds, settlement, provider outage, and auditability.
- **Files:** MIME/type verification, size, malicious content, decompression attacks, authorization, storage, retention, and parsing failure.
- **Notifications:** duplication, ordering, retries, stale notifications, preferences, unsubscribe, and notification storms.
- **Queues / workers:** at-least-once delivery, duplicate and poison jobs, retries, dead-letter handling, queue growth, and worker crashes.
- **Caching:** invalidation, stale or permission-sensitive data, tenant isolation, and stampedes.
- **Multi-tenant systems:** tenant-scoped queries, isolation, cross-tenant leakage, shared resources, and quotas.

### 8. Explore edge cases and failure modes

Prioritize plausible conditions at boundaries: absent/disabled actors, empty or legacy data, invalid transitions, retries, partial failure, double-clicks, concurrent actors, stale browser state, browser closure, network timeout, dependency outage, deployment across versions, and recovery by support staff. Do not dump every imaginable edge case.

### 9. Perform the mandatory internal red-team pass

Before writing the review, test the proposal against these questions:

- What is the most dangerous wrong assumption?
- What could cause data loss, unauthorized access, or inconsistent state?
- What happens if the operation runs twice, two users act concurrently, or it fails halfway?
- What happens if the operation succeeds but its response is lost, the browser closes, or a dependency times out?
- What happens to existing users, old records, and mixed-version deployments?
- How are rollback, manual recovery, support diagnosis, and developer debugging handled?
- Does the design create a second source of truth, excessive complexity, or an implicit critical requirement?
- Has the business goal been confused with the proposed technical mechanism?

Only plausible findings supported by the context belong in the output.

### 10. Trace second-order effects

For consequential decisions, trace only as far as useful:

```text
Decision
→ immediate consequence
→ operational consequence
→ future architectural consequence
→ maintenance consequence
```

Surface a chain when it changes the recommendation or exposes future obligations such as reassignment, history, admin tooling, escalation, capacity imbalance, or compatibility work.

### 11. Classify and prioritize

Use these finding types:

- `Requirement Problem`
- `Design Problem`
- `Implementation Risk`
- `Missing Information`
- `Opportunity`
- `Alternative`

Not every concern is a flaw in the user's request.

Use severity consistently:

- `BLOCKER`: do not implement until resolved; credible data loss, serious security issue, fundamental contradiction, invalid core logic, or impossible design.
- `HIGH`: likely redesign or serious production failure.
- `MEDIUM`: important but manageable without redesign.
- `LOW`: low-risk edge case or improvement.
- `NOTE`: useful observation.

Do not inflate severity. Merge overlapping findings and rank decision-changing concerns first.

## First-review output contract

Match the user's language. For Persian interaction, write user-facing analysis in natural Persian while retaining useful technical terms and code identifiers. Keep the response proportional to complexity and omit empty or irrelevant subsections.

Use this structure as the default:

```markdown
# Multiple POV Review

## 1. برداشت من از مسئله
- مسئلهٔ اصلی
- خروجی مورد انتظار
- مسیر پیشنهادی کاربر
- Known / Assumed / Unknown مهم

## 2. نقاط قوت ایده
[Concrete strengths and why they matter]

## 3. ایرادها و ریسک‌های اصلی
| Severity | POV | Type | Finding | Why it matters | Recommendation |
|---|---|---|---|---|---|

## 4. فرضیات پنهان و تناقض‌ها
[Only material items]

## 5. چیزهایی که هنوز مشخص نیست
### Must resolve
[Decision-critical unknowns]
### Can decide later
[Deferrable unknowns]

## 6. POV Summary
| POV | Status | Main finding |
|---|---|---|

## 7. Edge Cases / Failure Modes
[Prioritized plausible cases]

## 8. Brainstorm / Alternatives
### Option A — Proposed direction
### Option B — Recommended direction
### Option C — Minimal/MVP
[Include only useful options; omit Option C when irrelevant]

## 9. Recommendation
[One clear recommendation]

## 10. تصمیم‌هایی که از کاربر لازم دارم
[Only high-information decisions that affect architecture, business behavior,
security, data integrity, or implementation direction]
```

If the proposal is already sound, say so explicitly and explain the supporting evidence. Never invent criticism, alternatives, or questions merely to populate the template.

End the first review and wait for the user's decision. Do not include an implementation plan, detailed task sequence, code, model/schema edits, migration operations, or implementation work.

## After the user responds

Do not run the full review again. Briefly state:

- what the user confirmed;
- which alternative or behavior was selected;
- any important assumption you are making;
- any unresolved `BLOCKER`.

Then continue into the repository's normal planning or implementation workflow. If answers are partial, do not re-ask everything: resolve non-critical gaps with the safest reasonable assumptions, identify them explicitly, and continue. Stop only for a genuinely unresolved blocker or a separate required authorization.

## Delta-review output

For a material pivot, label the response `Delta Multiple POV Review` and include only:

1. changed premise and preserved decisions;
2. newly affected strengths, findings, and failure modes;
3. revised alternatives and recommendation;
4. new decision-critical questions.

After the user responds, the delta gate is complete and the same one-shot rule resumes.

## Internal self-check

Before delivering a full or delta review, verify:

```text
[ ] Is this genuinely new substantial work?
[ ] Has this scope already been reviewed?
[ ] Did I understand the real problem?
[ ] Did I inspect available evidence?
[ ] Did I separate facts / assumptions / unknowns?
[ ] Did I brainstorm alternatives?
[ ] Did I identify strengths?
[ ] Did I challenge weak assumptions?
[ ] Did I inspect relevant POVs?
[ ] Did I inspect edge cases?
[ ] Did I perform the red-team pass?
[ ] Did I consider second-order effects?
[ ] Did I avoid irrelevant theoretical risks?
[ ] Did I avoid over-engineering?
[ ] Did I prioritize findings?
[ ] Did I ask only decision-critical questions?
[ ] Did I avoid implementation?
[ ] Did I avoid detailed planning?
[ ] Is this exactly one review?
[ ] Will the workflow continue after the user's answer?
```
