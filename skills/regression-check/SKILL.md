---
name: regression-check
description: Verify that a completed change preserved important existing behavior within its realistic blast radius. Use after implementation, refactoring, bug fixes, database changes, or dependency updates; do not use for pure planning work.
---

# Regression Check

Verify preservation of existing behavior after a change. Do not assume that a working new feature, a plausible diff, or green unrelated tests proves regression safety. Identify the actual regression surface, check high-risk existing behavior with evidence, and report remaining uncertainty honestly.

## Scope, authority, and governance

Start by reading applicable `AGENTS.md`, `RULES.md`, project instructions, and the current user request. Use the governing instruction order: current user instruction, applicable repository rules, documentation, then this skill.

Default role: `Detect → Evidence → Explain → Recommend`. Do not modify implementation, commit, push, merge, deploy, mutate production data, trigger real payments/notifications, run destructive SQL, or perform unsafe production actions unless the user explicitly asks for that specific action and governance permits it.

Treat explicit “must not change” requirements as protected existing contracts. An intentionally changed old behavior is `INTENTIONAL_CHANGE`, not a regression.

## Relationship with final-check

`regression-check` is responsible only for verifying preservation of existing behavior after a change.

It must not decide whether the entire user request or task is complete.

Its verdict—`PASS`, `PARTIAL`, or `FAIL`—applies only to regression safety within the verified scope. Only `final-check` may make the final completion judgment for the whole task.

`regression-check PASS` does not mean “the task is complete.” It means only: “No regressions were found within the verified regression scope, and important affected legacy behaviors passed the performed checks.”

Use `practical-test` for deep browser-level workflow verification when appropriate; do not duplicate it. If a confirmed regression exists but its cause is unclear, recommend or invoke `root-cause`; do not guess or turn this skill into deep debugging.

## Regression method

1. **Reconstruct the change and contracts.** Inspect the request, plan, diff, changed files, tests, and Git history when useful. Record intended changes separately from behavior that must be preserved.
2. **Map the regression surface.** Trace direct and meaningful indirect dependencies: callers, shared utilities/base classes/middleware/decorators, models and serializers/forms, routes/APIs, permissions, templates/frontend state, configuration, jobs, reports, raw SQL, imports/exports, integrations, and legacy paths. Do not invent consumers.
3. **Classify risk.** Consider scope, sharedness, public contracts, data/schema effects, permissions, state/workflow changes, side effects, dependency/framework updates, configuration, and production exposure. Use `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL` without inflating severity.
4. **Choose Quick or Deep mode automatically.** Use Quick mode for isolated, low-risk UI/style or internal changes with no shared contract. Use Deep mode for shared components, models/schema, APIs, permissions, workflows, payments, central utilities, broad refactors, dependency/framework changes, or governance-defined high-risk areas. Broaden only if evidence reveals wider blast radius.
5. **Verify targeted existing behavior.** Prefer the cheapest reliable evidence: relevant automated tests, focused API checks, representative call sites, browser testing through `practical-test`, safe query results, or static invariants when execution is impossible. Test nearby valid/invalid cases and relevant negative paths when risk warrants it; do not retest only the changed happy path.
6. **Assess non-code effects when relevant.** Check configuration, database relations/transactions/concurrency, idempotency, errors, background jobs and other side effects, reports/historical data, imports/exports, APIs, integrations, and legacy URLs/forms/records. Distinguish local, test, staging, and production; local success is not production proof.
7. **Compare with baseline when possible.** Use prior behavior, requirements, documentation, prior commits, existing contracts, or before/after outputs. Differential comparison is especially useful for refactors. If no reliable baseline exists, keep ambiguous failures as `UNCLASSIFIED_FAILURE` or `UNVERIFIED`; never call them confirmed regressions without evidence.

Stop when high-risk surfaces are verified, medium-risk surfaces have representative coverage, and remaining risk is low and documented. Do not run a full suite, every endpoint, all browser flows, or unrelated modules unless the change justifies it.

## Classification and evidence

Classify each check as `PASS`, `FAIL`, `UNVERIFIED`, `STATICALLY_REVIEWED`, or `NOT_APPLICABLE`. Every `PASS` needs actual evidence. Static inspection alone cannot prove behavior requiring execution.

Classify failures honestly:

- `CONFIRMED_REGRESSION`: unintended loss of previously valid behavior supported by evidence.
- `POTENTIAL_REGRESSION`: credible risk lacking confirmation.
- `PRE_EXISTING_FAILURE`: evidence shows it predates or is unrelated to the change.
- `UNCLASSIFIED_FAILURE`: insufficient evidence to attribute it.
- `NO_REGRESSION_FOUND`: no issue found within a specific verified scope.

For a confirmed regression, assign `CRITICAL`, `HIGH`, `MEDIUM`, or `LOW`; do not blame the recent change without support. Keep residual risk separate from change risk: `LOW`, `MEDIUM`, or `HIGH`.

## Required report

```markdown
# Regression Check

## Verdict

PASS | PARTIAL | FAIL

This verdict applies only to regression safety within the verified scope.

## Change Summary

Brief change description.

## Regression Risk

LOW | MEDIUM | HIGH | CRITICAL — brief reason.

## Regression Surface

Meaningful potentially affected areas only.

## Dependency Findings

Important direct or indirect dependencies only.

## Protected Existing Behaviors

Existing contracts expected to remain unchanged.

## Checks Performed

| Area | Verification | Result | Evidence |
| ---- | ------------ | ------ | -------- |

## Confirmed Regressions

For each: severity, affected behavior, evidence, expected behavior, actual behavior, likely component, and recommended next step. Otherwise state `No confirmed regressions found within the verified scope.`

## Potential Risks

Credible but unconfirmed risks, or `None.`

## Pre-Existing / Unrelated Failures

Relevant failures not attributable to the change, or `None.`

## Unverified Areas

Explicitly list unverified behavior and why, or `None.`

## Residual Risk

LOW | MEDIUM | HIGH — brief reason.

## Governance

Only restrictions that affected verification and confirmation that no restricted operation occurred.

## Final Assessment

For `PASS`: `No regressions were found within the verified scope. Critical and high-risk affected behaviors passed the performed checks.`

For `PARTIAL`: state the meaningful unverified areas.

For `FAIL`: state the confirmed regressions.
```

Use `PASS` only when no regression was found in the relevant verified scope, critical/high-risk surfaces were sufficiently tested, and remaining uncertainty is acceptable. Use `PARTIAL` for meaningful unverified scope, blocked testing, or medium/high residual uncertainty without a confirmed critical regression. Use `FAIL` for one or more meaningful confirmed regressions. Never claim universal absence of regressions unless verification was genuinely exhaustive.
