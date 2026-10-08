---
name: db-impact
description: Analyze the complete blast radius of a proposed database change before it is executed. Use for migrations, schema/data changes, and production-impact reviews; do not use for ordinary read-only data queries.
---

# Database Impact Analysis

Analyze the complete impact of a proposed database-related change before execution. A schema change is not merely a migration: it changes data, application behavior, compatibility, history, and production risk.

Act as an evidence-based, governance-aware, production-aware safety gate. Determine what changes, what depends on it, what can break, whether existing data remains valid, what migration or manual action is needed, how rollback works, and whether execution is permitted. Technical feasibility never proves safety.

## Scope and relationship

Use for adding, removing, renaming, or converting fields and tables; null/default/constraint/index/PK/FK changes; relationship and `on_delete` changes; normalization or denormalization; data migrations; enums; identifiers; legacy schema integration; ORM/schema mismatch; and production schema alignment.

- `architecture-review` asks whether a data design is architecturally sound.
- `db-impact` asks what will happen if the database change is made.
- `root-cause` diagnoses database-related failures.
- `final-check` audits a completed implementation.

Typical flow: `full-plan → architecture-review → db-impact` when the change affects a database, then implementation, focused regression verification, `practical-test` when applicable, and `final-check`.

## Authority and governance

Analysis authority is not execution authority. Start by inspecting applicable `AGENTS.md`, `RULES.md`, `CONTRIBUTING.md`, README, database/deployment documentation, nested instructions, and the current session’s user instructions. Build an internal map of allowed, approval-required, and prohibited operations.

Follow precedence:

1. Explicit current user instruction.
2. Applicable project governance.
3. Repository documentation.
4. This skill’s defaults.

By default, perform analysis only. Never automatically run migrations, alter schema, modify a production database, delete or backfill production records, run destructive SQL, commit, push, or deploy. Execute a database change only if the user explicitly instructs that specific action and applicable governance allows it; complete this analysis first. If the correct action is prohibited, report it without executing it.

Always classify execution as exactly one of: `ANALYSIS_ONLY`, `READY_FOR_EXECUTION`, `REQUIRES_APPROVAL`, `BLOCKED_BY_GOVERNANCE`, or `DO_NOT_EXECUTE`.

Do not apply an allowed partial change when its prohibited companion change would leave the system inconsistent. State that partial execution is unsafe.

## Analysis workflow

1. **Define the change precisely.** State current and proposed schema/data state. Do not analyze a vague interpretation when repository evidence clarifies the intended change.
2. **Inspect actual state.** Compare relevant ORM models, migrations, accessible/documented schema, raw SQL, tables, constraints, indexes, triggers/procedures, legacy mappings, forms, serializers, APIs, reports, imports/exports, tests, and call sites. Do not assume model, migration, and database state match.
3. **Map schema impact.** Identify affected tables, columns, constraints, indexes, relationships, PK/FK behavior, cardinality, generated/auto-increment values, identifiers, collation, and engine-specific behavior.
4. **Analyze existing data.** Determine whether current rows remain valid. Check nullability, duplicates, conversion safety, length limits, FK resolution/orphans, `on_delete`, stored enum values, historical meaning, and possible loss. Never analyze schema in isolation.
5. **Find dependencies.** Search models, managers/querysets, forms, serializers, controllers, services, templates, frontend code, admin, tests, APIs, reports, ETL/jobs, search/filter/order code, validation, permissions, integrations, and third-party consumers. Explicitly find non-ORM references: raw SQL, stored queries/procedures, BI/reporting, cron jobs, scripts, import/export, and manual SQL tooling.
6. **Classify migration requirements.** State whether schema migration, data migration, and manual production action are each `YES` or `NO`, with a reason.
7. **Assess production and deployment.** Consider table size when known, locking, long-running operations, indexes, full-table writes, downtime, backfill, constraint validation, mixed old/new app versions, deployment order, observability, and rollback timing. Prefer an additive expand/contract sequence when a destructive or breaking change needs staged compatibility; do not require zero downtime when the project does not need it.
8. **Assess integrity, compatibility, and rollback.** State whether integrity improves or weakens; identify source-of-truth, FK, uniqueness, invalid-state, deletion, and historical-preservation effects. Classify compatibility as `BACKWARD_COMPATIBLE`, `PARTIALLY_COMPATIBLE`, or `BREAKING`; classify rollback as `FULLY_REVERSIBLE`, `REVERSIBLE_WITH_BACKUP`, `PARTIALLY_REVERSIBLE`, or `NOT_REVERSIBLE`. A reverse migration alone does not prove data recovery.
9. **Specify evidence and checks.** Distinguish `CONFIRMED IMPACT` from `POTENTIAL RISK`. When production data is unavailable, never claim its condition; provide only the required precondition query or verification step, subject to governance.

