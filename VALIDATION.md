# Validation evidence —3.1.0

Observed 2026-11-14T04:22:28.230382+00:00 on macOS26.2 / Python3.14.2 / PyYAML6.0.3; Codex CLI0.142.5.

## Current structural and executed checks

-26/26 personal skills pass strict YAML/name/resource checks and the current bundled quick validator. All16 original names/resources remain;10 new specialists are added. The build verifies exact manifest/files/tree hashes, full distribution coverage, safe paths/references and common secret patterns.
-44/44 Python package-tool tests pass: clean install, collision refusal, exact backups/permissions, partial failure, actual subprocess crash/recovery, idempotence, multi-root duplicate removal/rollback, journal/path/symlink guards, tamper/omission and unrelated/system preservation.
-14/14 runner helper tests pass: actual fixture preparation, immutable payloads/prompts, path guards, real-read vs self-declaration and unavailable/malformed trace handling.
-130 preserved UI runtime/data tests pass;12 domains/22 stacks/reasoning validation and actual absolute-path UX/Laravel searches pass. Full132-module discovery has two pre-existing import errors because refresh-google-fonts.py, refresh-icon-catalog.py and evaluate-relevance.py are upstream authoring helpers absent from this payload. Tests/assertions were not weakened.
-An actual in-memory SQLite fixture identifies duplicate phones, rejects an unsafe unique index and preserves both rows. It is not MySQL or production evidence.

Commands executed (with an external Python environment containing PyYAML):

```sh
python -B scripts/package_tools.py build --package-root /absolute/path/to/skill-package
python -B scripts/package_tools.py verify --package-root /absolute/path/to/skill-package
python -B -m unittest discover -s tests -p test_package_tools.py -v
python -B -m unittest discover -s evals -p test_runner.py -v
```

Logs, exact helper commands/times/code hashes and the complete case table are under [evals/evidence](evals/evidence/README.md). The final distribution aggregate is in package-integrity.json; it is not embedded here to avoid a checksum cycle.

## Behavioral observations

All60 original owner cases are unchanged and prepared. Thirty fresh delegated agents received candidate metadata, source and governance without expected answers. Their actual source investigation/plan records were reviewed; candidate body hashes match the same final personal payload snapshot. No forbidden workflow or critical safety violation was observed in that bounded slice.
-Observed cases: S01, S05, S06, S07, S09, S12, S16, S17, S21, S23, S26, S27, S28, S29, S30, S34, S35, S37, S38, S40, S43, S46, S47, S49, S51, S53, S54, S55, S59, S60.
-Expected read sets: 18 MATCH; 12 PARTIAL/UNVERIFIED. A missing expected read is disclosed, not converted into a pass.
-The model sometimes selects a directly relevant specialist without steps. Installation provides model-driven discovery, not guaranteed interception. For a mandatory coordinator, an appropriate project rule must explicitly route it; no global AGENTS.md is edited.
-Every full application case remains UNVERIFIED. Planning does not prove code changes, tests, browser actions, provider effects or operational deployment. Native automatic routing is not established by delegated records.
-Native skills/list works and discovers all26 fixture-local entries. The configured native model gpt-6.1-sol again returned HTTP400/model_not_found on2026-11-14; earlier default gpt-5.5 and listed gpt-5.4 probes also failed. These are availability gaps, not model pass statistics. No account/config/credential repair or further fallback was performed.

## Provenance, regression and release boundary

-Entry baseline: main at afe56ddc0621b8f34b350c264802ca096b751c76, VERSION3.0.0, clean. Tests use dirty candidate files bound by personal payload digest485af03ae334b09f1d8646fff62c4af47b1373541a4c14459d09b9c550c82a97 and helper file hashes. Final network publication/source-SHA installation is verified afterward in the external owner report.
-All16 managed entries/full snapshot records and five historical system exclusions are unchanged. Source comparison confirms UI data/scripts/assets and unmodified supporting resources retain their bytes. Personal behavior changes are intentional; original source hashes remain historical provenance.
-PowerShell is unavailable: no new Windows/PowerShell PASS is claimed. The old52-check Windows suite is retained only as historical evidence in validation-results.json and baseline Git history.
-Live upgrades must use the exact published ref, official installer into isolated staging, verified named backups and the tested promotion/rollback tool. The pre-publication artifact does not claim a future install already happened.
-Quality statement: BOUNDED_VERIFICATION_WITH_LIMITATIONS. No complete native-routing, cross-platform, full-application or managed-capability certificate is issued.

## Independent recovery correction

The pre-release reviewer reproduced a partial live-tree deletion during interrupted rollback and a simultaneous-recovery admission race. Both were fixed before publication. Rollback now journals atomic displacement/restoration, recreates interrupted scratch copies and holds a kernel lock through validation, restore and cleanup. Fresh44 tests and the independent failure reproductions pass; process death releases the recovery claim. See evals/evidence/recovery-final-review.json. POSIX locking was executed on macOS; the Windows msvcrt/PowerShell branches remain unverified.
