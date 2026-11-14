---
name: maintenance-evolution
description: Plan or implement bounded compatibility-preserving evolution, substantial refactors, deprecations, removals and major framework upgrades; assess scoped technical debt when requested. Skip routine implementation, small TODO cleanup and speculative future-proofing.
---

# Maintenance and Evolution

Change an existing system with an explicit account of its consumers, compatibility promises and removal criteria. Treat technical debt as an evidenced cost or risk, not a stylistic preference.

## Activation and input

**Policy: bounded CONTEXTUAL_AUTO.** Use for substantial refactoring, intended public removal/rename, major framework upgrades, or directly requested deprecation/debt assessment. A tiny internal rename with obvious bounded callers, routine feature or unnecessary TODO deletion does not need this workflow. Do not expand a module review into a whole-repository rewrite.

Establish the requested boundary, revision, current public/internal contracts, affected consumers, compatibility commitments, dependency support constraints and authorization to inspect/modify. Reuse known project policy; distinguish unknown external consumers from confirmed absence.

Modes: **COMPATIBILITY_CHANGE** for an evolution/refactor; **DEPRECATION** for a gradual replacement/removal; **DEBT_TRIAGE** for an explicitly bounded assessment. Assessment does not imply implementation permission.

## Method

1. Trace consumers across call sites, routes, serializers, jobs/events, configuration, database fields and available external-client contracts. Search actual usage and tests; lack of a repository reference does not prove external clients have migrated.
2. State the behavior to preserve and intended change. Identify breaking changes in shape, semantics, defaults, errors, permissions or timing. Separate a necessary contract change from incidental cleanup and do not silently enlarge the task.
3. Choose the smallest viable transition: keep an adapter/alias, introduce a compatible replacement, migrate consumers in stages, or make a coordinated cutover when evidence supports it. Explain coexistence and rollback limits; avoid parallel abstractions with no identified consumer benefit.
4. For deprecation, specify the replacement, notice channel, migration steps, owner and evidence needed for removal. Derive dates/windows from actual policy or owner decisions; do not invent commitments. Define how remaining usage is observed without exposing sensitive data and how stale consumers are handled.
5. For debt triage, record each issue's concrete location, recurring cost/risk, evidence, affected consumers and smallest remedy. Prioritize using observed failures, change frequency, maintenance burden and reversibility. Mark assumptions and do not fabricate numerical scores or commercial time/price estimates.
6. Implement only authorized changes in dependency order. Add tests for old/new behavior and transition boundaries; verify meaningful compatibility and failure cases. A framework upgrade must address actual version requirements and project integrations rather than blindly accept generated rewrites.
7. Define cleanup/removal exit criteria and retained fallback. Reuse current evidence from compatible revisions and rerun only checks invalidated by the change.

## Deliverable and acceptance

Return affected contracts/consumers, intended compatibility guarantees, chosen transition and rationale, scoped source/test changes or prioritized debt findings, migration/removal criteria, actual validation and unknowns. Use `VERIFIED`, `OWNER_CONFIRMED` and `UNVERIFIED` accurately. Keep speculative improvements distinct from required repairs.

Accept when consumer impact and breaking changes are explicit, the migration is proportionate, checks support preserved behavior and no unrequested rewrite was introduced. If a material breaking decision is unresolved, present that decision while continuing independent safe work.

## Ownership and authority

- `db-impact` owns persistence/migration blast radius; `architecture-review` reviews a concrete boundary change; `regression-check` verifies protected prior behavior; `test-engineering` implements tests. Reuse them when needed, not as an automatic sequence.
- `release-management` runs only for a directly requested release workflow. Deprecating code does not authorize publishing, deployment, server jobs, broader backups or production data migration.
- Project governance and existing task authorization determine actions. The skill cannot install a framework, rewrite Git history or delete live data merely because a transition would benefit.
