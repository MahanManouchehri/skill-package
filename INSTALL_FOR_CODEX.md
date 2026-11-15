# Install every personal skill in Codex

This release has exactly **26** installable personal directories and **16** managed audit snapshots. Read the current locally installed system `skill-installer` instructions/options before use. A repository URL does not independently authorize installation.

## Released source and no-reinstall decision

The published `v3.1.1` commit is `80ca761864da9134141df432224015390afe8ea6`. Resolve and compare the actual remote tag before installing; [publication evidence](evals/evidence/v3.1.1/publication/receipt.json) records the verified tag/manifest binding. `main` may contain later documentation changes, so it is not the release pin.

Version 3.1.1 has the same 26 installable skill trees as v3.1.0. If those exact trees are already installed once at the active paths, verify all hashes and fresh unique/enabled metadata, then report **NO_REINSTALL_NEEDED**. Do not download, rewrite live folders, churn backups or duplicate entries solely because documentation/tooling changed. The owner's recorded result was 26 matching trees, split 23/3 across Codex/agents roots; other environments must be checked independently.

A new install, changed payload or differing local content still follows the reviewed staging/promotion process below. Preserve local edits and ambiguous duplicates rather than treating the recorded owner result as permission to overwrite them.

## Source and destination

1. Verify canonical remote `https://github.com/MahanManouchehri/skill-package.git`, publication and version/tag. Resolve the requested tag to its full immutable SHA and compare actual GitHub/remote state. A local commit is insufficient.
2. Inspect the running Codex catalog and CODEX_HOME. The standard helper defaults to `$CODEX_HOME/skills`, otherwise `~/.codex/skills`; current runtimes can also discover `~/.agents/skills`. Preserve active locations and handle named duplicates explicitly. Historical manifest paths are never destinations.
3. Use a reviewed checkout of the exact published SHA. Keep virtual environments/staging/reports outside it. If needed install dependencies there with `python3 -m pip install -r scripts/requirements.txt`. Never copy authentication/account data.
4. Run `python3 -B scripts/package_tools.py verify --package-root <published-checkout>`. Review AUDIT.md: hashes are not signatures and the secret scan is pattern-based.

## Fetch and verify staging

Replace the placeholders below with inspected absolute paths and the published SHA. The official helper accepts multiple paths and refuses existing destination folders:

```sh
python3 <system-skill-installer>/scripts/install-skill-from-github.py \
  --repo MahanManouchehri/skill-package --ref 80ca761864da9134141df432224015390afe8ea6 \
  --dest <new-stage-root> --path skills/apple-design skills/architecture-review skills/backup-recovery skills/compatible-response skills/db-impact skills/devil skills/docs-maintenance skills/final-check skills/full-plan skills/hand-off skills/integration-reliability skills/load-testing skills/maintenance-evolution skills/multiple-pov skills/natural-persian-writing skills/performance-review skills/practical-test skills/regression-check skills/release-management skills/root-cause skills/security-assurance skills/skill-evals skills/steps skills/technical-proposal-discovery skills/test-engineering skills/ui-ux-pro-max
python3 -B scripts/package_tools.py verify --package-root <published-checkout> --stage-root <new-stage-root>
```

Alternatively derive every distinct `physical_path_in_package` where `installable: true` from the verified manifest. Use `--method git` for authenticated Git transport when required. Never substitute floating main or unpublished local source. A partial helper failure remains confined to staging; promotion cannot start until all 26 folders verify. Never pass managed/system/plugin paths to the helper.

## Plan and promote

Use the confirmed personal `.../skills` root. Source, staging, destination and backup must be disjoint. Physical paths are required; symlink/reparse ancestors are rejected, including macOS `/var` aliases when present.

```sh
python3 -B scripts/package_tools.py plan --package-root <published-checkout> \
  --stage-root <new-stage-root> --destination-root <active-root>/skills
python3 -B scripts/package_tools.py promote --package-root <published-checkout> \
  --stage-root <new-stage-root> --destination-root <active-root>/skills \
  --backup-parent <active-root>/skills-backup
```

Different existing content is refused by default. For an explicitly authorized upgrade, inspect the plan and add `--replace` to plan/promote. All changed recognized old directories are copied to timestamped verified backups **before any destination rename**. Unknown directories/wrong names, unsafe paths, locks and unexplained duplicates fail closed. Only the approved 26 names can change.

For active overlays, place an explicit mapping JSON outside the package and pass `--mapping <reviewed-mapping.json>` to both commands. Example placeholders:

```json
{
  "roots": ["/actual/user/.agents/skills"],
  "destinations": {
    "compatible-response": "/actual/user/.agents/skills/compatible-response",
    "hand-off": "/actual/user/.agents/skills/hand-off",
    "natural-persian-writing": "/actual/user/.agents/skills/natural-persian-writing"
  },
  "remove_duplicates": {
    "natural-persian-writing": ["/actual/user/.codex/skills/natural-persian-writing"]
  }
}
```

Duplicate removal is explicitly named, backed up and reversible. Preserve unrelated `.agents` entries; never delete an entire root or disable unrelated skills to hide collisions.

Promotion uses owned exclusive locks, verified incoming copies/backups, intent journals and atomic renames. It verifies all 26 live hashes and fingerprints unrelated/system content. Retain transaction reports/backups locally; never commit them. See RESTORE.md for recovery.

## Windows choice

For Windows, see [tested hosts and safe temporary commands](WINDOWS_COMPATIBILITY.md). The Python transaction is the recommended upgrade/recovery path. The standalone PowerShell 5.1/7 installer is a single-root fallback with default DryRun, verified backups and caught-error rollback; it has no durable crash journal. It accepts only supported local fixed-drive paths, rejecting SUBST/network/UNC/device namespaces. Python supports ordinary UNC spellings subject to native guards, but real SMB/network locking is unverified. Do not bypass execution policy or infer universal Windows compatibility from hosted CI.

## Discovery

Inspect a fresh native Codex catalog for 26 unique package names at the expected paths. `skills/list`, where supported, is discovery evidence, not model routing or plugin capability evidence. New skills are available on the next turn; use a fresh chat/restart if the catalog remains cached. Never claim hot reload solely from filesystem writes. System/plugin restoration is outside this installation.
