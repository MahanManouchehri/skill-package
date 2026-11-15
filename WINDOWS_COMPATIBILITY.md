# Windows compatibility and bounded validation

The v3.1.1 portability changes preserve the 26 personal skills, 16 archival
managed snapshots, five system exclusions, manifest schema 1, and byte-level
hash contract. They do not install plugins, grant model access, or establish
support for every Windows filesystem.

| Evidence | Current scope |
|---|---|
| STATIC_REVIEWED | Python transaction/recovery code; PowerShell installer, verifier, inventory and shared helpers; path, encoding, reparse and exclusion boundaries |
| CROSS_PLATFORM_TESTED | 57 package-tool tests executed on macOS and Windows Server 2025, including 13 added tests; Windows lexical decisions use the same production guard through PureWindowsPath |
| POWERSHELL_PARSED | Hosted Windows PowerShell 5.1.26100.33648 and PowerShell 7.6.9 each parsed all six scripts and passed the full disposable-profile driver; neither is locally installed on macOS |
| WINDOWS_CI_PASS | [Completed Windows Server 2025 run](https://github.com/MahanManouchehri/skill-package/actions/runs/43764630393): all five Python groups and both real PowerShell fixture drivers pass; scope bound to the recorded SHA/environment |

The [Windows validation workflow](.github/workflows/windows-validation.yml)
runs on windows-latest with contents:read permission and pinned official
[checkout v6.0.2](https://github.com/actions/checkout/releases/tag/v6.0.2) and
[setup-python v6.0.0](https://github.com/actions/setup-python/releases/tag/v6.0.0).
It does not change repository permissions or branch protection, persist checkout
credentials, require account secrets, invoke a model, or write actual Codex
profiles. TEMP, TMP, TMPDIR and CODEX_HOME point into runner.temp.

The immutable released source is `80ca761864da9134141df432224015390afe8ea6`. Both the [final commit CI](https://github.com/MahanManouchehri/skill-package/actions/runs/43764630393) and [tag CI](https://github.com/MahanManouchehri/skill-package/actions/runs/43765443386) pass on that source; [closure metadata](evals/evidence/v3.1.1/publication/README.md) preserves exact logs/results. The older `windows/ci-status.json` is a retained candidate snapshot, not the latest release binding. Documentation-only changes on main do not refresh these observations.

## Prerequisites and installer choice

Use Python 3.12 and PyYAML from [scripts/requirements.txt](scripts/requirements.txt)
for the verified workflow. Python may be exposed as py -3, python or python3;
confirm its actual path/version first. Windows Store aliases are not evidence
of an installed interpreter. PowerShell is optional for the Python tool.
The standalone PowerShell scripts target Windows PowerShell 5.1 and PowerShell
7; no external PowerShell module is required.
The standalone installer accepts local fixed-drive paths only. It uses the
read-only [QueryDosDeviceW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-querydosdevicew)
mapping and [GetDriveTypeW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getdrivetypew)
to compare package, destination, backup and staging identities. SUBST mappings,
UNC/network shares, removable/RAM drives and mappings
whose native identity is not an ordinary hard-disk volume are refused before
installation; this applies to DryRun too. Native API/compilation failures remain
visible. Copy the package to a local fixed drive and use an ordinary personal
skills root for this fallback.

For live restoration, use the official skill-installer pinned to the published
commit to obtain a clean staging tree, then use the verified Python
plan/promote/rollback transaction described in [INSTALL_FOR_CODEX.md](INSTALL_FOR_CODEX.md).
The package tool is a local verifier/promoter, not a replacement downloader.
It requires an explicit destination .../skills root and refuses protected
system, plugin, cache, managed and overlapping paths.

The PowerShell installer defaults to DryRun. Its explicit -Install mode keeps
verified backups and handles caught exceptions, but it has no durable on-disk
transaction journal for process death. Use the Python transaction for upgrades
that require resumable crash recovery. A stale lock is a refusal condition;
do not delete an unexplained lock or copy an unverified backup over live data.

The default PowerShell root is CODEX_HOME/skills when CODEX_HOME is set, otherwise
USERPROFILE/.codex/skills. USERPROFILE/.agents/skills is supported through explicit
-DestinationRoot. The Python tool supports both roots through its explicit
mapping/duplicate-removal contract; it does not guess which live copy is active.
Inspect actual Codex discovery and preserve the two-root mapping before a live
upgrade. Managed/system/plugin folders remain outside the install payload.

## Safe user-run dry-run

Run from the package checkout. Keep the virtual environment and fixtures outside
the distribution: unlisted files correctly invalidate package integrity.
The example creates only a unique directory under TEMP and does not install
into a real profile. If py -3 is unavailable, select an existing Python 3.12
interpreter and use its absolute path for the venv command.

```powershell
py -3 --version
$fixture = Join-Path $env:TEMP ('skill-package-check-' + [Guid]::NewGuid().ToString('N'))
$venv = Join-Path $fixture 'venv'
py -3 -m venv $venv
$python = Join-Path $venv 'Scripts/python.exe'
& $python -m pip install -r .\scripts\requirements.txt
& $python -B .\scripts\package_tools.py verify --package-root .
$stage = Join-Path $fixture 'stage'
Copy-Item -LiteralPath .\skills -Destination $stage -Recurse
$destination = Join-Path $fixture 'profile/.codex/skills'
& $python -B .\scripts\package_tools.py plan --package-root . --stage-root $stage --destination-root $destination
.\scripts\install.ps1 -DryRun -DestinationRoot $destination -PluginCacheRoot (Join-Path $fixture 'absent-plugin-cache')
```

Copying the trusted checkout into this fixture is for an offline dry-run; live
staging must follow the pinned official-installer procedure. Review the plan,
actual interpreter, destination and package hashes before choosing a live action.
An execution-policy restriction remains visible; this procedure does not change
machine/user policy.

To execute the full safe Windows verification after dependencies are available:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
& $python -B -m unittest discover -s tests -p test_package_tools.py -v
& $python -B -m unittest discover -s evals -p test_runner.py -v
& $python -B -m unittest discover -s skills/ui-ux-pro-max/scripts/tests -p 'test_*.py' -v
& $python -B -m unittest discover -s tests -p test_ui_authoring.py -v
& $python -B .\tests\windows_native_checks.py -v
powershell.exe -NoLogo -NoProfile -NonInteractive -File .\tests\windows_powershell_checks.ps1 -ScratchParent $env:TEMP -Python $python
pwsh -NoLogo -NoProfile -NonInteractive -File .\tests\windows_powershell_checks.ps1 -ScratchParent $env:TEMP -Python $python
```

Each PowerShell driver creates and removes its own unique temporary profile,
checks its own parser, real installation/replacement, backup hashes, injected
caught-error rollback, idempotence, inventory output refusal, UTF-8 BOM/CRLF
metadata, Unicode/metacharacter paths, CODEX_HOME and USERPROFILE defaults, and
an explicit .agents dry-run. It also creates a temporary SUBST drive, checks that
an aliased source destination is refused without changing package bytes, and
removes the mapping in finally. UNC installation is refused without accessing
the share. The four additional Python Windows tests use actual
junctions, a file handle denying FILE_SHARE_DELETE, and a long
Unicode destination. The normal 57-test suite also runs real concurrent
recovery and crash/resume tests against the Windows msvcrt backend.

## Recovery and restrictions

After Python promotion, retain the returned journal and backup_root. Recover
only after the installer is no longer active, using the exact reviewed roots:

```powershell
& $python -B .\scripts\package_tools.py rollback --journal $journal --allow-root $destination
# For a transaction spanning both roots, repeat --allow-root for the .agents root.
```

Rollback verifies all retained backup hashes, explicit allowed roots and current
destination states before restoring. It refuses unrelated later edits, changed
backups, untrusted journal scope, live competing processes and reparse paths.
Interrupted owned restore copies can be rebuilt from the verified backup.
Backups remain after recovery. The standalone PowerShell fallback has a different
report format and must not be passed to Python rollback; see [RESTORE.md](RESTORE.md).

The Windows liveness probe now uses read-only OpenProcess/SYNCHRONIZE and a
zero-time WaitForSingleObject call. It never uses os.kill(pid, 0): on Windows,
Python documents that call as terminating the target for ordinary signal values.
An inaccessible or uncertain process is conservatively considered live.
See [Python os.kill](https://docs.python.org/3/library/os.html#os.kill),
[OpenProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess)
and [WaitForSingleObject](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject).

Package-relative paths reject traversal, backslashes, drive/UNC/ADS syntax,
reserved devices (including superscript device digits), control characters,
trailing dots/spaces and case variants of protected components. Device/extended
namespace paths are refused because alternative spellings can bypass lexical
overlap checks; use ordinary absolute paths. Python accepts ordinary drive/UNC
spellings subject to its native guards; the standalone PowerShell installer
supports only the local fixed-drive subset described above.
Both tools conservatively refuse tilde-digit short-name spellings and trailing
dots/spaces in Windows path components. Python also applies overlap and protected
root/backup checks to canonical native Windows realpath results, covering drive aliases.
PowerShell compares read-only native volume identities for accepted local drives
and fails closed for unsupported aliases; it does not claim UNC/SMB identity safety.
Manifest file paths and catalog names must be unique without case distinctions. Existing
approved/managed catalog names with different case cannot bypass collision
checks. Owned trees reject links/reparse points; unrelated junctions are
fingerprinted as links without traversing their targets.

The .gitattributes rule * -text is intentional. The Git fixture clones LF, CRLF,
BOM, binary and Unicode filenames with autocrlf=true, false and input and checks
exact bytes. Hashes ignore timestamps and retain BOM/newline differences. CLI
JSON is explicitly UTF-8 even when redirected from a legacy Windows codepage.
Do not run a line-ending converter over the distribution.

Renames happen inside destination-adjacent scratch directories; verified backups
are copied, not assumed to be cross-volume atomic moves. Multi-skill promotion
is a journalled sequence, not one globally atomic filesystem operation. Read-only
copies can be cleaned only inside owned scratch; retained backups keep their
attributes. Sharing violations, antivirus interference and other permission
failures remain visible. No retry loop clears live-file attributes or bypasses
an active process lock.

Actual UNC/SMB shares, different backup volumes, network lock semantics, antivirus
products, machines with ordinary long paths disabled, every reparse
type, abrupt power loss and arbitrary user ACLs remain outside the hosted fixture.
PureWindowsPath tests prove lexical decisions only. A successful Windows run
supports its specific Python/PowerShell/runner configuration, not universal
Windows compatibility. Model/account eligibility and plugin capabilities require
separate native evidence.

Hosted evidence, exact counts and the earlier real failures are retained in [v3.1.1 CI status](evals/evidence/v3.1.1/windows/ci-status.json). Git read-only fixture cleanup, descendant cwd sharing, preserved legacy path spelling and backup-report fixture expectations were corrected without skipping or weakening assertions. Independent test groups still fail the job on any failure and run only after package verification succeeds.
