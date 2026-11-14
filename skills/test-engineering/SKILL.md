---
name: test-engineering
description: Design and implement meaningful unit, integration and contract tests for changed application behavior, APIs, business rules, permissions and data operations. Use existing project tooling; skip descriptive read-only work and trivial cosmetics without a behavior change.
---

# Test Engineering

Turn requirements and real failure risks into executable evidence. Tests should distinguish correct behavior from plausible defects, rather than restate the implementation.

## Activation and input

**Policy: CONTEXTUAL_AUTO.** Select for meaningful behavior creation/change or an explicit test request. A prose explanation, typo or isolated cosmetic edit does not require a new test suite. Use focused verification for small changes; do not force a new framework or coverage target onto a stable project.

Inspect applicable governance, requested behavior, actual diff/callers, current test conventions and safe commands. Identify the tested revision, runtime, fixtures, dependencies, database connection and permitted execution environment without printing secret configuration. Examples include the existing PHPUnit/Laravel, Django/pytest or JavaScript setup; the framework is discovered, not prescribed.

Modes may be **STRATEGY**, **IMPLEMENT/RUN** or **FLAKY_DIAGNOSIS**. A strategy-only request does not authorize source edits or test execution with external effects.

## Method

1. Map each material behavior/invariant to a small set of test cases and a suitable layer. Favor unit tests for pure rules, integration tests for persistence/framework interactions, and contract tests for boundary shape/semantics. Add end-to-end coverage only where it proves a distinct risk.
2. Derive positive, negative, boundary and failure cases from the requirement. Include absent/invalid inputs, authorization roles and object ownership, conflicting states, duplicate operations, transaction failure and relevant concurrency. Do not add every category mechanically to every task.
3. Assert observable results: status/body/errors, persisted state, emitted jobs/events, absence of forbidden effects and important invariants. A mocked function being called is insufficient when the requirement is a durable outcome. Avoid assertions tied to irrelevant internal ordering or generated wording.
4. Reuse the project's fixtures/factories and minimal synthetic data. Verify that test database creation/reset/transactions target an isolated test database, never production. Keep tests independent; control clock, randomness and environment when those influence behavior. SQLite success does not establish MySQL or SQL Server locking, collation or DDL compatibility.
5. Isolate external delivery/payment/provider effects using established fakes or contract fixtures. Keep enough real integration to detect wiring, validation and transaction defects. Document any provider or browser behavior the fake cannot establish.
6. Write the smallest tests that would fail for the relevant defect; reproduce before the fix when feasible. Run the narrow suite first, then required affected checks. Inspect actual failures instead of weakening assertions, hiding errors or updating snapshots merely to pass.
7. For flaky tests, preserve the failing evidence, reproduce under the observed conditions, and investigate shared state, time, ordering, races or unreliable dependencies. Distinguish infrastructure failure from application failure. Quarantine only under project policy with an explicit known gap; retries do not turn a nondeterministic failure into proof.
8. Reuse current trustworthy results from the same revision/environment. Rerun only invalidated checks after changes; broaden testing for demonstrated blast radius, not ceremony.

## Output and acceptance

Provide concise behavior-to-test traceability, changed tests/fixtures, exact commands and environment, actual counts/results, remaining gaps and relevant failure artifacts. Distinguish newly executed results from historical ones. Use `VERIFIED`, `OWNER_CONFIRMED` and `UNVERIFIED` accurately; report `BLOCKED` with the missing prerequisite when execution cannot safely run.

Accept when tests cover the task's material success and failure behavior, commands actually ran where claimed, and no production state or real external delivery was used accidentally. A passing subset is not a whole-project guarantee. Do not fabricate a PASS, test count or framework execution.

## Ownership and authority

- Test implementation belongs here. `regression-check` identifies protected prior contracts and verifies preservation; `practical-test` owns actual browser acceptance; `final-check` owns the overall deliverable verdict. Reuse their evidence without claiming their work ran.
- Use `db-impact` for real schema/data compatibility questions and `security-assurance` for material permission/trust changes. Do not route load testing, release, backup or a full security audit merely because tests touch those domains.
- Installing tools, creating/resetting databases, changing shared services, starting infrastructure and invoking live providers require appropriate task/environment authority. If unsafe or unavailable, prepare the reproducible command/fixture and report the bounded unverified result.
