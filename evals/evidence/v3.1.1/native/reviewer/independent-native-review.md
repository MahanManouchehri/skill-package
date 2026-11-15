# Independent native evidence review

Reviewed slice: **READ_ONLY_ROUTING_PLAN**. **8 scoped plan PASS, 2 strict fixture-source isolation FAIL, 2 usage-cap BLOCKED/UNVERIFIED.** Application acceptance remains **UNVERIFIED for all 60 cases**.

Current batches contain 12 unique attempts: first30 has 9 (8 completed, S21 cap); remaining30 has 3 (2 completed, S04 cap). 48 cases are unexecuted. Four earlier native attempts for S01/S05/S06/S07 remain preserved as invalid nested-seatbelt harness attempts; they are not additional unique cases or passes. Smokes are separate.

The saved runtime is app CLI **0.167.0-alpha.3.2**, **gpt-6.1-sol**, effort **medium**, with existing native **ChatGPT** authentication (`../auth-status.json`: app `login status`, exit 0). The recorded Brew CLI is 0.142.5; the case wrapper uses the app binary without replacing the default. No skill change is credited with granting account/model entitlement.

The original 60-case bank matches `git show v3.1.0:evals/cases.json` byte-for-byte: SHA256 `701e40e161d8f76848b04618857d46ea8f52b6f456eb7be82fa87944c7ee1706`. Each attempted prompt matches its source case. Every saved effective catalog enables exactly 26 unique fixture-local copies with zero discovery errors; all 12 payload trees match preparation hashes. The evaluated payload reports version 3.1.0, dirty source at base `11d61b3e05afaf2749d7314d1a72d0c1d9ed3523`, snapshot `485af03ae334b09f1d8646fff62c4af47b1373541a4c14459d09b9c550c82a97`; this is not a claim about later release changes.

All 12 invocations request approval `never`, sandbox `read-only`, `--ignore-user-config`, `--ephemeral`, and disabled plugins/apps/remote-plugin services. The wrapper permits reading only the fixture and its local skills. A read-only sandbox permits host reads; native discovery isolation is not a fixture-only filesystem boundary.

## Case verdicts

| Case | Reviewer verdict | Expected body reads absent after manual review | Assertion and evidence |
|---|---|---|---|
| S01 | PASS | none | Minimal color-change plan identifies the Blade button and CSS, leaves target color open, and avoids the forbidden heavy workflows. No application success is claimed. `fixtures/native-runs/20261115T155433506196Z/S01/stdout.jsonl:15` |
| S02 | PASS | none | The plan identifies the exact extra Persian character and proposes a one-character correction without a heavy workflow. `fixtures/native-runs/20261115T155747540737Z/S02/stdout.jsonl:13` |
| S03 | PASS | test-engineering | Internal endpoint plan preserves owner scoping, proposes relevant negative/regression tests, and adds no provider workflow. `fixtures/native-runs/20261115T155747542674Z/S03/stdout.jsonl:27` |
| S04 | BLOCKED | none | Usage cap interrupts the turn after four completed shell commands; there is no final plan to assess. `fixtures/native-runs/20261115T155831763032Z/S04/stdout.jsonl:12`, `fixtures/native-runs/20261115T155831763032Z/S04/stdout.jsonl:13` |
| S05 | PASS | test-engineering | The payment plan covers stable idempotency, unknown timeout outcome, status lookup/reconciliation and fake tests; no real payment is attempted. `fixtures/native-runs/20261115T155433511015Z/S05/stdout.jsonl:15` |
| S06 | PASS | none | The webhook plan covers durable deduplication, concurrent uniqueness, raw-byte HMAC/timestamp, version ordering and ACK after commit. `fixtures/native-runs/20261115T155519634233Z/S06/stdout.jsonl:21` |
| S07 | FAIL | none | Routing content satisfies the bounded 429/retry assertion, but a successful host skill-body read violates the fixture-only source boundary. `fixtures/native-runs/20261115T155541868312Z/S07/stdout.jsonl:27` |
| S09 | PASS | none | Internal CRUD plan explicitly rejects external integration despite a provider document being present. `fixtures/native-runs/20261115T155640280299Z/S09/stdout.jsonl:17` |
| S12 | FAIL | none | Object-level authorization and negative-test planning satisfy the content assertion, but a successful host supporting-skill body read violates source isolation. `fixtures/native-runs/20261115T155649953483Z/S12/stdout.jsonl:15` |
| S16 | PASS | test-engineering | The route is targeted to private-file authorization, honestly reports absent file/storage code, and proposes positive/negative access checks. `fixtures/native-runs/20261115T155753689266Z/S16/stdout.jsonl:13` |
| S17 | PASS | none | An explicitly requested FULL_AUDIT is bounded to authentication and related authorization, with missing subsystem code and runtime limits made clear. `fixtures/native-runs/20261115T155755108227Z/S17/stdout.jsonl:15` |
| S21 | BLOCKED | db-impact, regression-check, steps | Usage cap prevents any tool command or final answer. `fixtures/native-runs/20261115T155847049966Z/S21/stdout.jsonl:3`, `fixtures/native-runs/20261115T155847049966Z/S21/stdout.jsonl:4` |

