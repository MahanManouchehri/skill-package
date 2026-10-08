# Portable Feature Context — {{FEATURE_NAME}}

> **Repository:** `{{REPO}}` | **Branch:** `{{BRANCH}}` | **HEAD:** `{{COMMIT}}` | **Working tree:** `{{DIRTY_STATUS}}` | **Captured:** `{{DATE_TIMEZONE}}`
>
> **Scope:** {{IN_SCOPE}} | **Exclusions:** {{OUT_OF_SCOPE}} | **Coverage:** {{VERIFIED_OR_PARTIAL}} | **Freshness:** snapshot, not live source

## ۱. Instructions to receiving LLM

- This is a **source-grounded but time-bounded** snapshot, not repository access.
- You may use exact file paths and code relationships recorded below, but never claim you personally opened or checked the source unless the user supplies it.
- For new changes or unrecorded methods, request the relevant file content/diff; do not invent paths, API contracts or runtime success.
- Keep `SOURCE_VERIFIED`, `RUNTIME_VERIFIED`, `DOCUMENTED`, `INFERRED`, `UNVERIFIED` distinctions intact.
- The human's new code or newer Git revision takes precedence over this snapshot.
- Do not reproduce private implementation details outside the needs of the user's question.

## ۲. Feature Scope and Vocabulary

What this feature does, the exact functionality included/excluded, glossary/aliases, and relationships to shared modules.

## ۳. Architecture and Navigation Map

| Component | Path + verified line | Symbol / Hook | Responsibility | Callers / Wiring | Dependencies |
|---|---|---|---|---|---|

Include enough concrete relationships to answer file-navigation questions **without** relying on developer-guide.md.

## ۴. Primary Execution Paths

For each important flow, include trigger + registration, caller -> callee pairs with both coordinates, conditions, input/output, main DB effects, async effects, failure/result paths. Mark dynamic edges as unresolved if needed.

## ۵. Contracts and Invariants

Endpoints, inputs/outputs, roles, validation, business rules, schema/state, transactions, external events and security boundaries known from inspected source. Distinguish observation from design explanation.

## ۶. Edit/Impact Locator

| Change goal | Primary Edit | Dependent Edit | Verify Only | Invariants / Tests |
|---|---|---|---|---|

Include actionable change and debugging pointers for independent follow-up conversations.

## ۷. Tests and Diagnostic Entry Points

Exact verified test locations, scope of their assertions, applicable non-executed commands, breakpoint/log locations and known error branches. Runtime verification must state what was actually run and observed.

## ۸. Evidence, Unknowns and Confidentiality

For high-value claims cite paths/lines. List missing runtime evidence, stale/partial sections and files needed for follow-up verification. No secrets/customer data/raw credential values. Mark any restricted or redacted implementation aspects.

## ۹. Context Freshness / Request More Source

State commit/dirty snapshot, how another LLM should detect potential staleness, and which precise source files, diffs or logs to request from the user when answers exceed this dossier.

## یادداشت‌های دستی (حفظ در REFRESH)

<!-- HAND-OFF:MANUAL:BEGIN -->
<!-- Add personal context or corrections without changing generated evidence. -->
<!-- HAND-OFF:MANUAL:END -->
