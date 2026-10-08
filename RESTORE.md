# Manual restore on another Windows user/account

For Codex plugin installation from the repository URL, follow the **Install in Codex** section of `README.md`. This document is the Windows PowerShell fallback for a direct, hash-verified copy into the user skill directory.

## Get the bundle

Authenticate GitHub separately if using the private repository:

```powershell
git clone https://github.com/MahanManouchehri/skill-package.git
cd skill-package
```

Alternatively extract `skill-package-portable.zip` into a new folder and open PowerShell in that extracted folder. The ZIP does not contain `.git`, credentials, sessions or runtime cache. Check the independently supplied ZIP SHA-256 against the archive before extraction when available.

## Phase A: personal/user-global skills

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -PackageOnly
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Install
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

This installs only 16 personal skills. The manifest is the count authority. The installer uses CODEX_HOME if set, otherwise the current USERPROFILE; it never reads the original source paths as destinations. The dry-run lists installs, replacements, conflicts and dependency limitations without changing any files. Resolve conflicts before installing; the scripts never merge skills or make manual copies of managed skills.

An existing different personal skill is backed up to `<parent-of-skills>\skills-backup\<UTC timestamp>-<unique ID>\<skill>`. `install-report.json` records changed skills and backup locations. Unchanged content is skipped. Retain backups until you have verified the restored environment. To roll back manually, close Codex, inspect that report, and restore only the reported personal directories from the chosen backup. Do not replace the entire `.codex` directory.

Restart Codex or open a fresh chat after installation and confirm the personal entries appear exactly once in the live skill catalog. The disk verifier confirms discoverable metadata, structure, references and hashes; live runtime discovery must also be checked in Codex.

## Phase B: managed capabilities

1. Open destination Codex Settings → Plugins (or the available Plugins interface).
2. Find/enable each provider/plugin in PORTABILITY.md using the supported interface. Some bundled/runtime plugins are supplied by Codex and may have no separate install button. If unavailable, report **MISSING RUNTIME/PLUGIN DEPENDENCY**.
3. Connect/authenticate required services separately. Verify the actual required tools/runtime, including Excel's connected add-in session when using live Excel control. File snapshots do not supply these capabilities.
4. In a fresh destination chat, inspect the **active** catalog, identify actual physical plugin skill directories, and check tools. Populate a runtime evidence JSON outside the bundle using `runtime-catalog.example.json` as its schema. Never use cache inventory alone as evidence. Never set `enabled` or `capabilities_confirmed` true without observing them.
5. Run strict verification with that evidence and the destination plugin cache root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -RuntimeCatalogPath C:\path\to\runtime-catalog.json -RequireManaged
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\inventory.ps1 -RuntimeCatalogPath C:\path\to\runtime-catalog.json -OutputPath C:\path\to\inventory.json
```

For a nondefault runtime layout, also pass `-PluginCacheRoot <actual-provider-plugin-version-cache-root>`. Current verification supports the observed provider/plugin/version/skills layout. An unsupported destination layout requires inspection, not manual snapshot copying.

Runtime evidence must be observed within the last 24 hours. Runtime evidence is a caller attestation from a live Codex catalog/tool inspection, not a cryptographic assertion. The verifier checks its fields against the destination disk and provider layout but cannot itself ask Codex whether tools are enabled. Refresh it after switching accounts, enabling/disabling plugins or restarting/changing runtime. Current provider upgrades may differ from snapshot hashes; the verifier reports that difference without overwriting provider files.

Expected final outcome: 16 personal skills hash-verified; 16 managed skill entries provided and catalog-verified through proper plugins/runtime; system skills informational; unexpected duplicates 0. Missing managed capability keeps full environment restoration incomplete even when Phase A passes.

## Giving the folder to a new Codex

Use this prompt with the extracted folder or authorized private repository:

> Read README.md, RESTORE.md, PORTABILITY.md and skills-manifest.json. Audit package integrity, run install.ps1 -DryRun, restore only the installable user-global skills, then verify hashes and duplicates. Restore plugin capabilities through their supported mechanisms; never install managed/plugin-skills into user skills or plugin cache. Inspect the fresh active catalog/tools and report missing runtime/plugin dependencies separately. Do not alter skill content, system skills, AGENTS.md, account config or credentials.

## Isolated test

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -DryRun -DestinationRoot C:\path\to\temporary-test\skills
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Install -DestinationRoot C:\path\to\temporary-test\skills
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -DestinationRoot C:\path\to\temporary-test\skills
```
