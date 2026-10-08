# Independent Development Playbook Contract

Every complete guide must train a developer to locate, change, debug, refactor and test the *actual feature*. Give concrete code-specific instruction, not generic architecture advice.

## Change recipe format

For each genuinely useful scenario (aim for 3 distinct scenarios if meaningful; never invent filler):
1. **Goal / existing behavior:** describe the actual starting contract and desired change category; an example change is hypothetical and labeled as such.
2. **Primary edit:** exact file/symbol/coordinate and why this is the main change point.
3. **Impact map:** `Primary Edit`, `Dependent Edit`, and `Verify Only`, including reasons backed by call/data edges. Referencing a dependency never automatically requires modifying it.
4. **Ordered approach:** technical sequence of inspection and edit decisions, invariants, security constraints, migration/API/backward-compatibility risks.
5. **Verification:** existing test names and what they assert, missing test cases, non-executed commands when safe, observable acceptance criteria and rollback strategy.

## Debugging recipes

For at least the main critical flow, map symptom -> entrypoint -> meaningful branch/breakpoint -> expected intermediate data/state -> concrete evidence to gather -> alternative root causes -> safe verification. Annotate hypotheses, never fabricate log messages. Favor methods available in repository IDE and runtime: Go to Definition, Find References, Call Hierarchy, targeted `rg`, debugger, logs with sensitive values redacted.

## Refactor recipes

- Identify behavioral invariants, public API, DB schema, event names, authorization boundaries and performance/concurrency caveats that cannot silently change.
- Determine currently coupled clients before extracting or renaming a component.
- Separate required refactor steps from optional architecture improvements; never assume the existing architecture is wrong because it differs from a pattern.
- Provide before/after testing plan; do not perform refactor under this skill.

## Testing recipes

- `Existing Tests`: named test files/assertions seen in source.
- `Missing Tests`: uncovered cases inferred from observed branches/constraints.
- `Verification Steps`: exact commands adapted to repo config and their side effects; default `NOT RUN`.
- A test file's existence does not prove passing or exhaustive coverage.

## Independent Development Readiness (qualitative)

The guide should let a new maintainer determine: (1) where to start, (2) why those files matter, (3) what else could break, (4) what must remain invariant, (5) where to pause a debugger, and (6) how to verify without AI. If any essential answer is unknown, say which evidence would close the gap.
