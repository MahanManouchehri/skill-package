# Source Investigation Contract v2

## Evidence-oriented discovery

1. Locate actual project root, current directory, language/framework/version using source manifests; read relevant project `AGENTS.md` and architecture docs as context, not as a substitute for source verification.
2. Search feature aliases, user-visible actions, routes, events, model names, database fields and common error messages. Use `rg --files` and focused `rg -n` searches where available; adapt to tools and languages; never claim exhaustive search without covering relevant directories and generated/registered code.
3. Identify **all discovered entry-point categories** within scope: HTTP routes and middleware, WebSocket channels/consumers, CLI, scheduled jobs, queued tasks, events/signals, webhook handlers and internal service APIs. For each, cite definition and registration.
4. Trace each material main flow from trigger to observed code effects: caller/callee, interface/implementation resolution, conditions, validation, authorization, reads/writes, state transitions, transaction boundaries, cache, broadcasts, jobs, outbound calls, exceptions and returned response.
5. Reverse trace central symbols with references/call hierarchy, including cross-module callers. Distinguish direct call, DI wiring, framework dispatch, observer/signal registration, conditional call, data relation, external boundary and unresolved dynamic dispatch.
6. For database, document fields and relations shown by current model/migrations/schema; reconcile migrations and runtime schema only if latter actually accessible and safely read. Do not assume migration history equals current deployed schema.
7. Review available tests to distinguish existing assertions from untested paths. Recommending a command does not constitute execution.
8. Record alternate/error paths that affect security, state or contracts; do not invent branches. Show call order where important (e.g., persist before dispatch or dispatch after commit).

## Important fact format

For each relevant central symbol capture:
- Exact identity/signature and source coordinate (`path:Lx-Ly`).
- Business responsibility and invocation condition.
- Verified direct caller(s) and indirect registration/wiring; cite both endpoints of the edge.
- Direct dependencies/callees and meaningful return value.
- Inputs, validation, permissions, writes, side effects and exceptions.
- Most likely **first edit point** vs related edits vs verification-only callers.

## Impact discovery stopping rule

Stop expanding into a shared dependency when its input/output contract and relevant effects are understood, further internal details are irrelevant to the requested change, or the code is external/unavailable. Record that boundary and uncertainty. Do not recursively inventory an entire repository.

## Framework discovery hints (never assumed layers)

- Laravel/PHP: `routes/*`, Kernel/bootstrap middleware, controllers, FormRequests, gates/policies, providers, container bindings, Eloquent models/observers/scopes, events/listeners/jobs, migrations, resources, API docs and tests.
- Django/Python: `urls.py`, views/DRF viewsets, serializers/permissions, services if present, models/managers/signals, `apps.py`, middleware, Celery tasks, schema/migrations and tests.
- Other stacks: derive actual registration and execution from observed manifests/config and code; don't shoehorn into Laravel/Django.

## Call edge confidence

`A -> B` is `SOURCE_VERIFIED` only when the calling expression and target resolution (or documented framework hook registration) have been examined. For dynamic lookup, label `possible target` and record how to resolve it. Annotate conditionally executed edges and error branches explicitly. Mermaid is permitted when it reveals branching/cross-component relationships, but it must not pretend dynamic edges are proven.
