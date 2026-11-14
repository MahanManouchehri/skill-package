# Reproducible skill evaluations

`cases.json` contains the owner's exact 60 scenarios. The bank and `MATRIX.md` describe expected behavior; neither is an execution result. This runner uses Python 3.10+ and Git for fixture preparation; it installs no frameworks, dependencies, services or models.

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

## Native discovery and one explicit model attempt

The native app-server `skills/list` call lists actual runtime metadata without starting a model:

```sh
python3 evals/run.py discovery --cwd /absolute/path/to/new-eval-fixtures/S01 --output /absolute/path/to/native-catalog.json
```

When the current account has a verified supported model and an actual turn is authorized:

```sh
python3 evals/run.py run --prepared /absolute/path/to/new-eval-fixtures --case S01 --model SUPPORTED_MODEL
```

The runner makes **one attempt**, without model fallback, account/config repair or automatic retry. It validates the prepared payload/prompt, queries native discovery, and disables conflicting external **user** entries for matching names through this invocation's `skills.config` override. It never edits those installed skills. The fixture's local copies remain available. The exact command uses `codex -a never exec --ignore-user-config --ephemeral --json --sandbox read-only --model ...`; authorization, the real runtime's instruction hierarchy and its existing authentication remain in force. The test model receives the original request within a read-only evaluation wrapper, without expected/forbidden skill names. Inspect `invocation.json` for the exact input and effective overlay list.

Evidence is written under a new `native-runs/<UTC timestamp>/<case>/`: native catalog, invocation/model/runtime/source snapshot, raw stdout JSONL, stderr and an independently labeled result. The app-server helper uses native stdio pipe selection, exercised on macOS; another host must verify its transport support. The native CLI protocol may evolve: unknown or invalid events require manual inspection rather than a guessed PASS.

On 2026-11-13, this environment's Codex CLI `0.142.5` rejected the configured `gpt-6.1-sol`, default `gpt-5.5`, and listed `gpt-5.4` with HTTP 400 / `model_not_found`, including:

```text
The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account.
```

Those native probes are **UNVERIFIED**, not behavioral passes or skill failures. No further model attempts are warranted in that environment without a supported account/model becoming available. See the release validation report for current execution evidence. A genuinely fresh delegated-agent evaluation is a separate harness and must be labeled separately; it does not prove native CLI model support or automatic runtime discovery.

## Read results correctly

Every native case result has independent `STATIC_PASS`, `TOOL_TEST_PASS`, `LIVE_BEHAVIOR_PASS`, `UNVERIFIED` and `FAIL` fields. `null` means no pass was established.

- `STATIC_PASS` remains `null`; run the structural/package verifier separately.
- `TOOL_TEST_PASS` covers successful fixture/snapshot checks only, not application tests.
- Successful explicit `cat`/`sed`/`head`/`Get-Content` skill reads are extracted from completed command traces. Failed reads, printed path mentions and model self-declarations are recorded differently. Other valid read methods may need manual trace inspection.
- A recognized forbidden read flags a routing failure for review. Determine whether it activated a workflow or merely inspected a contract before issuing the final case verdict. Skill reads alone never establish the full acceptance assertion.
- Native startup errors, missing completion/output, malformed JSON or a successful-looking final declaration leave behavior `UNVERIFIED`. No automatic positive behavioral PASS is emitted. A reviewer must assess the complete trace, authorization, forbidden actions, evidence and case-specific assertion; record that verdict with an evidence path.

Keep designed coverage, actual executed cases, routing-plan observations, native discovery and full application acceptance separate. Never turn file/string checks or simulated responses into live-model statistics. Preserve failed attempts when correcting and rerunning an affected case.
