# Reproducible skill evaluations

`cases.json` contains the owner's exact 60 scenarios. The bank and `MATRIX.md` describe expected behavior; neither is an execution result. This runner uses Python 3.10+ and Git for fixture preparation; it installs no frameworks, dependencies, services or models.

## Released results and source pin

The immutable v3.1.1 source is `80ca761864da9134141df432224015390afe8ea6`; [published records](evidence/v3.1.1/publication/README.md) contain final commit/tag Windows CI, the source-bound install receipt and independent native review. This guide describes runnable tools; it does not claim a new run happened when documentation changes.

Current native ledger:60 designed,12 unique attempts,10 completed,8 scoped plan PASS,2 source-isolation FAIL,2 usage-cap BLOCKED and48 unexecuted. All full-application acceptance remains UNVERIFIED. Historical delegated18-complete/12-partial records and separate12-case adjudication remain unchanged. Use fresh corrected fixtures for any future explicitly authorized model evaluation; the final harness has no post-cap native rerun.

## Prepare without a model call

Choose a **new dedicated directory outside this package**:

```sh
python3 evals/run.py prepare --output /absolute/path/to/new-eval-fixtures
# A smaller preparation still uses the unchanged source bank:
python3 evals/run.py prepare --output /absolute/path/to/new-selected-fixtures --cases S01 S05
python3 -m unittest discover -s evals -p test_runner.py -v
```

Preparation refuses existing destinations, package-contained paths, symlinks and sensitive filenames. Each case contains its original `prompt.txt`, a 26-entry `available_catalog.json`, independent copies under `.agents/skills`, synthetic application source, an `AGENTS.md` governance fixture and provenance. S37 requires owner deployment approval; S55 has malicious README prose; S56 requires private uploads. No credentials, account settings, system skills or plugin caches are copied. Payload file hashes, a deterministic snapshot digest, base HEAD, `source_dirty`, observed version and bank SHA are recorded. `source_sha` is a backwards-compatible alias for the base commit, not a claim that uncommitted changes were already published. The snapshot digest binds the evaluated working tree. Metadata extraction is for the synthetic catalog only; strict YAML validation belongs to the package verifier.

These are **READ_ONLY_ROUTING_PLAN** fixtures. Composer/Python/Next manifests identify synthetic stacks; they are not installed applications. Laravel/Django/Blade/Next sources, SQLite duplicates and provider contracts permit grounded inspection. The S14 historical URL is scenario context, with actual availability unverified; the runner starts no browser or server. Model planning over these fixtures does not verify application implementation, browser acceptance or production operations.

## Native discovery, explicit preflight and one model attempt

The native app-server `skills/list` call lists actual runtime metadata without starting a model:

```sh
python3 evals/run.py discovery --cwd /absolute/path/to/new-eval-fixtures/S01 --output /absolute/path/to/native-catalog.json
```

Preflight records version/help, requires the requested model in the runtime's supported `debug models --bundled` catalog, verifies the native enabled catalog, and attempts one tool-free marker turn. It never falls back. A bundled entry alone does not confirm account access. Choose a new output directory:

```sh
python3 evals/run.py preflight --cwd /absolute/path/to/new-eval-fixtures/S01 --output /absolute/path/to/new-preflight --model SUPPORTED_MODEL --codex /absolute/path/to/codex
```

After a successful `NATIVE_MODEL_CONFIRMED` preflight and a real read-only tool check, run a case:

```sh
python3 evals/run.py run --prepared /absolute/path/to/new-eval-fixtures --case S01 --model SUPPORTED_MODEL --codex /absolute/path/to/codex --reasoning medium --timeout 240
```

The runner makes **one attempt**, without model fallback, account/config repair or automatic retry. It validates the prepared payload/prompt, queries native discovery, disables **all external user/system/plugin skill entries** through invocation-only `skills.config` overrides, then queries native discovery again and refuses a model call unless exactly the fixture's 26 copies are enabled. Plugins/apps/remote-plugin services are disabled for this invocation. It never edits installed skills or user configuration. The old `disabled_overlays` helper remains available for compatibility; actual runs use the strict `isolated_overlays` path. The exact command uses `codex -a never exec --ignore-user-config --ephemeral --json --sandbox read-only --model ...`; authorization, the real runtime's instruction hierarchy and its existing authentication remain in force. The test model receives the original request within a read-only evaluation wrapper, without expected/forbidden skill names. `--reasoning` defaults explicitly to `medium`; the selected model is always explicit. Inspect `invocation.json` for the exact input and effective overlay list.

