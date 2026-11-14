# Source and release audit — 3.1.0

## Scope and provenance

Canonical repository: MahanManouchehri/skill-package. Entry baseline: main at `afe56ddc0621b8f34b350c264802ca096b751c76`, version3.0.0, clean worktree,16 personal and16 managed entries. Version3.1.0 was unused when release work began. The owner explicitly approved implementation, tests, scoped commit/push and personal-skill installation; no unrelated production or account action is included.

The personal set is now26 unique names: all16 originals intentionally upgraded,10 approved specialists added. Historical personal source paths/hashes remain provenance. They no longer assert equality to the intentionally modified package; new entries originate in this repository. Managed entries and complete managed snapshot trees are retained unchanged, including provider-relative resources. The five historical system exclusions remain unchanged.

## Corrected legacy issues

- natural-persian-writing now has strict valid YAML without changing its language meaning.
- ui-ux-pro-max resolves scripts/data relative to its actual loaded installed directory; the package no longer requires CLAUDE_PLUGIN_ROOT. Existing datasets/scripts/assertions are preserved.
- full-plan approval rules are synchronized across its main instructions, docs and platform adapters. Authorized routine API work proceeds; unresolved material decisions and real governance restrictions remain gates.
- practical-test accepts previously confirmed safe targets; hand-off preserves its four modes and follows project documentation layout. Neither starts services or writes unsolicited handoff documents.
- Existing text files modified for the upgrade use LF line endings. Semantically unchanged resources retain their original bytes.

## Packaging and installation boundary

Manifest schema1 and the aggregate algorithm remain compatible: SHA256 of UTF8 ordinal-sorted relative path + NUL + lowercase file SHA256 + LF. Personal files and all distribution files are independently checked. package-integrity excludes itself and .git only; generated artifacts/environments belong outside the distribution. Source history is retained, never rewritten.

The official system installer downloads only26 manifest-listed personal paths at the published SHA into empty staging. The Python transaction tool verifies complete staging, rejects collisions by default, requires explicit replacement scope, verifies all backups before renames, uses owned locks/journals and supports tested rollback/crash recovery. Named duplicate consolidation is explicit and backed up. Unknown directories, symlinks/reparse escapes, system/plugin roots and unrelated entries are protected.

Different existing local versions are recognized as historical copies of the approved names and preserved in complete verified backups before replacement. No arbitrary merge of old local instructions is claimed. The old UI copy is smaller than the packaged dataset; the approved package resources are retained. Backup/account/credential files are never added to the repository.

## Security and verification limits

Strict YAML forbids duplicate keys and aliases. Checks include names/directory equality, references/assets, safe portable paths, case-insensitive collisions, file/tree/integrity coverage, omission/tamper detection and common secret patterns/sensitive filenames. Scanner results do not prove absence of every possible secret; owned diffs also require inspection. No credentials, account settings, chats, runtime binaries or plugin activation state are transferred.

Skill metadata discovery, workflow activation and execution authority are separate. Explicit-only workflows remain discoverable for direct natural-language intent, but installation cannot enforce model routing or grant production authority. Runtime-managed snapshots do not supply service access or tools.

Current executed evidence and limitations are in VALIDATION.md and validation-results.json. Historical Windows results are historical only. A native skills/list observation verifies discovery; delegated read-only routing/planning observations are not full application implementation, browser acceptance or native CLI model execution.

## Independent recovery review

Two concrete defects were found and corrected before publication: recursive deletion of a live skill during rollback, and nonexclusive recovery of a stale installer lock. The final implementation uses atomic live-tree displacement, retryable verified restore staging and held kernel locks. Independent reproduction, two-process contention and actual process-crash tests pass. Original failure and final-review evidence are retained under evals/evidence.
