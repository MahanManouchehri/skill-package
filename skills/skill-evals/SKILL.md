---
name: skill-evals
description: Evaluate Codex skill structure and observed routing or workflow behavior when the user explicitly creates, upgrades, tests or audits a skill, package or steps. Do not use for ordinary application development or comparisons between AI models.
---

# Skill Evaluations

Test what a skill makes an actual agent do, while keeping file validation and behavioral evidence separate. Instructions, a scenario bank and expected answers are not execution results.

## Activation and runtime boundaries

**Policy: EXPLICIT_ONLY.** A direct natural-language request to create, upgrade, test or audit a skill/package/`steps`, or an explicit invocation for that purpose, is sufficient. Ordinary Laravel/Django/frontend work, the word “test”, and general model benchmarking do not trigger this skill.

Metadata discovery may remain enabled so direct natural-language intent can find the skill. This is distinct from permission to start its workflow. `allow_implicit_invocation: false` removes normal discovery in runtimes that support that flag; it is not equivalent to an intent-sensitive explicit-only rule. Skill routing is model-driven, not guaranteed interception or an execution sandbox.

A skill does not create a worker or evaluation service. Use real available isolated CLI/agent sessions only when supported and authorized, and identify `IN_PROCESS` versus `DELEGATED` truthfully. No self-installation/update, production tests or credential copying as a side effect of evaluation.

## Input and case design

Establish the skill/package revision, current and proposed contracts, applicable governance fixtures, expected activation policies, available runtime/tools and safe execution roots. Inspect existing test conventions and preserve any owner-supplied case bank exactly. Choose **STRUCTURAL**, **TOOL**, **LIVE_BEHAVIOR** or a justified combination; a package upgrade normally needs all supported levels.

For package/orchestrator changes, target at least 30 meaningful scenarios and all newly added specialists; execute the full supplied bank when feasible and report designed versus executed counts separately. Include:

- Positive requests and adjacent negative prompts for every affected capability; minimum sufficient routing for tiny tasks.
- Explicit natural-language intent and named invocation, contextual specialists, supporting-only work and excluded subjects.
- Governance conflicts, untrusted repository text, authority boundaries and forbidden tool actions.
- Existing input/output contracts, preserved skill discovery, resource portability and concise but sufficient responses.
- Rework/resume, stale evidence, missing tools, dirty worktrees and actual failure recovery where relevant.

Each case needs an ID, realistic prompt/context, effective governance, expected behavior/allowed specialists, forbidden auto-routing/actions, required evidence and an observable verdict rule. Do not encode only a list of skill names or tell the tested model the expected answer.

## Execution

1. **STRUCTURAL:** strictly parse frontmatter/metadata; check names, descriptions, duplicates, activation declarations, relative resources, unsafe path/symlink escapes, dependencies, manifests, file/tree hashes and distribution exclusions. Run relevant validators. A keyword/regex check establishes only a file property.
2. **TOOL:** inspect helper scope, then run new/changed executables in isolated fixtures. Exercise clean install, collisions, idempotency, upgrades, verified backup, partial failure/rollback and tamper/omission detection when those mechanics changed. Protect unrelated/system/plugin content. Report the host actually exercised; macOS success is not Windows execution evidence.
3. **LIVE_BEHAVIOR:** discover the supported harness locally and inspect its command/options. Create fresh permitted fixture sessions with only the necessary artifacts, stable skill snapshot and effective governance. Use safe permissions and synthetic data. Record exact invocation, runtime/model, revision/version, prompt and tool trace; do not fabricate isolation or change project models to obtain favorable results.
4. Observe actual selected/read skills, tool calls, artifacts, refusals/gates, outcome and response sufficiency. A model saying “I used skill X” is weaker than an invocation/read trace. A planning-only route decision does not prove full implementation behavior; label the evaluated slice.
5. Compare the trace to the case assertion, including absence of forbidden actions. Equivalent verified minimal behavior can satisfy a tiny task without a particular skill only when the acceptance rule permits it; document the reason. A correct skill name with an unsafe action fails.
6. Reproduce real failures, make the smallest supported correction, and rerun affected cases. For before/after comparisons, use equivalent prompts, fixtures and runtime settings; do not conceal earlier failures or compare different conditions as causal evidence.

## Evidence and verdicts

Maintain per-case fields for structural, tool and live results, with evidence paths and `PASS`, `FAIL`, `BLOCKED` or `UNVERIFIED`. If a consumer requires `STATIC_PASS`, `TOOL_TEST_PASS`, `LIVE_BEHAVIOR_PASS`, `UNVERIFIED` and `FAIL` columns, preserve them independently. Do not aggregate unavailable live cases into a pass rate.

Report environment/time, source SHA or immutable snapshot hash, exact commands, case IDs, expected versus observed routing/actions, failures and limitations. Redact secrets from traces; never publish authentication/session files. `VERIFIED` describes inspected evidence, `OWNER_CONFIRMED` an owner assertion and `UNVERIFIED` an unobserved property.

If a live harness is unavailable, provide runnable cases/manual reproduction steps and mark behavior `UNVERIFIED`. If a critical invariant cannot be tested or a critical violation remains, report the exact release implication; do not certify full completion. Unrequested production/stress/deploy/restore, governance bypass, secret exposure, destructive installer behavior or hash mismatch is a critical failure, regardless of other passes.

`steps` owns task coordination; `test-engineering` can help implement meaningful helper tests; `regression-check` assesses preserved contracts; `final-check` owns full acceptance. Release, publication and installation require their own explicitly requested scope.
