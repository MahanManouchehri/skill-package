# Engineering Lens

Use this reference for code, implementation strategy, stateful workflows, integrations, and performance. Inspect the actual code and call paths before asserting a problem.

## Trace and challenge

Follow the relevant request or event from input to every observable effect. Verify callers, validation, permissions, business rules, state transition, persistence, queues/webhooks, external APIs, error responses, and downstream readers. Look for a second entry point that bypasses a rule, a changed contract with unmodified callers, duplicated validation, or legacy code retaining old semantics.

Ask only questions supported by the system shape:

- What invariant must always hold, and where is it enforced?
- Can two actors or retries violate it? Is the operation idempotent when it needs to be?
- What is committed before a timeout, crash, or external side effect? How is partial success detected and recovered?
- Are error semantics compatible with callers and safe for retry?
- Does a new dependency, abstraction, background worker, cache, or event flow solve a demonstrated problem rather than move complexity elsewhere?

## Failure and boundary analysis

Select relevant cases instead of listing all of them: empty/null/invalid inputs; zero/one/maximal data; duplicate, stale, deleted, or old-format state; authorization distinctions; concurrent updates; repeated requests; delayed/out-of-order events; dependency timeout/outage; malformed responses; interrupted deployment; mixed old/new versions; and unexpected load.

For meaningful failure modes, record the failure, impact, likelihood only when evidence supports it, detectability, existing control, and smallest mitigation. Do not fabricate numeric FMEA scores.

## Performance and maintainability

Treat performance as a design concern only where a concrete workload, unbounded operation, N+1/query pattern, hot path, payload, I/O, memory, CPU, cache, or external quota makes it relevant. Ask what changes at 10x usage or when the feature succeeds unusually well.

Challenge complexity through concrete cost: ownership ambiguity, coupling, hidden dependencies, testing burden, operational burden, duplicate logic, unexplained configuration, or a source of truth split. Also challenge underengineering: frontend-only rules, missing failure behavior, non-atomic state changes, and undocumented manual recovery.
