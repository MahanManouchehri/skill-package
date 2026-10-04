# /steps Deep Workflow Reference

Load this reference only when the active task needs deeper orchestration: high engineering criticality, complex governance, repeated rework, worker conflicts, complex approval/owner gates, recovery after partial changes, or strict final traceability.

## 1. Detailed workflow states

Use state deliberately; verdict and state are different concepts.

Common non-terminal states:

- `RECEIVED`
- `GOVERNANCE_CHECK`
- `TASK_ANALYSIS`
- `ROADMAP_CREATED`
- `WORKER_ASSIGNED`
- `WORK_IN_PROGRESS`
- `WORKER_COMPLETED`
- `TEAM_LEAD_REVIEW`
- `WAITING_FOR_USER`
- `WAITING_FOR_OWNER`
- `PAUSED`
- `BLOCKED`
- `FINAL_AUDIT`

Terminal success:

- `DONE`
- `DONE_WITH_LIMITATIONS`

Terminal non-success:

- `NOT_DONE`
- `CANCELLED`
- `SUPERSEDED`

`BLOCKED` is normally resumable. `PAUSED` is an intentional stop without a blocker.

## 2. Task ledger and resume capsule

For larger work, maintain a compact in-session ledger:

- Goal
- Criticality / Workload
- Requirements (`R1...`)
- Approved Decisions (`D1...`)
- Effective Governance / authority map
- Current scope
- Roadmap and current phase
- Carry-forward notes
- Pending approvals / owner actions
- Known risks
- Evidence and stale reviews

Do not persist this into repository files unless explicitly requested and permitted.

At major gates or before a likely session boundary, provide a short resume capsule containing only:

- current step
- completed steps
- current requirements/decisions that matter
- pending gate
- next step

## 3. Scoped approval model

Every approval request should state what is included and, when ambiguity is plausible, what is not included.

Example:

- Approved: add model `X` with fields `A`, `B`.
- Not approved: migration execution, new unrelated table, destructive data transformation.

Approval becomes stale when the approved proposal changes materially. Re-open only the affected approval; do not re-ask unrelated decisions.

User workflow overrides may change execution depth, optional reviewers, or specialist choices when allowed by governance. Preserve assessed criticality as an evidence-based value; record a separate deeper execution strategy if requested.

## 4. Requirement/decision change control

When the user changes a requirement:

1. mark the old requirement/decision as updated or superseded;
2. determine impact on existing steps, decisions, approvals, implementations, tests, and reviews;
3. invalidate only affected artifacts/steps;
4. reuse unaffected work;
5. replan from the earliest necessary dependency.

Do not restart the whole workflow unless the change truly invalidates the whole design.

## 5. Worker result envelope

For meaningful phases, normalize the worker result conceptually into:

- `Status`: completed / blocked / needs decision
- `Findings`
- `Deliverable`
- `Evidence`
- `Risks`
- `Scope deviations`
- `New dependencies`
- `Recommended next action`

This is an internal review aid, not a requirement for literal JSON or verbose formatting.

## 6. Entry and exit criteria

Before assigning a phase, confirm prerequisites are satisfied. Do not send a worker an under-specified assignment if another prerequisite phase is actually required.

A phase is complete only if its exit criteria are satisfied.

Example `/db-impact` exit criteria may include:

- affected schema/data paths identified
- backward compatibility assessed
- migration/data risk described
- rollback/recovery reasoning provided where relevant
- governance/owner-only actions identified

## 7. Conflict resolution

When specialists disagree:

### Clear technical winner

If one recommendation clearly violates requirements/governance or has materially worse correctness/risk, reject it with reasoning and route rework to the responsible phase.

### Multiple valid options

Escalate to the user with:

- option A: pros / cons
- option B: pros / cons
- material consequences
- team-lead recommendation and reason

Do not manufacture certainty when both are valid.

## 8. Independent review integrity

For independent reviews, avoid feeding the reviewer persuasive summaries like "the plan is already correct." Provide factual context instead:

