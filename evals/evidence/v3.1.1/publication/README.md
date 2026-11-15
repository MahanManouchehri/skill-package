# Published v3.1.1 closure evidence

These records describe the immutable released snapshot `80ca761864da9134141df432224015390afe8ea6`, annotated tag `v3.1.1`, and the owner's installation observation from that release. Later documentation-only commits on main do not move the tag, repeat native model evaluation or refresh the recorded installed state.

- [Persian final report](report.fa.md) and [final acceptance audit](final-check.md): DONE_WITH_LIMITATIONS; the overall audit is PARTIAL because native coverage is incomplete.
- [Publication/install receipt](receipt.json): remote commit/tag binding, schema1 manifest,26 matching installed trees and NO_REINSTALL_NEEDED.
- [Installed discovery](installed-discovery.json):26 unique enabled personal entries, metadata only.
- [Commit CI](commit-ci.json) / [raw log envelope](commit-ci-log.json) / [markers](commit-ci-markers.txt): completed Windows Server2025 run43764630393 on the released SHA.
- [Tag CI](tag-ci.json) / [raw log envelope](tag-ci-log.json): completed run43765443386 on the identical SHA.
- [Release change inventory](changed-files.json):235 release files with reasons/hashes. Paths are repository-relative; this is not the later documentation diff.
- [Preservation receipt](invariants.json):625 files unchanged in the release; [native case table](native-cases.csv):12 attempted bank cases.

The installed paths in historical receipts are observations, not portable destinations or future installation authority. Current guides resolve the active roots. No auth files, tokens, runtime binaries or live plugin/system payloads are included.

The derived native case CSV is exported with LF line endings for Git whitespace checks; parsed cell values match the original delivery table exactly. Original raw model stdout/stderr and all prior evidence remain byte-identical.
