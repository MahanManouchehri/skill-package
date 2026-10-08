---
name: performance-review
description: Evidence-driven software performance review for recent changes, endpoints, imports/exports, and explicitly requested audits. Use to identify real bottlenecks and scalable improvements; do not use for speculative micro-optimization.
---

# Performance Review

Analyze runtime cost and performance risk without optimization theater. The goal is measurably better performance with minimal complexity and preserved correctness, integrity, and security.

## Modes and authorization

Choose the narrowest applicable mode:

- `CHANGE_FOCUSED` (default): review only surfaces realistically affected by a recent change, feature, patch, refactor, query, API, report, import/export, or job.
- `ENDPOINT_REVIEW`: deeply inspect a named route, API, page, view/controller, search, or report.
- `FULL_AUDIT`: only for an explicit subsystem- or project-wide audit.
- `FIX_MODE`: only when the user explicitly asks to find and fix or review and optimize. Analyze and baseline first; make the smallest justified change; remeasure and regression-check it.

Default behavior is read-only: discover, measure, analyze, explain, recommend. Do not alter application code, schema, indexes, infrastructure, cache/queue architecture, deployment, or configuration unless `FIX_MODE` was explicitly authorized and project governance permits it.

## Governance first

Before performance-sensitive commands or changes, inspect applicable `AGENTS.md`, `RULES.md`, contribution/testing/deployment/database guidance, nested instructions, and the user request. Build a constraint map. Follow this precedence:

1. Current explicit user instruction
2. Repository governance
3. Project documentation
4. This skill

Never bypass restrictions for measurement. Never benchmark destructively, load-test/stress-test production, flood endpoints, make massive writes, exhaust resources, deploy, push, or modify production schema without explicit authorization and applicable approval.

## Context and evidence

Identify, when available: critical path, user/request frequency, dataset size and growth, latency/throughput expectations, business importance, sync vs async needs, and environment (`LOCAL`, `TEST`, `STAGING`, `PRODUCTION`). Do not invent scale or targets. State uncertainty and distinguish environments: local timings and engines do not prove production performance.

Ask first whether a meaningful bottleneck or credible scaling risk exists. If not, conclude `PASS` / no optimization needed. Do not add complexity for theoretical speed.

Establish a comparable baseline whenever practical: latency, query count and slowest query, execution plan, CPU, memory, response size, throughput, job duration, and external calls. Keep cold/warm behavior and input, dataset, environment, and cache state comparable. Do not claim p95/p99 from small samples or improvement without before/after evidence.

Assign every finding one confidence level:

- `MEASURED`: reproducible runtime data, profiling, timing, memory observation, query count, or plan.
- `STRONG_EVIDENCE`: code clearly indicates likely cost, but measurement is unavailable.
- `POTENTIAL`: credible but insufficiently evidenced risk.

Never present `POTENTIAL` as fact. If slowness is measured but its cause remains unclear, recommend `/root-cause` rather than guessing.

Prioritize by real impact: frequency x cost x business importance, adjusted for confidence and implementation cost. Use only relevant categories, such as `DATABASE`, `N_PLUS_ONE`, `QUERY_SHAPE`, `INDEX`, `PAGINATION`, `MEMORY`, `CPU`, `ALGORITHM`, `SERIALIZATION`, `RESPONSE_SIZE`, `EXTERNAL_IO`, `NETWORK`, `FILE_IO`, `CACHE`, `LOCKING`, `TRANSACTION`, `SYNCHRONOUS_WORK`, `FRONTEND`, `IMPORT_EXPORT`, `BATCHING`, or `UNKNOWN`.

## What to inspect

Inspect only what is in scope and plausibly expensive.

