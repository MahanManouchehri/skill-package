---
name: integration-reliability
description: Design, implement or diagnose reliable third-party API and webhook integrations, including timeouts, retries, 429s, duplicates and uncertain external effects. Use for a real provider dependency, not internal CRUD or an ordinary local REST endpoint.
---

# Integration Reliability

Make external interactions recoverable without duplicating effects or inventing provider guarantees. A skill provides instructions; it does not provision a queue, start a worker or authorize a payment.

## Activation and input

**Policy: CONTEXTUAL_AUTO.** Use when the requested implementation or diagnosis actually crosses a third-party boundary: payments, SMS, supplier APIs, incoming/outgoing webhooks or comparable external effects. Do not activate for a static page, internal API or local business method without that dependency.

Identify the provider, operation and direction, relevant source/configuration, documented contract/version, observed failure and permitted environment. Inspect existing adapters, state transitions, tests and applicable `AGENTS.md`. Reuse supplied contracts; verify changeable provider semantics from available authoritative documentation. Missing retry/idempotency guarantees remain unknown, not assumed.

Choose the bounded mode the request needs:

- **DESIGN/IMPLEMENT:** specify the external contract and failure handling, then modify only authorized code.
- **DIAGNOSE:** reproduce from sanitized logs, fixtures or safe sandbox responses before changing policy.
- **REVIEW:** assess the supplied integration without implementing an unrelated redesign.

## Method

1. Trace request creation through provider response, persistence and downstream effects. Separate webhook **sender** delivery rules from **consumer** acceptance/processing rules. Locate authentication, signature verification, secret handling and trust boundaries.
2. Build a compact failure matrix for the actual operation: success; validation/auth failure; 429; transient server/network failure; timeout before/after a possible effect; duplicate/replayed/out-of-order event; partial local/external failure. Mark a branch N/A only with a reason.
3. Define time budgets across connection/read/total operation and existing retries. Classify retryable errors from the provider contract. Honor documented `Retry-After` and quotas, use bounded attempts/backoff/jitter when justified, and avoid nested retry multiplication. A timeout does not prove that an operation failed.
4. For side effects, identify the provider's idempotency facility, key scope/lifetime and stable business operation identity. Reuse the same key for a retry of the same operation, bind it to the intended payload, and prevent concurrent duplicate processing with appropriate durable uniqueness/atomicity. Never blindly retry a non-idempotent payment/message whose outcome is unknown.
5. Model `pending`/`confirmed`/`failed`/`unknown` or the project's equivalent states. Explain when a provider lookup, reconciliation or owner action resolves an unknown outcome. Distinguish the local transaction boundary from the external effect; do not claim an atomic distributed transaction without evidence.
6. For incoming events, verify authenticity using the provider's actual signature/raw-body/timestamp rules, durable event identity, replay window and acknowledgement semantics. Define duplicate, stale and conflicting-event behavior. Use sequence/version information when available; otherwise reconcile current authoritative state instead of trusting arrival order. Do not allow a late event to silently reverse a terminal business state.
7. Choose the smallest justified recovery mechanism: existing job infrastructure, durable inbox/outbox, reconciliation task or explicit manual recovery. Explain atomic persistence/acknowledgement and crash recovery where relevant. Implementing job code does not authorize installing cron, starting workers or modifying a server.
8. Add correlation IDs and safe diagnostics for attempt, event identity, latency and outcome without credentials or sensitive payloads. Test failure branches with the project's fakes, recorded sanitized contracts or an authorized provider sandbox; assert durable effects and absence of duplicates.

## Evidence and deliverable

Return the relevant source/provider contract, failure matrix, timeout/retry rules, idempotency and state/reconciliation strategy, changed code/tests, executed commands/results and unresolved provider questions. Distinguish **current** behavior from **proposed** behavior. Label observations `VERIFIED`, owner attestations `OWNER_CONFIRMED`, and unavailable runtime/provider checks `UNVERIFIED`.

Acceptance requires 429, duplicate delivery, timeout-after-effect, ordering and partial failure to be addressed or explicitly N/A/unknown. Do not claim provider availability, exactly-once delivery or an SLA that was not established.

## Authority and boundaries

- Code changes and safe isolated tests follow existing task authorization. Real payment, SMS/email delivery, third-party writes and production retries require their own scoped authority; use fakes/sandbox by default and stop before an unauthorized external effect.
- If the contract cannot establish a safe retry, leave that operation blocked/unknown and propose reconciliation; do not guess to obtain a green result.
- `full-plan` may own the feature contract; `architecture-review` a concrete component-boundary decision; `test-engineering` test implementation; `security-assurance` a material security delta. Use them only when available and needed. This skill owns external failure semantics, not full security audits, release work or load testing.
