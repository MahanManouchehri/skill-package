# Source and release audit — 3.1.1

## Published source and lineage

Canonical repository: [MahanManouchehri/skill-package](https://github.com/MahanManouchehri/skill-package). The immutable `v3.1.1` annotated tag resolves to `80ca761864da9134141df432224015390afe8ea6`; tag object `cd2a33f7c977e752d3afec6a1ac1e31c36f170cf`. Publication, exact manifest binding and the owner's observed installation result are retained in the [closure records](evals/evidence/v3.1.1/publication/README.md). The [final commit CI](https://github.com/MahanManouchehri/skill-package/actions/runs/43764630393) and [tag CI](https://github.com/MahanManouchehri/skill-package/actions/runs/43765443386) both completed successfully on this SHA.

Version3.1.0 at `11d61b3e05afaf2749d7314d1a72d0c1d9ed3523` upgraded16 original personal skills and added10 specialists. Version3.1.1 preserves every one of those26 personal payloads, all16 managed archival entries and five system exclusions. The earlier v3.0.0 baseline was `afe56ddc0621b8f34b350c264802ca096b751c76`; its historical source hashes remain provenance, not claims of equality after the v3.1.0 behavior upgrade. Main can contain subsequent documentation-only commits; the released tag is not moved.

## Stabilization changes and executed evidence

- Native evaluation uses an explicit executable/model, catalog-plus-real-turn preflight, invocation-only service/host-skill overlays and exact26-entry fixture metadata checks. Discovery uses bounded portable pipe reading; external body reads and post-turn fixture changes are flagged. Model support was confirmed with the official app-bundled CLI0.167.0-alpha.3.2/gpt-6.1-sol and native ChatGPT login, without replacing Brew0.142.5 or copying credentials.
- Authentic UI authoring helpers are pinned to upstream6ae86f61f520d6ca229d2f40e070410638c908c5 with the MIT notice. The development-only launcher projects actual bytes into the pristine grader's canonical layout. All70 UI runtime/test/fixture files, all assertions and frozen thresholds remain unchanged. Full153 UI tests, five launcher regressions and the90-case frozen gate pass; [provenance](UI_AUTHORING_PROVENANCE.md).
- Windows liveness uses read-only kernel handles instead of os.kill(pid,0). Canonical path, namespace/device/case, read-only recovery and UTF-8 boundaries have actual hosted coverage. The standalone PowerShell installer verifies native fixed-drive identity before writes and rejects unsupported aliases. [Windows compatibility](WINDOWS_COMPATIBILITY.md) records57 package,27 runner,153 UI,5 launcher and4 Windows filesystem tests plus both full PS5.1/7 fixture drivers.
- Twelve historical PARTIAL routing observations were adjudicated separately: A0/B7/C5/D0. No skill-policy patch or universal steps activation was justified. Original owner prompts/assertions and earlier evidence were not rewritten. The current matrix's filename/index prose can be maintained without changing its60 scenario rows.

## Packaging and installation boundary

Manifest schema1 and the aggregate algorithm remain compatible: SHA256 of UTF8 ordinal-sorted relative path + NUL + lowercase file SHA256 + LF. Package-integrity covers every distribution file except itself and .git. Build updates generated records; environments, generated caches and unrelated reports belong outside the checkout. Hashes detect changes; they are not signatures or independent authentication. For the released snapshot,869 distribution files and625 protected files were verified; a later documentation checkout has its own regenerated integrity/count.

The official system installer is the downloader for changed/new personal installs: exactly26 manifest-listed paths at the immutable published SHA into empty staging. The Python transaction verifies complete staging, refuses differing collisions unless replacement is explicitly authorized, verifies backups before renames, holds locks/journals and supports tested interrupted rollback. Named duplicate consolidation requires explicit mapping. Unknown directories, symlinks/reparse escapes, system/plugin/cache roots and unrelated entries are protected.

For v3.1.1 the owner already had matching payloads:26 hashes and26 unique enabled native metadata entries were verified, split23/3 across Codex/agents roots. The result is NO_REINSTALL_NEEDED, with no new live write or backup. This is a recorded host observation; other users must inspect their own roots and content before choosing the [installation path](INSTALL_FOR_CODEX.md). Live transaction backups/auth/account data do not belong in the repository; the published receipts contain hashes/metadata, not those files.

## Preserved earlier corrections

The v3.1.0 upgrade repaired natural-persian-writing YAML, resolved UI search from the actual loaded directory, synchronized full-plan authorization and preserved practical-test/hand-off boundaries. Those skill bytes are unchanged in v3.1.1.

Earlier independent recovery review reproduced recursive live-tree deletion during rollback and simultaneous stale-lock recovery. The corrected transaction displaces live trees into owned scratch, stages verified restoration, and holds kernel locks throughout recovery. POSIX and actual Windows crash/concurrency fixtures now pass. Windows Git read-only test cleanup, descendant fixture cwd sharing, valid parent-link normalization and backup-report fixture expectations were also corrected; their failed runs remain preserved.

## Security and verification limits

Strict YAML rejects duplicate keys/aliases. Validation checks names/directories, resources/references, safe portable paths, case-insensitive collisions, file/tree/distribution coverage, tamper/omission and common secret/sensitive-filename patterns. A zero-candidate scan is bounded evidence, not proof against every possible secret. No auth/config rewrite, credential transfer, live plugin/system copy or account-entitlement repair was performed. The model-cache hash changed during runtime activity and is not claimed byte-preserved.

The native bank has60 designed,12 unique attempted,10 completed,2 usage-cap blocked and48 unexecuted cases. Independent raw review yields eight scoped read-only plan PASS and two source-isolation FAIL (S07/S12), even though returned host-body bytes match the fixture. The final corrective harness has unit coverage and no post-cap model rerun. Catalog overlays are not a filesystem read jail; dynamic commands require raw review. All full-application/browser/provider/production acceptance remains UNVERIFIED. [Validation](VALIDATION.md) and the [Persian final report](evals/evidence/v3.1.1/publication/report.fa.md) retain these limitations.

Metadata discovery, workflow activation and execution authority are separate. Skills cannot grant service access, enforce routing or authorize production effects. Managed snapshots describe historical provider resources, not current activation. Hosted Windows evidence is scoped to the recorded configuration; real SMB/UNC, arbitrary ACLs/antivirus, every reparse type and power-loss behavior remain outside the fixtures.
