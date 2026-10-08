# Evidence, Coverage, and Quality Gate

## Evidence levels

- `SOURCE_VERIFIED`: actual declaration/config/call site examined and cited; proves code structure, **not deployed execution**.
- `RUNTIME_VERIFIED`: specific authorized command/test/check was actually run, result and environment recorded.
- `DOCUMENTED`: authoritative in-repo ADR or documentation claim; distinguish from current code.
- `INFERRED`: technical interpretation or hypothesis, explicitly marked and reasoned.
- `UNVERIFIED`: source missing, unclear runtime wiring, dynamic dispatch not resolved, or claims needing testing.

Never infer original developer intent merely from an observed pattern. Separate **observed fact** from **why the developer likely chose this pattern**. For missing behavior say `Not found in examined scope`, not `does not exist anywhere`.

## Coverage matrix for HANDOFF

Use `Verified | Partial | Unknown | N/A` for each:
1. Scope, feature boundaries, core entry points.
2. Primary and important alternate execution paths.
3. Direct/indirect call edges, DI and runtime registration.
4. Data models, main reads/writes, transactions and state transitions.
5. Validation, authorization and failure branches.
6. Async events, jobs, caching, integrations and order of effects.
7. Extension points, impact map and invariants.
8. Tests, debugger points, and how to verify modifications.

For every `Partial` or `Unknown`, document impact, reason, and next verification step; avoid unearned global coverage percentages.

## Full handoff completeness gate

- All *discovered* main user-visible paths are mapped from entry point to main effect and output, or clearly tagged partial.
- Security/state-changing paths have explicit verification status.
- Critical symbol navigation and important call edges have source coordinates; referenced paths exist, line ranges verified.
- No dependency is called a runtime execution merely because it is registered; no test pass is claimed without execution.
- Guide contains actionable edit paths, change impact, real tests/debug checks and uncertainty boundaries.
- LLM context contains independently sufficient **verified** structure, version metadata and response guardrails.
- Out-of-scope and external code boundaries are named; sensitive values are excluded.
- Existing documentation/user annotations survived update; only allowed files changed.

If any central main flow is unresolved, **call the result `Partial handoff`**, regardless of document length. Do not block delivery of useful verified portions.
