---
name: backup-recovery
description: Design backup and recovery runbooks, verify backup integrity or rehearse/execute a restore only on direct request with appropriate scope. Ordinary database changes, migrations, application jobs and feature delivery do not trigger a backup service or production restore.
---

# Backup and Recovery

Make recovery requirements explicit and test recovery without assuming that a backup file is usable or that code rollback restores data.

## Activation, modes and input

**Policy: EXPLICIT_ONLY.** A direct natural-language request for backup, restore, disaster recovery or a restore rehearsal, or a relevant invocation, starts this workflow. Merely editing a schema, adding a SQLite column or writing a scheduled job does not.

Choose **PLAN**, **VERIFY**, **REHEARSE** or **RESTORE** according to the request and authority. “Design a production runbook; do not execute” remains plan-only. Production restore/deletion, retention changes, infrastructure configuration, server cron/service installation and live backup writes each require appropriate scoped permission or the designated owner. Reuse valid permission; do not infer it from a high task criticality or from mentioning production.

Establish the system/state boundary, current environment, owners, existing backup tools and locations, data sensitivity, retention policy, recovery dependencies and available evidence. Inspect applicable `AGENTS.md`. Gather RPO (acceptable data loss) and RTO (acceptable recovery time) when established; otherwise mark them unresolved rather than inventing guarantees.

## Method

1. Inventory separately: application code/artifacts; database/schema; uploads and other mutable state; configuration and secret dependencies. Identify what can be regenerated, what must be captured consistently, and any external provider state beyond local recovery control.
2. Review the actual backup mechanism, consistency point, engine/version constraints, encryption/access controls, retention and failure detection. Use installed appropriate tooling only. Do not print or copy secrets/customer data into the repository or an unapproved destination; reference secure retrieval responsibilities instead.
3. Define a concrete runbook: preflight and owner gates, source/target identities, backup selection/provenance, integrity checks, restore order, isolation, application quiescence where required, permissions, validation, cutover and failure/abort recovery. Separate proposed commands from executed commands and adapt paths/engines to observed facts.
4. Verify integrity at the relevant level. Checksums prove byte identity, not transaction consistency or restorability. Inspect format/catalog metadata safely and test restoration in an isolated permitted target when requested/authorized. Confirm version compatibility and required dependencies before the rehearsal.
5. For a **REHEARSE** operation, use synthetic or appropriately protected approved data and a separate target with no outbound notifications/payments/jobs. Bound disk/time/resource use and cleanup. Record the exact source snapshot and starting target state, exercise restore and failure paths, then verify schema/data/application invariants without exposing records.
6. Before **RESTORE**, confirm the exact live target, backup/recovery point, expected overwrite/data loss, owner authorization, current-state preservation and rollback/abort plan. Stop before mutation if any is ambiguous. Never restore over production merely to test a runbook.
7. Validate recovery through relevant counts/checksums, referential/domain invariants, file availability, permissions and a safe application smoke check. Measure observed recovery time/data-loss window only where evidence permits. Preserve failures and discrepancy findings rather than marking the presence of files as recovery success.
8. Retain the verified evidence/runbook and define responsible owners, rehearsal frequency and unresolved operational assumptions. Do not install cron or alter retention automatically; commands prepared for an owner remain unexecuted until authorized.

## Deliverable and acceptance

Return scoped assets, ownership/retention/consistency assumptions, RPO/RTO status, restore order and exact prerequisites, integrity/rehearsal evidence, abort/rollback instructions and unresolved gaps. Label observations `VERIFIED`, owner attestations `OWNER_CONFIRMED` and untested operational steps `UNVERIFIED`.

Accept with a concrete testable runbook or authorized verified recovery result. State `BLOCKED` for a missing critical permission/target/backup dependency while completing safe planning. Do not claim a recovery objective or backup is proven until the relevant restore/validation actually ran.

## Ownership boundaries

`db-impact` reviews schema/data migration hazards; `release-management` handles explicitly requested code-release rollback; `test-engineering` can implement recovery validation. This skill owns broader state recovery when requested. It is not a prerequisite for routine local migrations, and creating its instructions does not provision storage, transfer credentials, start workers or operate company infrastructure.
