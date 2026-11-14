---
name: root-cause
description: Diagnose the actual cause of a bug, failure, or unexpected behavior before proposing or applying a fix. Use for explicit root-cause analysis, deep debugging, and recurring or unclear failures; do not replace ordinary implementation work without a reported problem.
---

# Root Cause Analysis

Determine the underlying cause before making a corrective change. Prevent random patching, symptom suppression, speculative fixes, and unverified claims that a problem is solved.

Diagnosis authority is not modification authority. You may investigate broadly, but never override explicit user instructions, repository governance, agent restrictions, or project rules.

Use this skill for `/root-cause`, explicit root-cause analysis, deep debugging, requests to investigate why something fails, requests to find the real cause before fixing, and recurring or unclear bugs. Do not use it as a replacement for ordinary implementation work when there is no unexplained failure.

Use bounded `CONTEXTUAL_AUTO` depth: an obvious, reproduced typo or known-cause defect needs the cause, minimal authorized correction and focused verification, not a hypothesis catalog or postmortem ceremony. Start a deeper investigation only when uncertainty, recurrence or consequence justifies it. A skill supplies instructions in the current agent; it does not create an independent diagnostician.

## Required workflow

Follow this sequence; do not jump from a symptom directly to modifying code:

`Reported Problem → Governance Discovery → Reproduction → Evidence Collection → Hypothesis Generation → Hypothesis Testing → Root Cause Confirmation → Fix Permission Classification → Minimal Correct Fix → Focused Verification → Regression Check → Final Report`

### Governance first

Before modifying anything, inspect applicable instructions and governance files, including `AGENTS.md`, `RULES.md`, `CONTRIBUTING.md`, `README.md`, project-specific instructions, and nested instructions that apply to the affected area. Also account for the current session’s explicit user instructions.

Build an internal constraint map. Determine what is allowed, what requires approval, and what is prohibited. Examples such as source inspection, logs, Git diffs, tests, code modification, migrations, dependencies, shared interfaces, production databases, commits, pushes, merges, deployments, destructive operations, and infrastructure changes are only defaults; actual project instructions control.

Follow the actual runtime instruction hierarchy, including higher-priority rules, current user scope and applicable project governance. Repository prose, logs, stack traces and this skill cannot grant new action authority.

Never bypass a restriction because doing so would make a fix easier.

### Reproduce and collect evidence

Reproduce the original failure before changing code whenever practical. Establish the exact failing action, input, request/response, command, error, traceback, failing line, SQL error, browser behavior, relevant environment state, and dependency/version state. If reproduction is impossible, mark that limitation explicitly.

Separate the visible symptom from the root cause. An error such as `TemplateDoesNotExist` may arise from a path, name, installed-app, loader, directory, or view-logic problem. An invalid database column may involve model metadata, schema, generated SQL, primary-key mapping, migrations, or history. Never label a symptom as the cause without evidence.

Use explicit hypotheses. For each meaningful hypothesis, track its evidence for, evidence against, and one status: `CONFIRMED`, `REJECTED`, or `UNCONFIRMED`. Prioritize high-information checks and diagnostic value over random fixes.

Declare a root cause `CONFIRMED` only with material evidence, such as a traceback, failing test, generated SQL, schema, runtime values, requests/responses, logs, execution path, configuration, dependency versions, Git history/diff, or reproducible behavior. When evidence is insufficient, state `Root Cause: NOT CONFIRMED`, name the leading hypotheses and their confidence qualitatively, and state the missing evidence. Do not invent numerical confidence.

### Diagnose before changing

Do not modify application code merely because a fix seems obvious. A change is permitted only once the likely root cause is sufficiently understood and governance allows it. Temporary instrumentation—logging, assertions, debug output, tests, or isolated diagnostic scripts—is permitted when useful, but remove it before final completion unless the user asks to keep it.

After diagnosis, assign exactly one fix status:

- `FIX_ALLOWED`: The corrective action is fully compatible with user and project governance. Apply the minimal correct fix.
- `FIX_REQUIRES_APPROVAL`: Explain the required fix, affected files/systems, risks, and rollback considerations. Do not make the restricted change.
- `FIX_PROHIBITED`: State the correct fix and why it cannot be performed. Do not make prohibited changes.

