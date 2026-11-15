# Validation evidence — 3.1.1

Baseline: `v3.1.0` / `11d61b3e05afaf2749d7314d1a72d0c1d9ed3523`. Release date: 2026-11-16 (owner timezone). Local command timestamps use UTC. The package remains schema 1 with 26 personal skills, 16 managed archival entries and five system exclusions.

## Verified publication and installation

Release `v3.1.1` is published at `80ca761864da9134141df432224015390afe8ea6` with annotated tag object `cd2a33f7c977e752d3afec6a1ac1e31c36f170cf`. The [final commit run](https://github.com/MahanManouchehri/skill-package/actions/runs/43764630393) and [tag run](https://github.com/MahanManouchehri/skill-package/actions/runs/43765443386) are completed WINDOWS_CI_PASS on this exact SHA. [In-repository publication records](evals/evidence/v3.1.1/publication/README.md) include the remote receipt, final raw CI logs/markers, installed-tree/discovery observations and [Persian delivery report](evals/evidence/v3.1.1/publication/report.fa.md).

The release outcome is DONE_WITH_LIMITATIONS; its overall acceptance audit is PARTIAL because native coverage is incomplete. The owner installation outcome is NO_REINSTALL_NEEDED: all26 existing trees match the released manifest, with26 unique enabled metadata entries,23 in the Codex root and3 in the agents root. These are release-time observations, not new test/model/install runs during a documentation update. Later main documentation commits do not change the immutable release SHA or its recorded869-file aggregate.

## Local executed gates

| Check | Actual result | Evidence |
|---|---|---|
| Package transaction/portability tests | 57 executed/passed, no failures/skips | [log](evals/evidence/v3.1.1/local/package.txt) |
| Native runner helpers | 27 executed/passed; original 14 methods retained | [log](evals/evidence/v3.1.1/local/runner.txt) |
| Unchanged full UI discovery | 153 executed/passed; zero failures, errors or skips | [log](evals/evidence/v3.1.1/local/ui.txt) |
| Additional UI launcher regressions | 5 executed/passed | [log](evals/evidence/v3.1.1/local/ui-launcher.txt) |
| Default strict relevance | 90 cases; original frozen thresholds/fingerprints pass | [report](evals/evidence/v3.1.1/ui/final-licensed-relevance-report.json) |
| Offline catalog and search/path smoke | 11 catalog tests, 13 independent smoke checks pass | [summary](evals/evidence/v3.1.1/ui/ui-repair-summary.json) |
| Preservation | 625 immutable files checked; personal/managed payloads and old bank/evidence unchanged | [invariants](evals/evidence/v3.1.1/preservation.json) |
| Live installed payload/discovery | 26 matching trees, 26 unique enabled names; 23 Codex / 3 agents roots | [hashes](evals/evidence/v3.1.1/installed-check.json), [metadata](evals/evidence/v3.1.1/installed-discovery.json) |

The old UI discovery was 130 real passes plus two import-error placeholders. Authentic authoring implementations expose the previously unimportable 23 tests, so the repaired full count is 153. No runtime/test/fixture bytes or acceptance thresholds were changed. Tools are pinned to upstream `6ae86f61f520d6ca229d2f40e070410638c908c5`, licensed MIT, and remain outside installable payloads; see [provenance](UI_AUTHORING_PROVENANCE.md).

## Native execution and limits

The default Homebrew CLI `0.142.5` has an old bundled model catalog. The official app-bundled `/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex`, version `0.167.0-alpha.3.2`, lists `gpt-6.1-sol`; actual ChatGPT-authenticated smoke and read-only tool turns succeed. No model fallback, provider reconfiguration, default binary replacement or credential copying occurred. [Catalog summary](evals/evidence/v3.1.1/native/models-catalog-summary.json), [auth status](evals/evidence/v3.1.1/native/diagnosis/auth-status.json), [successful preflight](evals/evidence/v3.1.1/native/preflight-final/result.json).

The unchanged bank has **60 designed / 12 unique attempted / 10 completed / 2 usage-cap blocked / 48 unexecuted**. Independent raw review distinguishes eight satisfactory bounded routing plans from two fixture-source isolation failures (S07/S12), where a host `compatible-response` body was read. Its bytes match the fixture copy, but the source-path violation remains a failure. No forbidden operational workflow, secret access or production/provider effect was observed in the reviewed slice. These counts are not application acceptance or a 60-case pass rate.

Four earlier case attempts used an extra macOS seatbelt profile; nested sandbox application prevented tool reads. They remain in `native/initial-harness-attempts/`, excluded from successful routing counts. Five auxiliary smoke/tool probes are separate from bank cases. All native cases used the same explicit model/medium effort. The process was stopped on actual account `usage limit` errors, without automatic retry or model switching.

Native discovery showed exactly 26 enabled fixture copies after all external entries were disabled per invocation. Discovery isolation does not confine shell reads. After review the runner redirects ancestor skill-path preferences to project-local copies, flags recognized external skill-body reads, and checks post-turn fixture hashes. Unit/subprocess tests pass; **that final corrective harness revision has no new native behavioral verification after the account cap**. Dynamic/compound read methods require manual trace review. All full application behavior remains UNVERIFIED.

Primary auth/config/skill/plugin files were not manually edited or copied. An early outer profile protected cache writes but blocked nested sandboxing; later standard read-only CLI use succeeded. The primary model-cache hash changed during runtime activity; it was not manually rewritten, deleted or restored. Do not claim byte-preserved cache or an account entitlement repair.

## Windows evidence

Source review and 57 cross-platform package tests are green on macOS and in hosted Windows execution. Local PowerShell 5.1/7 are unavailable. The authorized `windows-latest` workflow exercises actual Windows locking/liveness, junctions/locked files, UTF-8/raw hashes, package/runner/UI suites and both PowerShell parsers/temp-only transactions. [Completed final-SHA hosted run](https://github.com/MahanManouchehri/skill-package/actions/runs/43764630393) is WINDOWS_CI_PASS on Windows Server 2025 / Python 3.12.10: 57 package, 27 runner, 153 UI, 5 launcher and 4 real filesystem tests pass, and both PowerShell 5.1/7 parse six scripts and pass full temp-profile transactions. [Snapshot-bound status](evals/evidence/v3.1.1/windows/ci-status.json) preserves the exact tested SHA, markers and all four earlier failures. The preserved ci-status file is an earlier successful candidate snapshot; the final published-SHA commit/tag confirmations and raw logs are in [publication evidence](evals/evidence/v3.1.1/publication/README.md). [Restrictions and safe commands](WINDOWS_COMPATIBILITY.md) distinguish the Python installer from the standalone PowerShell fixed-drive-only fallback.

## Historical routing and publication

The original 30 delegated observations remain 18 complete / 12 partial / 30 unexecuted in their historical ledger. The separate 12-case adjudication is A=0, B=7, C=5, D=0; no skill-policy patch is justified. [Review](evals/evidence/v3.1.1/routing-adjudication.md). It does not relabel the old results as 30/30 PASS.

Old `evals/evidence/*` records and all 60 owner prompts are immutable. The prior root report is retained byte-for-byte at [baseline validation](evals/evidence/v3.1.1/baseline-validation-v3.1.0.json). New evidence belongs under `evals/evidence/v3.1.1/`. Build/verification cover the entire distribution; aggregate hashes live in `package-integrity.json` to avoid self-reference. Final remote/tag provenance and the published-manifest installation binding are recorded in [publication evidence](evals/evidence/v3.1.1/publication/receipt.json). The later documentation-only source has a separately regenerated package-integrity file; its own SHA is not embedded in its contents. No live reinstall or new backup is needed for byte-identical personal payloads.