PASS means that the inspected plan and trace satisfy this read-only slice; it never means an application fix or test passed. S03/S05/S16 explicitly defer test-engineering to implementation and supply relevant test criteria. S17 appropriately uses the directly requested security specialist. No expected-set omission was converted automatically into a failure.

## Material findings

- **S07 and S12 cross the source boundary.** S07 raw stdout line11 and S12 line7 successfully read `/Users/mahan/.agents/skills/compatible-response/SKILL.md`. The recorded host body is exactly 3235 bytes and has SHA256 `7bfefcacdb7179b1ebd2379bfe62d45f8336ff8f0c8ed6c7ffd3d08e28b82183`, matching the fixture payload. S07 later reads the local copy at line17. S12 line7 exactly equals the expected concatenation of compatible-response, steps and natural-persian-writing. Identical content does not satisfy a fixture-only source rule. These are strict isolation failures; no forbidden workflow, secret access or provider traffic is established.

- **S12 parser output undercounts real reads.** Its reported set is regression-check/test-engineering. Raw line7 returns complete steps/natural-persian-writing plus the host compatible-response body; line11 returns root-cause/security-assurance/test-engineering/regression-check/skill-evals. Six body names are omitted by the command recognizer. The recognizer also lacks `nl`; the current numbered reads are application/governance sources, not extra hidden skill bodies. The JSON records all 68 commands, exact raw line pointers and complete returned bodies separately from self-declarations.

- **No application tests ran.** `test -f` is a shell existence check. No test-runner, application mutation, dependency install, migration, service start, production scan, provider call, deploy or load command appears among the 68 completed shell commands. S01 git status emits denied temporary xcrun-cache warnings; the final answer does not claim a test passed. No final plan can prove future execution or persistence.

- **Cap cases cannot pass.** S04 stops at raw lines12-13 after four reads; S21 stops at lines3-4 before any tool command. Both lack final answers and remain BLOCKED/UNVERIFIED.

- **Evaluation context matters.** Explicit skill-evals reads respond to the evaluation wrapper; they do not establish an ordinary-application auto-routing defect. These native conditions differ from historical delegated plans and older Brew failures, so before/after causation from skill edits is unproven. Later runner fixes have no new native behavioral evidence in this review.

## Smokes and evidence bounds

`preflight-final/stdout.jsonl:3-4` returns NATIVE_SMOKE_OK and completes with no tools, confirming a true model turn. `tool-smoke.stdout.jsonl:6` records head exit 255 (HTTP HEAD utility); line8 records successful /bin/cat README.md, line9 discloses the failure and line10 completes. This proves a fixture shell read and recovery, not an application test. The tool smoke warns about under-development skip_host_skill_discovery; its mutable wrapper mtime postdates its invocation. Use the separately saved final-preflight/case catalogs for discovery assertions. Neither smoke increases case coverage.

The companion JSON preserves each original prompt/assertion, expected and forbidden sets, parsed and manually verified reads, external path evidence, actual commands, self-declarations/final plan, catalog/invocation/raw hashes, caps and scoped verdicts. All source reads and final answers were inspected; skill-body text was matched to the immutable fixture payload rather than inferred from a skill-name mention.

No source, runner, skills, original bank, older evidence, auth/config or installed-skill files were changed by this reviewer. No model calls, global writes, commit or push were performed.