- **Database:** query count and latency, joins, filters, ordering, grouping, aggregates, subqueries, `EXISTS`, `DISTINCT`, scans, N+1, eager loading, pagination, row counts, transactions, locks, batching, and plans. Query count is evidence, not a universal target, and one query can be expensive. Use safe `EXPLAIN`/engine-specific plan tooling only when permitted. Account for engine differences.
- **N+1 and ORM:** detect list-plus-per-row relation queries in code, serializers, and templates. For Django, choose `select_related`, `prefetch_related`, annotation, or restructuring based on relation and access pattern; do not eager-load blindly. Similar framework-specific choices apply to Laravel/Eloquent and other ORMs.
- **Indexes:** recommend only from query shape/frequency, table size, selectivity, ordering/join use, existing composite indexes, write volume, and engine behavior. An index, schema, denormalization, or partitioning proposal requires `/db-impact` before execution; do not apply it by default.
- **Data and memory:** detect over-fetching, unbounded lists/responses, large serializers, `SELECT *`, loading complete files or querysets, duplicate copies, and giant in-memory structures. Consider projection, pagination, streaming, iterators, chunking, or bounded buffers only if the data volume warrants it.
- **CPU/algorithm:** look for costly parsing, repeated regex/transforms, unnecessary sorting/scans, nested loops, and repeated work. Treat complexity as meaningful only at realistic input sizes.
- **External and file I/O:** separate application time from external latency. Review request count, sequential independent calls, timeouts, retries/backoff, connection reuse, rate limits, response size, disk/file access, and redundant parsing. Recommend concurrency only if independent, safe, rate-limit compatible, and worthwhile.
- **Caching and background work:** first remove work, improve query/code, batch, or reduce payload. A cache recommendation must specify key, data, scope, TTL, invalidation, staleness, memory, consistency, and tenant/permission isolation. Recommend queues/workers only for genuinely long or costly work, considering operations, retries, idempotency, and user feedback.
- **API/frontend:** inspect payload/serialization shape, nested per-object work, repeated fetches/renders, hydration/bundle/DOM cost, image size, and large list rendering only when relevant. Do not break response contracts without explicit design approval; suggest `/api-contract-review` when available.
- **Imports/exports:** examine per-row queries/writes/validation, transaction size, streaming, chunking, batch size, duplicate checks, and external I/O. Evaluate bulk operations against signals, hooks, validation, custom logic, and correctness semantics.
- **Transactions/locking:** only with evidence or realistic concurrency; identify long transactions, external I/O inside transactions, contention, hot rows, and lock duration. Never trade integrity or correctness for speed.

Do not recommend Redis, caching, indexes, cursor pagination, async jobs, or concurrency by default. Do not weaken authorization, validation, CSRF, encryption, transactions, permissions, security, or data integrity for performance.

## Recommendations and fixes

For each material recommendation, weigh implementation cost, expected benefit, and regression risk as `LOW`, `MEDIUM`, or `HIGH`. Significant complexity needs significant measured or credible benefit. Separate low-cost/high-benefit/low-risk quick wins from structural changes such as cache layers, queues, distributed processing, denormalization, partitioning, or redesign; recommend `/architecture-review` for the latter.

In `FIX_MODE`, use this order:

1. Establish a baseline and confirm the root performance cause.
2. Select the smallest correct optimization allowed by governance.
3. Apply it.
4. Rerun the same measurement and compare results.
5. Verify correctness and run or recommend `/regression-check`.

If improvement cannot be demonstrated, report `NO_MEASURABLE_IMPROVEMENT`; do not describe the code as optimized. Consider rollback for structural changes.

## Report format

Use this structure, omitting inapplicable technical sections and keeping an already-efficient review short:

```markdown
# Performance Review

## Review Type
CHANGE_FOCUSED | ENDPOINT_REVIEW | FULL_AUDIT
State FIX_MODE separately if used.

## Verdict
PASS | OPTIMIZATION_RECOMMENDED | PERFORMANCE_RISK | INCOMPLETE

## Release Recommendation
GO | GO_WITH_CAUTION | NO_GO

## Scope
## Performance Context
Critical Path, Expected Load, Dataset, Environment, and Performance Requirement; state unknowns.

## Baseline
Measured latency/query count/slowest query/memory/response size/throughput/external calls, or "Not sufficiently measured."

## Findings
### [SEVERITY] - title
Confidence: MEASURED | STRONG_EVIDENCE | POTENTIAL
Problem, Evidence, Impact, Root Performance Cause, Recommended Optimization,
Expected Benefit, Implementation Cost, Regression Risk, Tradeoff, Verification.

## Database
## Application / CPU
## Memory
## External I/O
## Payload / Serialization
Include only applicable sections.

## Quick Wins
## Structural Improvements
## Performance Regressions
## Unverified Areas
## Governance
## Residual Performance Risk
LOW | MEDIUM | HIGH | CRITICAL, with a brief explanation.

## Required Actions Before Release
## Optional Improvements
## Final Assessment
```

Use severity independently from confidence: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`, or `INFO`. Reserve critical/no-go for expected normal-use failure, severe latency, exhaustion, or major overload, not cosmetic opportunities. `PASS` means no meaningful issue was found within the reviewed scope, not that the entire application is performant. `INCOMPLETE` means relevant surfaces could not be evaluated sufficiently.

Activate for `/performance-review` and requests such as performance/bottleneck review, slow API diagnosis, N+1/query-count inspection, query-flow optimization, scaling review, import/export speed, report performance, or memory analysis. `/performance-review endpoint`, `/performance-review full`, and `/performance-review fix` map to `ENDPOINT_REVIEW`, `FULL_AUDIT`, and `CHANGE_FOCUSED + FIX_MODE` respectively.