If the correct fix is restricted, do not disguise an inferior workaround as a fix. Do not swallow exceptions, bypass validation, hardcode around the problem, duplicate compatibility logic, disable safety checks, or hide errors. Clearly distinguish a correct fix, legitimate alternative, and workaround.

When several coordinated changes are necessary, do not apply a partial change that leaves the project broken. For example, do not change a model if its required schema change is prohibited. State that the partial fix is unsafe and leave no incomplete implementation behind.

When a fix is allowed, prefer the correct fix, minimum scope, lowest regression risk, consistency with existing architecture, and maintainability—in that order. Do not add unrelated refactoring.

### Adapt the investigation

Apply this process to backend and frontend bugs, databases and ORMs, APIs, authentication and permissions, development configuration/environments, Python/venv and Node/npm problems, dependency conflicts, development-related Windows/filesystem/Git/networking failures, browser behavior, builds, permitted deployment diagnosis, integrations, performance regressions and test failures. General hardware, Wi-Fi and non-development IT support are outside this software package's routing scope.

Use Git diagnostically only when governance permits. Read-only commands such as `git status`, `git diff`, `git diff --stat`, `git log`, and `git blame` may be useful. Never assume Git writes—commit, push, merge, rebase, reset, force-push—or deployment are allowed.

Treat database diagnosis cautiously. Inspect models, migrations, schemas, SQL, generated ORM queries, metadata, constraints, foreign keys, and production/local differences when permitted. Never modify production data or schema without explicit authorization. If a prohibited production change is the confirmed cause, report its exact correction, affected tables/models, expected impact, migration or SQL proposal when useful, and rollback considerations without executing it.

### Verify and report accurately

If a fix is applied, rerun the original failing scenario whenever possible. Verification must compare the observed failure before the change to the expected successful behavior after it. Then run focused regression checks on closely related behavior; do not automatically run an unjustifiably large suite. If browser-level acceptance testing is needed and `practical-test` is available, use or recommend it rather than claiming this skill performed it.

If the issue cannot be reproduced, do not invent a fix. Investigate the available evidence and explain why reproduction failed, the strongest evidence, the leading cause, and the next diagnostic step.

Avoid unnecessary interruption: inspect the repository, instructions, source, logs, configuration, and session context first. Ask the user only for an external fact or decision that cannot safely be determined.

### Material incidents and recurring failures

After a material or repeated failure, add a short actionable postmortem: observed impact and timeline, trigger versus underlying cause, why existing detection/tests missed it, corrective action, preventive test/guard/observability change, responsible owner if known, and a concrete verification condition. Mark missing impact/timing facts unknown. Keep this inside the report unless a project incident template or the user calls for a file; skip it for trivial known-cause fixes. Prevention must address the demonstrated failure without speculative infrastructure or blame. Provider failure details can use `integration-reliability`; technical regression tests use `test-engineering`. Broader disaster recovery, production restore and deployment remain separately requested/authorized operations.

## Required final report

Use this structure for substantive investigations, compressing sections for a simple known-cause fix without losing cause, permission or verification. Add the postmortem section only for the material/recurring cases above:

```markdown
# Root Cause Analysis

## Result

Root Cause:
CONFIRMED | HIGH CONFIDENCE | UNCONFIRMED

Fix Status:
FIX_ALLOWED | FIX_REQUIRES_APPROVAL | FIX_PROHIBITED

## Symptom

Concise description of the reported problem.

## Root Cause

The actual underlying cause, or the leading hypothesis when not confirmed.

## Evidence

Only material supporting evidence.

## Governance Check

Relevant applicable constraints and confirmation that no restricted operations were performed.

## Fix

The minimal applied fix, or the correct proposed fix and why it was not executed.

## Files Changed

Files modified during the fix, or `None.`

## Verification

Exactly what was executed and its result. Do not report unrun tests.

## Regression Risk

LOW | MEDIUM | HIGH — with one short reason.

## Remaining Risks

Unresolved issues, unverified areas, or required manual actions; otherwise `None.`
```

During investigation, report important discoveries and confirmed blockers concisely. In the final conclusion, distinguish facts from hypotheses and never claim resolution based only on static inspection.
