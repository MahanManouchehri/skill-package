---
name: release-management
description: Prepare versions, release notes, provenance and deployment or rollback plans when directly requested, and execute specifically authorized release actions. Passing tests, a finished feature or a routine commit does not request publication, CI changes or deployment.
---

# Release Management

Make a requested release identifiable, reviewable and recoverable. Report actual publication and deployment state rather than inferring it from a local commit or successful command submission.

## Activation and authority

**Policy: EXPLICIT_ONLY.** Direct natural-language requests for release preparation, release notes, version/tag/publication, deployment or release rollback, or an invocation for that purpose, trigger this workflow. Do not route here automatically after feature completion, tests or ordinary commit work.

Select **PREPARE**, **PUBLISH**, **DEPLOY** or **ROLLBACK** only as requested. Source edits, commit, push, tag/release creation, CI/infrastructure changes, deployment, migrations and destructive rollback are separate action scopes. Reuse existing explicit authorization for the matching scope; do not add ceremonial permission gates. Honor real owner-only/governance restrictions and obtain missing authority before the restricted action. A skill never grants it.

## Inputs and readiness

Inspect the correct repository/remotes, branch/upstream, dirty work, current SHA, version scheme, existing tags/releases, branch protections/CI, reviewed diff, acceptance evidence and deployment ownership/environment. Do not dump credentials or change unrelated account configuration. Identify which party operates deployment; do not assume it is always the user.

Resolve the target version from actual compatibility policy and published state. Never reuse/move an existing tag, downgrade accidentally, force-push or relabel a breaking release as compatible. A notes-only request needs no Git mutation.

## Method

1. Define the release contents and readiness criteria. Trace intended changes to current validation; distinguish fresh results from historical/invalidated evidence and name unresolved blockers.
2. Prepare a compact release manifest: repository, branch, exact source SHA, version, changes, compatibility/migration notes, dependencies/artifact hashes where relevant, tests, operational owner and rollback limits. Release notes describe actual user/developer impact without unsupported claims.
3. Before an authorized commit/push, inspect status/diff and stage only owned paths. Preserve unrelated/dirty work. Fetch/compare the authorized remote before publication and handle concurrent changes without destructive history operations.
4. Respect branch protection and required checks. If publication requires a PR or owner action, report `PR_PENDING`/`BLOCKED` precisely. A pushed feature branch is not merged main, and an unmerged PR is not the final release. Do not use an alternate repository or force action to bypass policy.
5. For authorized publication, create only unused version identifiers under project policy. Read back remote commit/tag/release or artifact provenance and verify it resolves to the intended SHA. Local commit success, queued CI or an API request returning an ID does not prove publication/deployment completed.
6. For explicitly authorized deployment, verify the concrete environment, artifact/SHA, configuration prerequisites, health criteria and rollback owner before mutation. Execute only permitted steps in dependency order. Stop on failed checks/migrations; do not seed, retry unsafe writes or proceed to later phases to conceal failure. Application job implementation does not authorize server cron or worker provisioning.
7. For rollback, determine whether reverting code is compatible with the current schema/data and irreversible external effects. Prepare the smallest permitted recovery; broader data restore belongs to a separately requested `backup-recovery` workflow. Do not promise that Git revert restores a database.
8. Verify observed completion/health at the intended target and record exact command/output, timestamp and revision. If a required observation is unavailable, state that limit and avoid a successful deployment claim.

## Output and acceptance

Return version/branch/SHA, release notes or manifest, actual GitHub/artifact/tag/PR URLs when verified, executed actions and results, compatibility/rollback boundaries and remaining owner actions. Label evidence `VERIFIED`, `OWNER_CONFIRMED` or `UNVERIFIED`; report `PR_PENDING`, `BLOCKED` or partial failure truthfully.

Accept with verifiable release provenance for actions actually requested, or a precise pending state. No unsolicited deployment, infrastructure/cron edits, production data mutation or secret disclosure. `final-check` audits overall acceptance; `regression-check` supplies preservation evidence; this skill does not replace either or automatically run load/security/backup workflows.
