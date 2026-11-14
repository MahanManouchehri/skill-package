---
name: technical-proposal-discovery
description: Produce a technical proposal or an evidence-backed competitor software comparison only on direct request. Distinguish proposal scope and deliverables from ordinary feature brainstorming; exclude commercial pricing, contracts and financial management.
---

# Technical Proposal and Product Research

Convert a requested brief into an actionable technical proposal, or compare real product evidence. Keep the two modes distinct and use only those requested.

## Activation and input

**Policy: EXPLICIT_ONLY.** A direct natural-language request for a technical proposal or competitor/product research, or a relevant invocation, triggers the workflow. Ordinary feature implementation, design options or “analyze my app idea” does not request market research or a proposal document; `multiple-pov` can support general product/engineering discovery.

Establish the audience, brief/problem, existing product/stack, constraints, desired output and available sources. Read applicable project documentation rules before creating files. Surface only missing facts that materially affect the proposal; use labeled assumptions for reasonable reversible details.

## TECHNICAL_PROPOSAL

1. Restate the concrete problem, actors/workflows, current constraints and desired outcome from the supplied brief and inspected artifacts. Separate validated facts, assumptions and decisions needing the owner.
2. Define included scope, non-goals, deliverables and observable acceptance. Cover relevant API/UI/jobs/data/integration work without forcing a framework or new infrastructure. Keep the project's chosen stack unless a real requirement makes a change necessary.
3. Explain the proposed technical approach, boundaries, dependencies, alternatives with material consequences, implementation order and verification. Avoid ceremonial options when one straightforward solution fits.
4. Identify compatibility, permissions, data/integration risks, deployment ownership and operational assumptions. Distinguish application code from server administration and production actions. Note maintenance, documentation and handoff needs only to the extent the proposal requires.
5. Produce a decision-ready technical artifact with open questions and acceptance criteria. An implementation outline is not permission to build, buy services, deploy or contact anyone.

Exclude sales prices, commercial time/cost commitments, legal contracts and financial management. A technical dependency/order estimate may be qualitative and conditional; do not invent customer budgets, commitments or business data.

## COMPETITOR_RESEARCH

1. Identify the products/sites and comparison question. Use genuinely accessible current primary sources where possible: product documentation, public pages, observed UI and official technical information. Record access/publication date and URLs near claims. Respect available access; do not claim access to private dashboards or bypass controls.
2. Compare evidence-supported software features, user flows, UX/accessibility, platform/integration constraints and relevant design/technical trade-offs. Distinguish “not observed” from “not supported”; an inaccessible page is an evidence gap.
3. Label direct observation, source claim and inference separately. Resolve conflicting/stale sources or preserve the uncertainty. Do not invent usage, performance, revenue, internal architecture or security properties from appearance.
4. Map useful findings to the proposed product's constraints instead of copying a competitor wholesale. Use a compact comparison table when it makes evidence and gaps easier to assess; cite exact supporting sources.

If current source access is unavailable, deliver the researched subset and a clearly unverified comparison plan. Do not present remembered or fabricated browsing as current verification.

## Deliverable and boundaries

Provide the requested proposal/comparison with provenance, assumptions, concrete deliverables/recommendations, risks, acceptance and unresolved decisions. Use `VERIFIED`, `OWNER_CONFIRMED` and `UNVERIFIED` accurately. Acceptance requires actionable scope or a reliable evidence-backed comparison, without fictional facts or commercial commitments.

`full-plan` can refine an approved feature contract; `architecture-review` can review a concrete design; `hand-off` owns requested developer takeover documentation. Do not auto-start release, backup, load tests, full security audits, WebSocket/SSE, 3D or demos because a proposal mentions them as possibilities. No publication, messaging or external account changes without scoped authorization.
