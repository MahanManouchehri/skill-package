# Independent v3.1.1 pre-release review

Reviewed source: `/Users/mahan/Desktop/Web/skill-package`, baseline `11d61b3e05afaf2749d7314d1a72d0c1d9ed3523`, candidate through `83aea6a` (`fix: preserve normalized Windows documentation references`). Review is read-only apart from this external report. No native/model invocation, installation, auth/private-file access, source edit, commit or push was performed by this reviewer.

**Code-review verdict: no additional actionable blocker found in the reviewed changes.** Publication is still conditional on the owner's final Windows CI assessment, refreshed distribution integrity/evidence and remote/tag verification. This report is not a release or full behavioral certificate.

## Code and integration

- **UI restoration:** authentic implementations remain outside the 26 installable skill trees. I rehashed the four restored upstream sources and MIT notice against their recorded SHA-256 and Git blob IDs; all five match. The launcher hash also matches its provenance document. `scripts/evaluate-relevance.py:21-24` refuses replaced vendor source; `:41-77` copies complete declared inputs and invokes the pristine evaluator in an ephemeral canonical layout. Existing runtime/data/test/threshold files are unchanged. `tests/test_ui_authoring.py:70-115` checks the default 90-case strict run and rejects changed runtime bytes, CRLF, grading helper and vendor source. I found no mocked oracle, lowered acceptance threshold or test removal/skip.
- **Windows filesystem boundaries:** `scripts/package_tools.py:59-102` keeps native spelling checks separate from link/reparse checks and canonical overlap decisions. Personal/backup roots receive canonical Windows checks (`:518-553`); catalog case collisions and unrelated reparse entries receive explicit handling. `:882-908` uses read-only process handles instead of a Windows signal probe. Read-only attribute changes are restricted to validated transaction scratch (`:708-722`), retaining backup attributes and existing journal/rollback checks.
- **Windows navigation correction:** the added exemption for literal `.`/`..` in `ordinary_windows_path` is appropriate. Actual Markdown targets are normalized, checked for links and bounded to the declared snapshot (`scripts/package_tools.py:234-251`); manifest `safe_relative` remains strict about traversal. Literal trailing dots/spaces and short-name aliases remain refused. No security regression found in this delta.
- **Standalone PowerShell:** `scripts/common.ps1:41-82` establishes accepted local fixed-volume identities and refuses unsupported aliases before install. `scripts/install.ps1:11-21,58-62` checks package/destination/backup/staging disjointness. Documentation correctly distinguishes its caught-error recovery from Python's durable journal and states its fixed-drive-only restriction.
- **Native runner:** `evals/run.py:250-279` verifies exactly the local fixture catalog before a turn. `:351-359` never awards automatic positive behavioral PASS; `:425-475` records external recognized skill reads and checks post-turn fixture integrity. `:187-237` bounds discovery and avoids waiting indefinitely on descendant-held stdout. Shell-parser limits are disclosed, so the parser is not presented as a complete filesystem-confinement proof.
- **Windows workflow:** `.github/workflows/windows-validation.yml:25-59` confines test state to runner temp, pins official actions, runs package/runner/UI suites plus actual Windows and separate PowerShell 5.1/7 drivers, and grants only `contents: read`. Source exists for real Windows evidence; workflow presence alone is not reported as a pass.

## Evidence and acceptance coverage

| Requirement | Review result |
|---|---|
| Native availability | Saved final smoke has `NATIVE_MODEL_CONFIRMED`, exit 0, completed exact tool-free marker, explicit `gpt-6.1-sol`/medium. No entitlement repair is claimed. |
| Actual bank coverage | Independently recounted raw files: 12 unique attempts, 10 completions, two usage-cap stops, 68 completed shell commands. Every saved effective catalog has 26 unique enabled names. The published ledger's eight bounded-plan PASS, two source-isolation FAIL and 48 unexecuted cases is consistent. |
| Isolation failures and correction | S07/S12 successful host supporting-skill reads remain explicit failures despite identical content. Corrected harness unit coverage is distinguished from the absent post-cap native rerun. No full application acceptance is claimed. |
| Full UI suite | Saved exact discovery log contains 153 actual passes and no failure/error/skip; the former two import placeholders exposed 23 real tests. Five launcher tests and the frozen 90-case gate are separately evidenced. |
| Windows checks | Fresh local package log now contains 57 passes. Actual Windows run 2 failed package verification on navigation spelling; source correction and regression were reviewed above. Windows CI success/PowerShell runtime success remain pending at this report. |
| Owner bank/history preservation | Independently compared 624 selected baseline-tracked files under personal/managed/historical evidence plus cases/MATRIX: no byte changes. The package's broader 625-file preservation result is separately retained. No policy/skill-body change or expected-case rewrite was introduced. |
| Historical 12 partial cases | Separate A=0/B=7/C=5/D=0 adjudication includes case-specific source and plan evidence. It does not overwrite the historical 18 complete/12 partial ledger or award new runtime passes. |
| Installed payload | Repository evidence separates 26 matching installed trees/unique enabled names from actual exercised workflows, and identifies 23 Codex/three agents roots. Unchanged installable payload supports `NO_REINSTALL_NEEDED`; final published-SHA binding belongs to the owner's final check. |

Fresh saved logs inspected: package 57, runner 27, full UI 153, launcher five. `git diff --check` passed at review. I did not redundantly rerun those suites or run the Windows drivers on macOS.

## Remaining publication conditions

1. Inspect the actual post-fix Windows CI result. Any reproducible local code defect remains a code gate; unavailable runtime evidence must retain its specific limitation.
2. Refresh CI status, count-bearing documentation, manifests/integrity after the final evidence edit; verify the final candidate rather than this moving working tree. At review, `windows/ci-second-attempt.json` was being updated and `ci-status.json` still said awaiting hosted results.
3. Complete normal remote commit/tag-target verification and the published-payload installation binding before reporting release completion.

With those conditions met, the remaining native quota and unexecuted full application cases support only the explicitly bounded `DONE_WITH_LIMITATIONS` report, not an unqualified full-routing/application certificate.

## Focused Windows teardown/workflow delta review

Reviewed the subsequent uncommitted changes to `tests/test_package_tools.py:71-88,107-121` and `.github/workflows/windows-validation.yml:42-67`. **No actionable issue found in this delta.**

- `remove_fixture_tree` is called only for the two resolved roots created by `mkdtemp` with the `skill-tools-fixture-` and `skill-tools-test-` prefixes. Its recovery callback requires Windows, `PermissionError`, an unlink/remove operation, a contained regular file, no reparse attribute and a read-only mode before changing attributes and retrying once. Other errors remain visible. It does not broaden production installer cleanup, remove/skip assertions, or use `ignore_errors`.
- Each independent workflow suite uses an explicit cancellation status function plus successful `steps.verify.outcome`. This permits sibling gates after a test failure while retaining package verification as the prerequisite for fixture execution. No `continue-on-error` was added, so a failing step continues to fail the job. A canceled run does not start further suites.
- The owner reports CI run 3 passed package verification and reached all 57 assertions but failed during teardown while deleting a read-only Git pack index. That is still a failed test-suite execution, not a suite PASS. This delta addresses the reported teardown path; its new Windows behavior has not been independently executed by this reviewer. The fresh local 57-test rerun and hosted Windows rerun were still pending at this focused review. The earlier successful local log does not establish the new cleanup branch on Windows.

No additional test, native/model invocation or source mutation was performed for this focused review.
