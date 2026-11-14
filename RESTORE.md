# Restore, upgrade and rollback

For exact-SHA download/staging and active-root inspection, follow [INSTALL_FOR_CODEX.md](INSTALL_FOR_CODEX.md). The install set is exactly26 personal skills. Managed/system/plugin snapshots never enter personal roots; do not replace the whole .codex or .agents directory.

## Python promotion and recovery

Use Python3 with scripts/requirements.txt installed in an external environment. Verify package/staging, inspect plan and use --replace only for authorized recognized upgrades. A clean install refuses unknown or differing collisions by default. Every replaced directory and explicitly removed same-name duplicate is backed up and hash-verified before the first destination rename. Unchanged/unrelated directories remain outside ownership.

The returned timestamped backup root contains backups/ and transaction.json. Keep it private/local. The journal records exact approved paths, original/new hashes, backups, transaction identity and phase. It cannot grant itself authority: rollback requires trusted explicit allowed roots.

```sh
python3 -B scripts/package_tools.py rollback \
  --journal <verified-backup-root>/transaction.json \
  --allow-root <actual-codex-root>/skills
```

For a transaction spanning an agents overlay, also pass `--allow-root <actual-user>/.agents/skills`. Allowed roots must exactly match the reviewed journal scope. Never supply unknown roots merely to satisfy a journal. Backups under system/plugin/cache trees and unsafe links are refused.

Rollback validates every backup and all current owned states before changing anything. It restores original directories and removes only newly installed approved paths, preserving unrelated content. Post-install manual edits to an owned skill cause refusal instead of deletion; inspect and preserve those edits before recovery. Repeated rollback verifies the restored state. Backups remain available.

After an interrupted transaction, stop/confirm the original process is no longer alive, inspect its lock/journal, then use the same explicit rollback command. Another transaction's lock is never removed. A crash before the prepared journal exists has not renamed any destination; inspect the owned PREPARING scratch/lock and preserve all backups before targeted manual cleanup. Do not blindly delete locks or all stage directories. A failed automatic rollback is BLOCKED/recovery-required, not a successful install.

After installation or rollback, verify complete hashes and inspect a fresh Codex catalog; use the next turn/fresh chat/restart if needed. Discovery is distinct from model behavior.

## Windows PowerShell fallback

The original PowerShell5.1 scripts remain unchanged and retain their existing contract. They are a Windows fallback; current macOS execution does not establish a new Windows pass. Use a trusted exact-ref checkout or authorized archive with independent checksum when available.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -PackageOnly
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Install
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

Destination is CODEX_HOME/skills or USERPROFILE/.codex/skills, never manifest provenance paths. -DestinationRoot supports an isolated test root. The manifest supplies26 personal entries; managed snapshots are never installed. Existing recognized differences receive timestamped verified backups; unrelated/system/AGENTS/account content is preserved. Review install-report.json before manual recovery of only named directories. The Python overlay mapper is recommended for multiple active roots; PowerShell's single-root interface does not automatically consolidate overlays.

## Managed capabilities — separate restoration

The sixteen managed entries are historical audit snapshots. Enable the corresponding plugin/runtime through its supported destination mechanism and authenticate separately. Confirm actual active catalog entries, physical provider identity and tools; file existence/cache inventory alone does not prove activation. Consult PORTABILITY.md and runtime-catalog.example.json.

The PowerShell -RequireManaged option needs fresh caller-attested live catalog/capability evidence, not a fabricated success file. Provider versions may differ from historical snapshots. No package installer activates plugins, modifies provider caches or transfers account entitlements. Missing managed capabilities do not change the personal26 installation count, and must not be mislabeled a complete environment restore.

Recovery uses a nonblocking kernel lock (fcntl on POSIX, msvcrt on Windows) in addition to the installer marker; two recoveries cannot write the journal concurrently. Live trees are displaced atomically into owned scratch before restoration. A process crash releases kernel ownership and the next validated recovery can resume. Windows execution remains unverified on the current macOS build host.
