[CmdletBinding()]
param(
    [string]$ScratchParent = $env:RUNNER_TEMP,
    [string]$Python = 'python'
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'WINDOWS_RUNTIME_UNVERIFIED: this driver requires Windows.' }
if (-not $ScratchParent) { $ScratchParent = [IO.Path]::GetTempPath() }
$scratchFull = [IO.Path]::GetFullPath($ScratchParent).TrimEnd('\','/')
$allowed = @([IO.Path]::GetTempPath())
if ($env:RUNNER_TEMP) { $allowed += $env:RUNNER_TEMP }
$permitted = $false
foreach ($candidate in $allowed) {
    $candidateFull = [IO.Path]::GetFullPath($candidate).TrimEnd('\','/')
    if ($scratchFull -eq $candidateFull -or $scratchFull.StartsWith($candidateFull+'\',[StringComparison]::OrdinalIgnoreCase)) { $permitted = $true }
}
if (-not $permitted) { throw 'ScratchParent must be inside the operating-system temp directory or RUNNER_TEMP.' }
$packageRoot = Split-Path -Parent $PSScriptRoot
. (Join-Path $packageRoot 'scripts/common.ps1')
Assert-NoReparse $scratchFull

function Assert-Condition([bool]$Condition, [string]$Message) {
    if (-not $Condition) { throw "Fixture assertion failed: $Message" }
}
function Assert-Refused([scriptblock]$Action, [string]$Pattern) {
    $refused = $false
    try { & $Action } catch {
        if ($_.Exception.Message -notmatch $Pattern) { throw }
        $refused = $true
    }
    Assert-Condition $refused "Expected refusal matching $Pattern"
}
function Invoke-PackageTool([string[]]$Arguments) {
    $json = & $Python -B (Join-Path $packageRoot 'scripts/package_tools.py') @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Package tool failed with exit $LASTEXITCODE" }
    return (($json -join [Environment]::NewLine) | ConvertFrom-Json)
}
function Get-BackupState([string]$Root) {
    $exists = Test-Path -LiteralPath $Root
    [string[]]$listing = @()
    [string[]]$fileHashes = @()
    if ($exists) {
        Assert-Condition (Test-Path -LiteralPath $Root -PathType Container) 'Backup root is not a directory'
        Assert-TreeNoReparse $Root
        $listing = @(Get-ChildItem -LiteralPath $Root -Force -Recurse | ForEach-Object {
            $(if ($_.PSIsContainer) { 'directory:' } else { 'file:' }) + (Get-Relative $Root $_.FullName)
        })
        $fileHashes = @(Get-TreeFiles $Root -IncludeGenerated | ForEach-Object {
            (Get-Relative $Root $_.FullName) + [char]0 + (Get-SHA256 $_.FullName)
        })
        [Array]::Sort($listing, [StringComparer]::Ordinal)
        [Array]::Sort($fileHashes, [StringComparer]::Ordinal)
    }
    return [pscustomobject]@{ exists=$exists; listing=($listing -join "`n"); sha256=(Get-TextHash ($fileHashes -join "`n")) }
}

# Parse the actual .ps1 distribution, including the optional skill validator.
# A PS7 parse is never recorded as a PS5.1 parse.
$parsed = 0
foreach ($file in Get-ChildItem -LiteralPath $packageRoot -Recurse -File -Filter '*.ps1') {
    $tokens = $null; $errors = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile($file.FullName,[ref]$tokens,[ref]$errors)
    if (@($errors).Count) { throw ("PowerShell parse failed: " + $file.FullName + ': ' + (($errors | ForEach-Object Message) -join '; ')) }
    $parsed++
}
Write-Host "POWERSHELL_PARSED: $parsed scripts on $($PSVersionTable.PSVersion)"
$fixture = Join-Path $scratchFull ('skill-package-ps-' + [Guid]::NewGuid().ToString('N'))
$oldCodexHome = $env:CODEX_HOME; $oldProfile = $env:USERPROFILE
$oldPythonUtf8 = $env:PYTHONUTF8
$oldOutputEncoding = [Console]::OutputEncoding
$global:SkillPackageFixtureMoveCount = 0
try {
    [void](New-Item -ItemType Directory -Path $fixture)
    # Construct Persian text with codepoints so PS5.1 needs no UTF-8 BOM here.
    $unicode = -join @([char]0x645,[char]0x633,[char]0x6CC,[char]0x631)
    $fixtureProfile = Join-Path $fixture ($unicode + " & literal [x] ' profile")
    $env:USERPROFILE = $fixtureProfile
    $env:CODEX_HOME = Join-Path $fixtureProfile '.codex'
    $env:PYTHONUTF8 = '1'
    [Console]::OutputEncoding = New-Object Text.UTF8Encoding($false)
    $OutputEncoding = [Console]::OutputEncoding
    $destination = Join-Path $env:CODEX_HOME 'skills'
    $pluginCache = Join-Path $env:CODEX_HOME 'plugins/cache'
    Assert-Condition ((Get-CodexRoot) -ceq $env:CODEX_HOME) 'Custom CODEX_HOME was not honored'
    $env:CODEX_HOME = $null
    Assert-Condition ((Get-CodexRoot) -ceq (Join-Path $fixtureProfile '.codex')) 'USERPROFILE fallback was not honored'
    $env:CODEX_HOME = Join-Path $fixtureProfile '.codex'

    foreach ($bad in @('../outside','..\outside','C:\outside','C:outside','\\server\share\outside','a:stream','.SYSTEM/a','.git/a','a/NUL.txt','a/COM1.log','a./b','a /b','a//b','a/*')) {
        Assert-Refused { Get-SafePath $fixture $bad } 'Invalid|Unsafe|Reserved|escapes'
    }
    $drive = [IO.Path]::GetPathRoot($fixture)
    Assert-Refused { Assert-NoReparse (Join-Path $fixture 'SHORT~1/skills') } 'short aliases'
    Assert-Refused { Assert-NoReparse (Join-Path $fixture 'profile./skills') } 'trailing dots/spaces'
    Assert-Refused { Assert-NoReparse (Join-Path $fixture 'profile /skills') } 'trailing dots/spaces'
    Assert-Refused { Assert-NoReparse ('\\?\' + $fixture) } 'namespace|not supported|format'
    Assert-Condition ((Get-SafePath $drive 'fixture-file') -ceq (Join-Path $drive 'fixture-file')) 'Drive-root relative path handling failed'
    $nested = Join-Path $fixture 'hash/nested'
    [void](New-Item -ItemType Directory -Path $nested -Force)
    $utf8 = New-Object Text.UTF8Encoding($false)
    [IO.File]::WriteAllText((Join-Path $nested 'file.txt'),$unicode,$utf8)
    Assert-Condition ((Get-Relative (Join-Path $fixture 'hash') (Join-Path $nested 'file.txt')) -ceq 'nested/file.txt') 'Hash paths must use forward slashes'
    # A script path avoids PS5.1's lossy native -c quoting rules.
    $pythonHash = & $Python -B (Join-Path $packageRoot 'tests/windows_native_checks.py') --tree-hash (Join-Path $fixture 'hash')
    Assert-Condition ($LASTEXITCODE -eq 0 -and $pythonHash -ceq (Get-TreeHash (Join-Path $fixture 'hash'))) 'Python and PowerShell fingerprints differ'
    $crlf = [string][char]13 + [char]10
    $description = 'Fixture ' + $unicode
    $frontmatter = '---' + $crlf + 'name: steps' + $crlf + 'description: ' + $description + $crlf + '---' + $crlf
    [IO.File]::WriteAllText((Join-Path $nested 'SKILL.md'),$frontmatter,(New-Object Text.UTF8Encoding($true)))
    Assert-Condition ((Get-SkillMetadata (Join-Path $nested 'SKILL.md')).description -ceq $description) 'BOM/CRLF Unicode metadata decoding failed'
    & (Join-Path $packageRoot 'scripts/verify.ps1') -PackageOnly
    [void](Invoke-PackageTool -Arguments @('verify','--package-root',$packageRoot))
    Assert-Condition ((Get-LocalInstallPathIdentity $fixture) -match '^\\Device\\HarddiskVolume[0-9]+\\') 'Local fixed-drive identity was not verified'
    Assert-Refused { & (Join-Path $packageRoot 'scripts/install.ps1') -Install -DestinationRoot (Join-Path $packageRoot 'skills') } 'Unsafe destination'
    Assert-Refused { & (Join-Path $packageRoot 'scripts/install.ps1') -Install -DestinationRoot '\\localhost\skill-package-unavailable\profile\skills' } 'local fixed-drive.*UNC'
    # A real SUBST alias to the source must be refused before any package writes.
    $subst = Join-Path $env:SystemRoot 'System32/subst.exe'
    $substDrive = $null
    try {
        foreach ($codepoint in 90..68) {
            $letter = [string][char]$codepoint
            if (Get-PSDrive -Name $letter -ErrorAction SilentlyContinue) { continue }
            $candidate = $letter + ':'
            & $subst $candidate (Split-Path -Parent $packageRoot)
            if ($LASTEXITCODE -ne 0) { throw 'Could not create the isolated SUBST fixture.' }
            $substDrive = $candidate
            break
        }
        Assert-Condition ($null -ne $substDrive) 'No free drive letter for the isolated SUBST fixture'
        $aliasDestination = $substDrive + '\' + (Split-Path -Leaf $packageRoot) + '\skills'
        Assert-Condition ([IO.Directory]::Exists($aliasDestination)) 'SUBST did not alias the source skills directory'
        $sourceBeforeAlias = Get-TreeHash $packageRoot
        Assert-Refused { & (Join-Path $packageRoot 'scripts/install.ps1') -Install -DestinationRoot $aliasDestination } 'SUBST|drive mapping'
        Assert-Condition ((Get-TreeHash $packageRoot) -ceq $sourceBeforeAlias) 'Refused SUBST installation changed package bytes'
    } finally {
        if ($substDrive) {
            & $subst $substDrive /D
            if ($LASTEXITCODE -ne 0) { throw 'Could not remove the isolated SUBST fixture.' }
        }
    }
    $before = Get-TreeHash $fixture
    & (Join-Path $packageRoot 'scripts/install.ps1') -DryRun
    & (Join-Path $packageRoot 'scripts/install.ps1') -DryRun -DestinationRoot (Join-Path $fixtureProfile '.agents/skills')
    Assert-Condition ((Get-TreeHash $fixture) -ceq $before) 'Default-root dry-run mutated the fixture'
    Assert-Condition (-not (Test-Path -LiteralPath $destination)) 'Dry-run created a destination'

    # Real standalone installer execution in a disposable profile.
    & (Join-Path $packageRoot 'scripts/install.ps1') -Install
    $verified = & (Join-Path $packageRoot 'scripts/verify.ps1') -DestinationRoot $destination -PassThru
    Assert-Condition ($verified.user_global_verified -eq 26) 'PowerShell installation did not verify all 26 personal skills'
    Assert-Condition (@(Get-ChildItem -LiteralPath $destination -Directory).Count -eq 26) 'Managed/system data was installed'
    $originalTree = Get-TreeHash $destination
    $backupParent = Join-Path $env:CODEX_HOME 'skills-backup'
    $backupBeforeIdempotent = Get-BackupState $backupParent
    & (Join-Path $packageRoot 'scripts/install.ps1') -Install
    Assert-Condition ((Get-TreeHash $destination) -ceq $originalTree) 'Idempotent install changed bytes'
    $backupAfterIdempotent = Get-BackupState $backupParent
    Assert-Condition ($backupAfterIdempotent.exists -eq $backupBeforeIdempotent.exists -and $backupAfterIdempotent.listing -ceq $backupBeforeIdempotent.listing) 'Idempotent install churned backup directories or files'
    Assert-Condition ($backupAfterIdempotent.sha256 -ceq $backupBeforeIdempotent.sha256) 'Idempotent install changed retained backup bytes'
    [IO.File]::WriteAllText((Join-Path $destination 'steps/local.txt'),'preserved original bytes',$utf8)
    $stepsHash = Get-TreeHash (Join-Path $destination 'steps')
    $reportsBeforeReplacement = @(Get-ChildItem -LiteralPath $backupParent -Recurse -File -Filter 'install-report.json' | ForEach-Object FullName)
    & (Join-Path $packageRoot 'scripts/install.ps1') -Install
    $newReports = @(Get-ChildItem -LiteralPath $backupParent -Recurse -File -Filter 'install-report.json' | Where-Object { $_.FullName -notin $reportsBeforeReplacement })
    Assert-Condition ($newReports.Count -eq 1) 'Replacement did not create exactly one new backup report'
    $report = $newReports[0]
    Assert-Condition ($null -ne $report) 'Replacement did not retain its backup report'
    $reportData = Get-Content -LiteralPath $report.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
    Assert-Condition ((Get-TreeHash (Join-Path $reportData.backup_root 'steps')) -ceq $stepsHash) 'Replacement backup does not match the old skill'
    Assert-Condition ((Get-TreeHash $destination) -ceq $originalTree) 'Replacement did not restore package bytes'

    # Inject after one real move; the actual catch must restore both originals.
    [IO.File]::WriteAllText((Join-Path $destination 'apple-design/local.txt'),'first old bytes',$utf8)
    [IO.File]::WriteAllText((Join-Path $destination 'steps/local.txt'),'second old bytes',$utf8)
    $beforeFailure = Get-TreeHash $destination
    function Move-Item {
        param([string]$LiteralPath,[string]$Destination)
        Microsoft.PowerShell.Management\Move-Item -LiteralPath $LiteralPath -Destination $Destination
        $global:SkillPackageFixtureMoveCount++
        if ($global:SkillPackageFixtureMoveCount -eq 1) { throw 'Injected isolated fixture move failure' }
    }
    try {
        Assert-Refused { & (Join-Path $packageRoot 'scripts/install.ps1') -Install } 'Injected isolated fixture move failure'
    } finally { Remove-Item Function:\Move-Item }
    Assert-Condition ((Get-TreeHash $destination) -ceq $beforeFailure) 'PowerShell caught-error rollback lost original bytes'
    Assert-Condition (-not (Test-Path -LiteralPath (Join-Path $env:CODEX_HOME '.skill-package-install.lock'))) 'PowerShell rollback left a lock'

    Assert-Refused { & (Join-Path $packageRoot 'scripts/inventory.ps1') -DestinationRoot $destination -OutputPath (Join-Path $destination 'inventory.json') } 'outside skill'
    & (Join-Path $packageRoot 'scripts/inventory.ps1') -DestinationRoot $destination -OutputPath (Join-Path $fixture 'inventory.json')
    $inventory = Get-Content -LiteralPath (Join-Path $fixture 'inventory.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    Assert-Condition ($inventory.user_global_found -eq 26) 'Inventory did not discover all 26 personal skills'
    Write-Host "WINDOWS_POWERSHELL_FIXTURES_PASS: host=$($PSVersionTable.PSVersion); parsed=$parsed; temporary profile only"
} finally {
    $env:CODEX_HOME = $oldCodexHome; $env:USERPROFILE = $oldProfile
    $env:PYTHONUTF8 = $oldPythonUtf8
    [Console]::OutputEncoding = $oldOutputEncoding
    Remove-Variable -Name SkillPackageFixtureMoveCount -Scope Global -ErrorAction SilentlyContinue
    if (Test-Path -LiteralPath $fixture) {
        Assert-NoReparse $fixture
        Remove-Item -LiteralPath $fixture -Recurse -Force
    }
}