- requirements
- approved decisions
- applicable governance
- artifact/current snapshot
- relevant evidence

A review is valid only for the snapshot it inspected. If a later change affects the reviewed area, mark that review stale and refresh only the affected review scope.

## 9. Rework and recovery

When a modifying phase fails or is interrupted:

1. inspect current actual state;
2. identify what was already applied;
3. determine whether failure is implementation, plan, architecture, unknown-root-cause, governance, or requirement ambiguity;
4. route to the smallest responsible phase.

Typical recovery:

- implementation defect -> implementation
- plan defect -> `/full-plan`
- architecture defect -> `/architecture-review`
- unknown behavior -> `/root-cause`
- DB-impact misunderstanding -> `/db-impact`
- requirement ambiguity -> user decision

Do not retry from the original mental model if repository state has changed.

## 10. Rework loop guard

For the same issue, two automatic rework attempts are normally enough:

1. normal correction
2. targeted correction with explicit failed criterion

If still unresolved, stop repeating and change strategy. State why the repeated approach failed and what new information or specialist is needed.

## 11. Necessary incidental changes

Not every small out-of-file change is scope creep.

A necessary incidental change may be allowed without a new user gate when it is:

- directly required to satisfy the approved requirement
- small and reversible
- low-risk
- not a new public/data/security contract
- compatible with governance

Report it when technically meaningful.

Anything that adds a feature, new behavior, contract, subsystem, destructive change, significant refactor, or new risk is scope expansion and requires replan/possibly approval.

## 12. Database-sensitive workflow

When DB impact is real:

1. use `/db-impact` when it adds value;
2. present schema/data/migration/compatibility details proportionate to criticality;
3. request scoped approval where governance requires it;
4. perform only allowed source/model changes;
5. never infer permission to run migrations or mutate production data;
6. create `OWNER_ACTION_REQUIRED` for owner-only commands/actions;
7. after owner confirmation, re-read the relevant model/schema/artifacts before continuing.

Database involvement alone does not determine star rating; governance and criticality remain separate.

## 13. Test and evidence policy

Scale evidence with criticality.

Low criticality may need only focused diff/render/behavior verification.

Standard work should usually include targeted tests and affected-flow verification.

High/critical work may require multiple evidence types: targeted tests, regression evidence, independent review, rollback reasoning, permission/security checks, critical-path verification, and practical testing when applicable.

Never run destructive tests against an environment whose safety is unclear.

Evidence labels:

- `VERIFIED`: directly supported by inspectable evidence.
- `OWNER_CONFIRMED`: user performed/confirmed an owner-only action; do not mislabel it as independently verified unless you subsequently verify observable state.
- `UNVERIFIED`: could not be checked; explain why and its consequence.

## 14. Final status discipline

`DONE_WITH_LIMITATIONS` is allowed only when:

- core requirements are complete;
- missing verification is non-critical;
- the limitation is explicit;
- residual risk is understood and acceptable.

If a mandatory critical verification or owner action for the approved Definition of Done is incomplete, use `NOT_DONE` or `BLOCKED`.

## 15. Token/context discipline

For complex tasks, be deep where risk exists, not everywhere.

- Reuse prior repository discovery when still trustworthy.
- Give workers targeted context rather than full conversation history.
- Do not repeat requirement lists in every report; reference them internally and surface only relevant changes/conflicts.
- Use `LEAN`, `STANDARD`, or `DEEP` worker output depth.
- Load additional references only when the current workflow condition requires them.
- Prefer small targeted re-verification over full-task reruns.

## 16. Progress reporting

Do not simulate background workers or unsupported live telemetry. Report transitions:

- phase started
- meaningful finding
- phase completed
- review verdict
- roadmap changed
- user/owner gate
- final audit

For the user, preserve meaningful technical details such as affected files/modules, API/input/output/validation changes, schema impact, permissions, risks, test evidence, and why a phase was accepted or rejected. Filter repetitive raw worker prose.
