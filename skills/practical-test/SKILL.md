---
name: practical-test
description: "Perform real browser acceptance tests for implemented user flows when directly requested or routed by steps with a confirmed safe running target. Use for observable UI behavior; skip static code review and implementation fixes."
---

# Practical acceptance testing

When directly requested in natural language or via `$practical-test` / `/practical-test`, or contextually routed by `steps` for a meaningful implemented UI flow with a confirmed safe running target, perform strict browser acceptance testing. A skill is an `IN_PROCESS` workflow unless a genuinely separate supported worker performs it; do not claim independence merely from loading it. Default an explicit whole-conversation request to **all implemented work in this conversation**; a scoped `steps` assignment may test only its identified requirements. Do not modify application source, dependencies, project configuration, database schema, Git history, deployment, or server state; test-data changes through authorized safe UI flows are governed below.

## Reconstruct the acceptance scope

Before testing, inspect the conversation from its beginning. The user’s requests and later corrections are the source of truth; later conflicting instructions override earlier ones. Repository diffs are supporting evidence only.

Create an internal requirement ledger for every item that was both requested and actually implemented or changed in this session. Do not include ideas merely discussed. Number items `R01`, `R02`, etc. For each item retain the requested behavior and all relevant details: user-visible outcome, business rules, validation, navigation/redirects, access control, labels/text, UI state, interaction, animation, loading/error/empty states, persistence, duplicate prevention, and explicit edge cases or visual requirements. Do not silently omit minor details.

## Obtain the target

After reconstructing the ledger, find a valid `http://` or `https://` application URL from the current request, a previously confirmed target in this conversation, or the verified target passed by `steps`. Confirm that it still belongs to the requested application, is running, and permits the intended tests. Use a single unambiguous confirmed target without asking again. If several targets conflict, resolve only that ambiguity. A historical URL without confirmed project/environment ownership is insufficient.

Only when no usable confirmed target can be found, ask for the URL of the already-running application, in Persian:

`آدرس پروژه‌ای که الان ران است را بده تا تست عملی را شروع کنم. خودم پروژه را مجدداً ران یا ری‌استارت نمی‌کنم.`

Do not guess a URL, hostname, or port. Once the user supplies or confirms the URL, do not ask them to invoke this skill again. Browser access alone does not authorize writes on a production target; use read-only flows or obtain the specifically missing permission for meaningful side effects.

Never start, stop, restart, kill, replace, or deploy the application server as a side effect of this test. In particular, never run `manage.py runserver`, `flask run`, `uvicorn`, Node package dev/start commands, Docker Compose startup, IIS/PHP development servers, or equivalents. Never run migrations for this test. If service management is separately requested and permitted, leave this verification phase and have `steps` handle that distinct operation before confirming a fresh target.

## Perform real browser acceptance tests

Use available real browser automation (Codex browser tooling first; otherwise installed Playwright or another existing browser capability). Open the supplied URL and interact with the actual application. Do not substitute code review, a route check, compilation, unit tests, or assumptions for browser evidence.

For every applicable requirement, test the happy path and the relevant negative/validation case. Also test, where applicable: reload/persistence, navigation and redirects, access/permissions, UI interaction, requested edge cases, and full end-to-end multi-page workflows. Prefer realistic user flows over isolated component checks. Open controls and menus, operate modals, type safe values, submit safe forms, reload, and revisit data when necessary.

For UI requirements, visually inspect the rendered page and post-interaction states for clipping, overlap, spacing/alignment, overflow, horizontal scroll, readable labels, exact visible text, selected/disabled/hidden states, modal sizing, loading, empty/error states, and requested animation behavior. Check browser-console errors and relevant failed network requests where tooling permits. Capture screenshots or other evidence when useful.

If browser automation is unavailable, first check for existing browser/Playwright capability. A temporary testing script may be created outside the repository, but never alter the app, package manifests, requirements, or dependencies solely to test. If practical browser testing remains impossible, mark affected items `BLOCKED`; never fabricate results.

## Authentication and safe test data

Use an existing browser-authenticated session first. Never invent, extract, reveal, or search for unrelated credentials. If login is required and no session is usable, ask the user to log in manually or provide a dedicated test login, then resume this same workflow. Report CAPTCHA, OTP, and 2FA as blockers; do not bypass them.

When safe data creation is required, use recognizable temporary values such as `PT-<timestamp>-...`, and clean them up only when clearly safe and reversible. Never perform irreversible or externally impactful actions merely for coverage, including real payments, invoices, messages, emails/SMS, important record deletion, or real external API effects. Mark such an individual scenario `NEEDS_APPROVAL`, state the exact required action, and continue independently testable scenarios.

## Result rules and test separation

Do not fix failures during this run and do not weaken a requirement to match the implementation. Record the state actually tested.

- `PASS`: the requirement was practically verified in a real browser and behaved as required.
- `FAIL`: actual browser behavior differs from the requirement.
- `BLOCKED`: a technical, environment, browser, or authentication blocker prevented testing.
- `NEEDS_APPROVAL`: testing needs a potentially destructive or externally impactful action.
- `NOT_APPLICABLE`: only when the requirement genuinely cannot apply to the implemented result.

Continue with independent scenarios when another one is blocked. Distinguish implementation failures from environment problems and pre-existing/unrelated runtime issues when possible. Reuse fresh test-engineering/regression evidence for context, but only actual browser observations count as practical verification; send the observed results to `final-check` for the overall completion judgment.

For every `FAIL`, preserve enough evidence to reproduce it: requirement ID and wording, exact test, expected and actual behavior, reproduction steps, affected URL/page, relevant console/network evidence, screenshot/evidence reference when available, and practical severity (`Critical`, `High`, `Medium`, or `Low`).

## Final report

End with a concise but complete report headed exactly `PRACTICAL TEST RESULT`. Include the target URL; counts for reconstructed requirements, tested, passed, failed, blocked, and needs approval; and the overall result.

Include this matrix:

| ID | Requirement | Test | Result | Evidence/Notes |
| -- | ----------- | ---- | ------ | -------------- |

Then include, even if empty where appropriate:

## Failures

Give full reproduction details for every failure.

## Blocked / Untested

List what could not be practically verified and why.

## Browser / Runtime Issues

List console errors, uncaught exceptions, failed API calls, HTTP 4xx/5xx requests, broken assets, and navigation errors encountered in the tested flows. Identify issues that appear unrelated/pre-existing when possible.

## Acceptance Coverage

State exactly: `X / Y reconstructed requirements were practically verified.`

Do not claim that everything works unless every applicable requirement was actually browser-tested and passed. End the report exactly with:

`Project server start/restart performed by practical-test: NO`
