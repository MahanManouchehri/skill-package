---
name: practical-test
description: "Perform strict browser-based acceptance testing for all work implemented in the current Codex conversation. Activate when the user explicitly types /practical-test; do not use for code review or for implementing fixes."
---

# Practical acceptance testing

When the user invokes `/practical-test`, act as an independent, strict QA and acceptance-testing agent for **all work implemented during the current conversation**. This is a verification phase: do not modify application source, dependencies, project configuration, database schema/data, Git history, commits, deployment, or server state.

## Reconstruct the acceptance scope

Before testing, inspect the conversation from its beginning. The user’s requests and later corrections are the source of truth; later conflicting instructions override earlier ones. Repository diffs are supporting evidence only.

Create an internal requirement ledger for every item that was both requested and actually implemented or changed in this session. Do not include ideas merely discussed. Number items `R01`, `R02`, etc. For each item retain the requested behavior and all relevant details: user-visible outcome, business rules, validation, navigation/redirects, access control, labels/text, UI state, interaction, animation, loading/error/empty states, persistence, duplicate prevention, and explicit edge cases or visual requirements. Do not silently omit minor details.

## Obtain the target

After reconstructing the ledger, first inspect the **same invocation message** for one explicit, valid `http://` or `https://` application URL. This includes a plain URL, a Markdown link, or a URL supplied alongside `$practical-test` or `/practical-test`. If exactly one is supplied, use it as the target immediately and continue the practical-test workflow; do **not** ask for the URL again. Treat it as user-provided, not guessed.

Only when the invocation message contains no usable URL, ask the user exactly for the URL of the already-running application, in Persian:

`آدرس پروژه‌ای که الان ران است را بده تا تست عملی را شروع کنم. خودم پروژه را مجدداً ران یا ری‌استارت نمی‌کنم.`

Do not guess a URL, hostname, or port—even if one appeared earlier. Once the user supplies the URL, whether in the initial invocation or a follow-up, do not ask them to invoke this skill again.

Never start, stop, restart, kill, replace, or deploy the application server. In particular, never run `manage.py runserver`, `flask run`, `uvicorn`, Node package dev/start commands, Docker Compose startup, IIS/PHP development servers, or equivalents. Never run migrations for this test.

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

Continue with independent scenarios when another one is blocked. Distinguish implementation failures from environment problems and pre-existing/unrelated runtime issues when possible.

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