## Special scrutiny

- **Primary-key changes:** inspect child FKs, ORM expectations, URLs/API IDs, caches, imports/exports, external/legacy references, serialization, history, and joins. Never treat as a simple field edit.
- **Foreign keys:** verify target uniqueness/type, source values, orphans, nullability, `on_delete`, indexes, query behavior, migration order, and suitability of any `to_field`.
- **Enums/choices:** distinguish stored values from labels; inspect legacy values, validation, comparisons, APIs, reports, and filters. A label-only change may not require data migration.
- **Renames:** establish whether the migration is a true rename, remove-and-add, compatibility alias, or staged migration. Look for old-name dependencies and destructive ORM inference.
- **Destructive changes:** explicitly identify drops, truncation, incompatible conversion, overwrite, irreversible normalization, lossy merges, length reduction, and duplicate deletion. Identify the minimum backup/snapshot requirement when relevant; do not perform it without authorization.
- **Multiple engines/environments:** distinguish local, test, staging, and production. Account for SQLite/PostgreSQL/MySQL/SQL Server differences in syntax, constraints, types, indexes, datetime/case behavior, and identifier rules when relevant.

## Risk and recommendation rules

Use a primary verdict of exactly one: `SAFE`, `LOW_RISK`, `MEDIUM_RISK`, `HIGH_RISK`, `BREAKING`, or `DESTRUCTIVE`. Add flags only when relevant: `MIGRATION_REQUIRED`, `DATA_MIGRATION_REQUIRED`, `PRODUCTION_SENSITIVE`.

Do not call every migration high risk, invent production conditions, hide destructive behavior, or claim local behavior equals production. Suggest a safer alternative—such as staged additive migration, nullable field plus backfill plus later constraint, a compatibility period, preserved column, or mapping layer—only when it addresses a real risk.

When appropriate, recommend a minimal pre-execution checklist: validate data preconditions, snapshot/backup affected data, verify compatibility, test in staging, run focused tests, and obtain required approval. Recommend targeted post-change verification: migration result, old-record reads, create/update behavior, relationships, reports, API compatibility, and orphan checks. Use `practical-test` only when browser-level behavior needs testing.

## Required output

```markdown
# Database Impact Analysis

## Verdict

SAFE | LOW_RISK | MEDIUM_RISK | HIGH_RISK | BREAKING | DESTRUCTIVE

Optional flags: MIGRATION_REQUIRED | DATA_MIGRATION_REQUIRED | PRODUCTION_SENSITIVE

## Proposed Change

Current:
...

Proposed:
...

## Schema Impact

Affected tables, columns, constraints, indexes, and relations.

## Existing Data Impact

Effects on existing rows and validation unknowns.

## Application Dependencies

Only meaningful affected components or files, including raw SQL and integrations when relevant.

## Migration Requirements

Schema Migration: YES | NO
Data Migration: YES | NO
Manual Production Action: YES | NO

## Data Integrity

Relevant risks or improvements.

## Backward Compatibility

BACKWARD_COMPATIBLE | PARTIALLY_COMPATIBLE | BREAKING — reason.

## Production Risk

LOW | MEDIUM | HIGH — concrete reason.

## Rollback

FULLY_REVERSIBLE | REVERSIBLE_WITH_BACKUP | PARTIALLY_REVERSIBLE | NOT_REVERSIBLE — reason.

## Governance

Applicable restrictions and whether execution is allowed.

## Pre-Execution Checks

Required checks, or `None.`

## Required Actions

Actions required for safety, or `None.`

## Optional Improvements

Useful non-blocking improvements, or `None.`

## Execution Status

ANALYSIS_ONLY | READY_FOR_EXECUTION | REQUIRES_APPROVAL | BLOCKED_BY_GOVERNANCE | DO_NOT_EXECUTE

## Final Assessment

Concise conditions for safe execution.
```

Keep trivial, safe changes concise; deepen the report for PK/FK, destructive operations, large data migration, production changes, compatibility concerns, or legacy schemas.
