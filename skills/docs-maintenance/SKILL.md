---
name: docs-maintenance
description: Synchronize existing project documentation with real code, API or configuration changes, and write end-user guides when directly requested. Follow project documentation paths; skip unaffected docs and delegate source-code explanation or developer handoff to hand-off.
---

# Documentation Maintenance

Keep documentation accurate at the places readers already use. Preserve the project's structure, terminology, templates and useful user prose.

## Activation and modes

- **SYNC — CONTEXTUAL_AUTO:** an authorized code/API/configuration change invalidates existing documentation, or applicable project instructions require an update. First check whether documentation is actually affected; a no-change result is valid.
- **USER_GUIDE — EXPLICIT_ONLY:** the user directly asks for end-user instructions, in natural language or through an invocation. Feature implementation alone does not request a guide.

Do not create documents to demonstrate activity. A narrow source/caller question belongs to `hand-off EXPLAIN`; a requested developer takeover dossier belongs to `hand-off HANDOFF`, not an end-user guide here.

## Input and workflow

1. Read applicable `AGENTS.md`, nested rules, documentation indexes/templates and the source/diff for the requested behavior. Resolve the authoritative destination and required format first. A project rule such as API docs under `spec/api` overrides generic defaults; do not create an alternative `docs/hand-offs/` tree.
2. Identify impacted claims: actors/permissions, inputs, validation, outputs/errors, state transitions, routes, configuration defaults and operational commands. Distinguish implemented behavior from proposed behavior and source inspection from verified runtime behavior.
3. In **SYNC**, change only invalidated sections and prescribed related artifacts. Preserve unaffected prose, links, examples and schema contracts. Update generated docs through their established source/generator when available; avoid hand-editing generated output that will be overwritten. If no claim changed and governance imposes no update, explain briefly and leave docs untouched.
4. In **USER_GUIDE**, define audience and tasks, then describe verified prerequisites, actions, expected results and recoverable errors. Inspect the actual UI/feature or source-backed flow. Do not invent buttons, screenshots, roles or successful operations. Clearly label any source-only/unobserved steps; ask only when a missing fact materially prevents correct instructions.
5. Keep examples synthetic and secrets redacted. Preserve identifiers, routes, statuses and authorization semantics exactly. Use project language conventions and the Persian writing skill when available for meaningful Persian prose.
6. Check changed links, headings/anchors, examples and required schema/render checks. Validate commands only in an authorized safe environment; writing a deploy/cron/restore instruction does not authorize executing it. Reuse fresh test results instead of claiming another run.

## Output and acceptance

Provide changed document paths, the behavior/source that required each change, checks actually performed and remaining limitations. Use `VERIFIED` for inspected or tested claims, `OWNER_CONFIRMED` for owner assertions and `UNVERIFIED` for unavailable runtime observations. Do not label a source-derived UI flow browser-verified.

Accept when the smallest necessary documentation change follows project paths/formats, preserves protected prose/contracts and is traceable to actual behavior or the explicit guide request. If code and docs disagree and intent cannot be established, surface that bounded conflict rather than silently changing the product.

## Boundaries

`hand-off` owns source maps, technical explanation and portable LLM context; `full-plan` owns proposed feature contracts; `release-management` owns requested release notes/provenance. Use those skills only when their tasks are actually requested/needed. Do not publish, send a document, modify sharing or upload private content without scoped authority.
