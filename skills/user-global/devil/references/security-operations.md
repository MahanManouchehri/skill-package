# Security and Operations Lens

Use this reference when trust boundaries, sensitive data, deployments, dependencies, availability, or recovery materially affect the proposal.

## Security

Start from assets, actors, data flows, and trust boundaries. Use STRIDE as a prompt for relevant threats—not an exhaustive checklist: spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege.

Inspect authentication, authorization (especially object/tenant scope), input handling, injection boundaries, secrets/credentials, default configuration, logging/audit data, supply-chain dependencies, rate limits, abuse cases, and data exposure. A security finding needs a credible path in the proposed system; label missing facts as unknown instead of implying an exploit exists.

## Operations and recovery

Challenge deployment ordering, configuration drift, feature flags, backward compatibility, rollback, backups, monitoring, logs/metrics/traces, alert ownership, and incident recovery. Ask how an operator detects the failure, narrows scope, restores correctness, and prevents repeated damage.

For production-impacting changes, distinguish the desired happy path from the recovery path after interruption, unknown completion, failed rollback, dependency outage, capacity exhaustion, or bad configuration. Recommend only the observability and controls that materially reduce a stated risk.

## Pre-mortem trigger

For Critical reviews, or Deep reviews with significant irreversibility, run a concise pre-mortem: imagine failure six months after adoption, identify plausible technical/data/operational/product/dependency causes, and name early warning signals plus an owner or guardrail where useful. Do not create a pre-mortem for a trivial decision.
