# Architecture and Data Lens

Use this reference for component boundaries, APIs, distributed workflows, schema changes, migrations, and data ownership.

## Architecture

Reconstruct responsibilities, data ownership, interfaces, consistency needs, and failure isolation. Check whether components are coupled for a real reason, whether state has one authoritative owner, and whether an API/event contract has versioning, ordering, idempotency, and compatibility requirements. Do not prescribe patterns such as microservices, CQRS, event sourcing, queues, repositories, or distributed locks without a concrete requirement.

For asynchronous or distributed behavior, inspect duplicate delivery, ordering, retry, poison messages, dead-letter or manual recovery, outbox/side-effect ordering when relevant, dependency failure, observability, and backpressure. State consistency and availability trade-offs in plain language rather than treating them as generic defects.

## Data and migrations

Inspect models, migrations, raw SQL, constraints, indexes, data access, reports/jobs/integrations, and old records where accessible. Challenge assumptions about existing data, nullability, uniqueness, deletion, historical meaning, ownership, retention, and PII.

For a consequential change, determine:

- whether old and new application versions can coexist;
- whether the change is additive, breaking, destructive, or lossy;
- whether a backfill, snapshot, verification, staged expand/contract path, or data restoration plan is needed;
- locking, table-size, index, query-performance, and rollback implications;
- which data cannot be reconstructed after rollback.

A down migration is not proof of data recovery. Do not claim production data is safe without evidence. Route detailed database blast-radius work to `db-impact`; Devil should challenge the resulting conclusion and cross-domain implications.

## Reversibility

Classify each material decision as `easily reversible`, `reversible with cost`, `difficult to reverse`, or `effectively irreversible`. Consider source data, external contracts, public commitments, deployed clients, vendor lock-in, compatibility windows, and restoration. Demand evidence proportional to irreversibility.
