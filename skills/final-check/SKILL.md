---
name: final-check
description: Audit an apparently completed implementation against the user's original request before declaring it finished. Use for explicit final verification and substantial implementation tasks; do not use as a generic code review or repeatedly during development.
---

# Final Check

Perform an evidence-based completion audit. The goal is to establish whether the requested work—not merely the code—has actually been completed.

Use this skill when the user invokes `/final-check` or `final-check`, asks for final verification, or a substantial implementation task is ready for its completion audit. Run it once at the end of the work, not as a recurring implementation check.

## Audit method

1. Reconstruct every meaningful original requirement from the current session. Include requested behavior, business rules, UI/UX, backend and database work, validation, permissions, edge cases, constraints, explicit non-changes, and components expected to remain untouched. Keep an internal checklist; do not silently omit requirements.
2. Inspect the actual implementation and relevant changed files. When useful and available, use `git status`, `git diff`, and `git diff --stat` to identify what changed. Do not commit, push, merge, rebase, deploy, alter Git history, or edit code as part of this audit unless the user explicitly asks for fixes.
3. Classify each requirement independently as `PASS`, `PARTIAL`, `FAIL`, or `UNVERIFIED`. `PASS` requires both implementation and sufficient verification. Code inspection alone cannot turn an untested implementation into `PASS`.
4. Check integration points that apply: routes and URLs, controllers/views, models and migrations, serializers/forms/templates, frontend state and JavaScript, APIs, authentication and authorization, relations and transactions, jobs, configuration, dependencies, imports, and existing call sites. Look specifically for code that was added but is never used.
5. Analyze regression impact, distinguishing confirmed regressions from potential risk. Consider changed interfaces, renamed fields, shared components, model behavior, routes, database compatibility, validation, API consumers, and backwards compatibility.
6. Record only testing evidence actually obtained: automated, manual, browser, or static inspection. Never say a test passed unless it was executed successfully. If browser-level functional verification is needed and the `practical-test` skill is available, use or recommend it as appropriate; this audit does not substitute for browser testing.
7. For schema or database changes, assess migration consistency, null/default behavior, existing-data compatibility, foreign keys, destructive operations, production impact, and rollback concerns. Never perform destructive production database actions.
8. Apply security review only where relevant: authentication, authorization and object-level access, input validation, file handling, secrets, injection, and privilege escalation.
9. Identify unnecessary changes only when supported by evidence: unrelated modifications, formatting churn, duplication, debug or dead code, commented-out code, unused imports, artifacts, or development values. Do not inflate minor style concerns into blockers.

Be skeptical but concise and factual. Prioritize correctness and fulfillment of the original requirements over code aesthetics. Do not invent defects, hide incompleteness, or modify code merely to make the audit pass.

## Required report

Return this structure exactly, with one overall verdict only:

```markdown
# Final Check

## Verdict

PASS | PARTIAL | FAIL

## Requirement Coverage

| Requirement | Status | Evidence |
| ----------- | ------ | -------- |

## Problems Found

Only real issues or meaningful risks. For each: severity (Critical, High, Medium, or Low), location, explanation, and recommended action. State `None found.` when applicable.

## Testing Status

State exactly what was tested, what passed, what failed, and what was not tested.

## Regression Risk

Low | Medium | High — explain the main reason briefly.

## Unverified Items

List every item that could not be verified, or state `None.`

## Final Conclusion

A short engineering conclusion on whether the work is genuinely ready to be considered complete.
```

Choose the verdict strictly:

- `PASS` only when all critical requirements are satisfied and sufficiently verified.
- `PARTIAL` when the main implementation exists but non-fatal requirements, tests, or verification remain incomplete.
- `FAIL` when a critical requirement is missing, incorrect, broken, or contradicted by the implementation.
