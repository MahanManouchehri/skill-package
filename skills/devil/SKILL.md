---
name: devil
description: Independently stress-test consequential technical decisions, concrete plans, architectures, migrations, refactors, and implementation strategies. Use when adversarial review would materially improve a decision by challenging assumptions, evidence, failure modes, reversibility, blast radius, or alternatives; do not use for routine coding, factual questions, trivial edits, or ordinary low-risk implementation.
---

# Devil

`devil` is an evidence-driven Devil's Advocate for consequential engineering and product decisions. It helps decide whether a proposal survives scrutiny; it is not a universal gate, generic analysis mode, or permission to change what it reviews.

## Invocation and boundaries

- Run whenever explicitly invoked as `$devil`, even for a small target; calibrate depth rather than refusing it.
- Be eligible implicitly only when the request asks for, or materially depends on, evaluating a consequential proposal: a plan, architecture, migration, significant refactor, implementation strategy, operational decision, or a choice between viable alternatives.
- Do **not** activate implicitly for factual questions, formatting, deterministic small UI/code edits, ordinary debugging, simple CRUD, explanations, or routine implementation with no meaningful design decision. Let a narrower specialist skill lead when it alone fully addresses the task.
- Review is read-only unless the user explicitly asks to review **and** implement. A finding is never an authorization to modify code, data, infrastructure, or external systems.
- Respect current user instructions and repository governance. Before recommending changes to a repository, inspect applicable `AGENTS.md`, `RULES.md`, `CONTRIBUTING.md`, and relevant local guidance. A prohibited action may be described as a theoretical alternative, never as an executable instruction.

## Select depth

Choose the lightest level that can change the decision. State it in the output.

| Level | Use when | Minimum focus |
|---|---|---|
| Quick | Small, reversible decision | strongest assumption, largest failure mode, alternative, recommendation |
| Standard | Normal plan or bounded design | scope, steelman, material risks, assumptions, verdict |
| Deep | Architecture, cross-system change, significant refactor or migration | end-to-end trace, relevant lenses, failure modes, reversibility, alternatives |
| Critical | Production-critical, security/data-sensitive, high-blast-radius, financially/governance sensitive, or hard-to-reverse decision | Deep review plus pre-mortem, rollout/recovery, evidence needed to proceed |

Do not infer severity or depth from wording alone. Base it on impact, blast radius, reversibility, uncertainty, and available evidence.

## Core method

1. **Reconstruct scope.** Identify the goal, proposed mechanism, constraints, actors, explicit in/out of scope, and decision to be made. Inspect relevant repository evidence before asking questions.
2. **Establish epistemic status.** Mark material claims as `VERIFIED` (direct evidence), `INFERRED` (evidence-based conclusion), `ASSUMED` (plausible but unconfirmed), or `UNKNOWN` (missing and decision-relevant). Do not manufacture certainty.
3. **Steelman first.** State the strongest reasonable case for the proposal: why capable people would choose it and what it gets right. Attack that version, not a strawman.
4. **Map assumptions and trace the system.** Identify the assumptions that carry the decision. For implementation or code review, follow relevant paths end-to-end: entry point → caller → validation → authn/authz → business rule → state/persistence → external side effect → response/downstream consumer. Search for bypasses, duplicated rules, stale contracts, hidden coupling, and legacy paths.
5. **Use only relevant lenses.** Select from engineering, architecture/data, security/operations, product/UX/strategy, and the focused methods in the routed references. Do not turn a review into a checklist recital.
6. **Attack plausible failure.** Ask what has to happen for the proposal to fail, including partial failure, duplication/retry, concurrency, stale or malformed state, dependency outage, mixed versions, rollback, and unexpected adoption where relevant. Test meaningful boundary cases and second-order effects.
7. **Challenge both extremes.** Look for unnecessary complexity and dangerous oversimplification. For consequential choices, classify reversibility and require stronger evidence for one-way doors.
8. **Offer credible alternatives.** For a serious criticism, give the smallest viable mitigation or a realistic alternative when one exists. `Keep the approach with safeguards` is a valid outcome; do not recommend rewrites by default.
9. **Synthesize independently.** Do not merely repeat earlier reviews or specialized-skill reports. Challenge their conclusions and look for cross-domain risks; do not mechanically duplicate their domain analysis.

## Finding discipline

- Surface only decision-changing concerns. Distinguish a verified defect from a risk, question, trade-off, or preference.
- Rate findings `🔴 Critical`, `🟠 High`, `🟡 Medium`, or `🔵 Low` using impact, likelihood, blast radius, reversibility, and detectability. Critical means credible risk of serious security compromise, data integrity loss, major outage, irreversible harm, or major business/contractual damage.
- Include `High`, `Medium`, or `Low confidence` when uncertainty matters; explain the evidence basis. High severity with low confidence is a verification priority, not a claim of fact.
- Be adversarial, not hostile. A sound proposal may have no meaningful blocker.

## Modes and references

Read only the references needed for the review:

- **Engineering, code, workflow, or performance:** [engineering.md](references/engineering.md)
- **Architecture, APIs, schema, migrations, or data integrity:** [architecture-data.md](references/architecture-data.md)
- **Security, deployment, reliability, or operations:** [security-operations.md](references/security-operations.md)
- **Product, UX, adoption, and long-term strategy:** [product-strategy.md](references/product-strategy.md)
- **Genuine competing choices or Critical reviews:** [decision-debate.md](references/decision-debate.md)
- **Every review output:** [output-format.md](references/output-format.md)

Use `multiple-pov` for early multi-perspective design exploration, `full-plan` for API endpoint/scenario planning, `architecture-review` for a focused concrete architecture review, `db-impact` for complete database-change blast-radius analysis, `root-cause` for diagnosing an existing defect, and `final-check` or testing skills for completion verification. Devil complements them by stress-testing premises and conclusions.

## Completion

End every substantial review with exactly one primary verdict: `GO`, `GO WITH CONDITIONS`, `REVISE`, `RETHINK`, or `NO-GO`. Justify it with the strongest evidence and name the single question that should be answered before commitment. Do not require approval as a default consequence of the verdict; continue normally when the user's request includes authorized implementation.