Evidence is written under a new `native-runs/<UTC timestamp>/<case>/`: native catalog, invocation/model/runtime/source snapshot, raw stdout JSONL, stderr and an independently labeled result. The app-server helper uses a portable queue/reader thread instead of selecting on Windows pipes. Its requests time out, cleanup avoids blocking on a descendant-held stdout, and actual subprocess tests cover buffered notifications and retained handles. Host-specific results remain separately labeled. The native CLI protocol may evolve: unknown or invalid events require manual inspection rather than a guessed PASS.

On 2026-11-13, this environment's Codex CLI `0.142.5` rejected the configured `gpt-6.1-sol`, default `gpt-5.5`, and listed `gpt-5.4` with HTTP 400 / `model_not_found`, including:

```text
The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account.
```

Those native probes are **UNVERIFIED**, not behavioral passes or skill failures. That is historical evidence for the old executable, not a permanent entitlement verdict. On 2026-11-15 the official app-bundled `0.167.0-alpha.3.2` lists `gpt-6.1-sol` and actual ChatGPT-authenticated model/tool turns succeed. The default Homebrew `0.142.5` was preserved. See `evidence/v3.1.1/` for the current preflight, intermediate harness failures, raw turns and separate reviewer verdicts. See the release validation report for current execution evidence. A genuinely fresh delegated-agent evaluation is a separate harness and must be labeled separately; it does not prove native CLI model support or automatic runtime discovery.

## Read results correctly

Every native case result has independent `STATIC_PASS`, `TOOL_TEST_PASS`, `LIVE_BEHAVIOR_PASS`, `UNVERIFIED` and `FAIL` fields. `null` means no pass was established.

- `STATIC_PASS` remains `null`; run the structural/package verifier separately.
- `TOOL_TEST_PASS` covers successful fixture/snapshot checks only, not application tests.
- Successful explicit `cat`/`sed`/`head`/`Get-Content` skill reads are extracted from completed command traces. Failed reads, printed path mentions and model self-declarations are recorded differently. Other valid read methods and compound commands need manual trace inspection; an aggregate shell exit cannot certify every earlier subcommand. Conditional-OR/background reads are deliberately not counted. A declaration of intent never proves a body read.
- A recognized forbidden read flags a routing failure for review. Determine whether it activated a workflow or merely inspected a contract before issuing the final case verdict. Skill reads alone never establish the full acceptance assertion.
- Native startup errors, missing completion/output, malformed JSON or a successful-looking final declaration leave behavior `UNVERIFIED`. No automatic positive behavioral PASS is emitted. A reviewer must assess the complete trace, authorization, forbidden actions, evidence and case-specific assertion; record that verdict with an evidence path.

Keep designed coverage, actual executed cases, routing-plan observations, native discovery and full application acceptance separate. Never turn file/string checks or simulated responses into live-model statistics. Preserve failed attempts when correcting and rerunning an affected case.

## v3.1.1 raw-review corrections

Current evidence records 12 unique native attempts: 10 completed, two usage-cap blocked, 48 bank cases unexecuted. Two completed cases read an identical host supporting-skill body and therefore fail strict fixture-source isolation; do not infer successful isolation from the enabled catalog alone. After raw review, new fixtures redirect ancestor/global skill-path preferences to the same named local copies, preserving policy/authority semantics. Recognized external skill-body reads now fail source isolation, and changed fixture files fail post-turn integrity. These corrections have helper coverage but no subsequent native model run after the quota stop. Old fixtures/traces remain bound to their original governance hashes; do not imply they used the corrected fixture text.

The standard Codex read-only sandbox restricts writes, not all filesystem reads. Invocation overlays are metadata selection controls, not an OS read jail. Review raw traces for dynamic/compound commands and any outside-fixture access before recording a scoped plan verdict. A host body matching the package hash does not excuse its source-path deviation. Every full application implementation/operational acceptance remains UNVERIFIED.
