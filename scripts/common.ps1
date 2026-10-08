Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Get-CodexRoot {
    if ($env:CODEX_HOME) { return [IO.Path]::GetFullPath($env:CODEX_HOME) }
    if (-not $env:USERPROFILE) { throw 'USERPROFILE or CODEX_HOME is required.' }
    return Join-Path $env:USERPROFILE '.codex'
}
function Get-SafePath([string]$Root, [string]$Relative) {
    if ([string]::IsNullOrWhiteSpace($Relative) -or [IO.Path]::IsPathRooted($Relative) -or $Relative.Contains(':')) { throw "Invalid relative path: $Relative" }
    $parts = $Relative -split '[/\\]'
    if (@($parts | Where-Object { $_ -in @('..', '.', '', '.system', '.git') }).Count) { throw "Unsafe relative path: $Relative" }
    $base = [IO.Path]::GetFullPath($Root).TrimEnd('\','/')
    $path = [IO.Path]::GetFullPath((Join-Path $base $Relative))
    if (-not $path.StartsWith($base + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw "Path escapes root: $Relative" }
    return $path
}
function Assert-NoReparse([string]$Path) {
    $p = [IO.Path]::GetFullPath($Path)
    while ($p) {
        if (Test-Path -LiteralPath $p) {
            $item = Get-Item -LiteralPath $p -Force
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse point is not allowed: $p" }
        }
        $parent = Split-Path -Parent $p
        if ($parent -eq $p) { break }; $p = $parent
    }
}
function Assert-TreeNoReparse([string]$Root) {
    Assert-NoReparse $Root
    if(-not(Test-Path -LiteralPath $Root -PathType Container)){return}
    foreach($item in Get-ChildItem -LiteralPath $Root -Force){
        if($item.Attributes -band [IO.FileAttributes]::ReparsePoint){throw "Reparse point in replacement/backup tree: $($item.FullName)"}
        if($item.PSIsContainer){Assert-TreeNoReparse $item.FullName}
    }
}
function Get-TreeFiles([string]$Root, [switch]$IncludeGenerated) {
    if (-not (Test-Path -LiteralPath $Root -PathType Container)) { return }
    Assert-NoReparse $Root
    foreach ($item in Get-ChildItem -LiteralPath $Root -Force) {
        if ($item.Name -eq '.git') { continue }
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse point is not allowed: $($item.FullName)" }
        if ($item.PSIsContainer) {
            if (-not $IncludeGenerated -and $item.Name -in @('__pycache__','.pytest_cache','node_modules','.venv','logs','temp','tmp')) { continue }
            Get-TreeFiles $item.FullName -IncludeGenerated:$IncludeGenerated
        } else {
            if (-not $IncludeGenerated -and ($item.Extension -in @('.pyc','.pyo') -or $item.Name -in @('.DS_Store','Thumbs.db'))) { continue }
            $item
        }
    }
}
function Get-Relative([string]$Root, [string]$Path) {
    $base = [IO.Path]::GetFullPath($Root).TrimEnd('\','/') + [IO.Path]::DirectorySeparatorChar
    $full = [IO.Path]::GetFullPath($Path)
    if (-not $full.StartsWith($base,[StringComparison]::OrdinalIgnoreCase)) { throw "Path outside root: $Path" }
    return $full.Substring($base.Length).Replace('\','/')
}
function Get-SHA256([string]$Path) {
    $sha=[Security.Cryptography.SHA256]::Create();$stream=[IO.File]::OpenRead($Path)
    try { return ([BitConverter]::ToString($sha.ComputeHash($stream))).Replace('-','').ToLowerInvariant() }
    finally { $stream.Dispose();$sha.Dispose() }
}
function Get-TextHash([string]$Text) {
    $sha = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($Text)))).Replace('-','').ToLowerInvariant() }
    finally { $sha.Dispose() }
}
function Get-TreeHash([string]$Root) {
    $map = @{}
    foreach ($f in Get-TreeFiles $Root) { $map[(Get-Relative $Root $f.FullName)] = Get-SHA256 $f.FullName }
    [string[]]$keys = @($map.Keys)
    [Array]::Sort($keys, [StringComparer]::Ordinal)
    $sb = New-Object Text.StringBuilder
    foreach ($key in $keys) { [void]$sb.Append($key).Append([char]0).Append($map[$key]).Append("`n") }
    return Get-TextHash $sb.ToString()
}
function Get-SkillMetadata([string]$Path) {
    $text = [IO.File]::ReadAllText($Path)
    $fm = [regex]::Match($text, '(?s)^\uFEFF?---\s*\r?\n(.*?)\r?\n---(?:\s|$)')
    if (-not $fm.Success) { throw "Missing frontmatter: $Path" }
    $name = [regex]::Match($fm.Groups[1].Value, '(?m)^name:\s*([^\r\n]+)')
    $desc = [regex]::Match($fm.Groups[1].Value, '(?m)^description:\s*([^\r\n]+)')
    if (-not $name.Success -or -not $desc.Success) { throw "Missing name/description: $Path" }
    $n = $name.Groups[1].Value.Trim().Trim('"',"'")
    $d = $desc.Groups[1].Value.Trim().Trim('"',"'")
    if ($d -in @('>','|','>-','|-')) {
        $block = [regex]::Match($fm.Groups[1].Value, '(?ms)^description:\s*[>|]-?\s*\r?\n((?:[ \t]+[^\r\n]*(?:\r?\n|$))+)')
        $d = (($block.Groups[1].Value -split '\r?\n' | ForEach-Object { $_.Trim() }) -join ' ').Trim()
    }
    if (-not $n -or -not $d) { throw "Empty metadata: $Path" }
    [pscustomobject]@{ name=$n; description=$d }
}
function Get-LocalCatalog([string]$Root, [switch]$System) {
    if (-not (Test-Path -LiteralPath $Root)) { return }
    foreach ($f in Get-TreeFiles $Root) {
        if ($f.Name -ne 'SKILL.md') { continue }
        $rel = Get-Relative $Root $f.FullName
        if (-not $System -and ($rel -eq '.system/SKILL.md' -or $rel.StartsWith('.system/'))) { continue }
        $md = Get-SkillMetadata $f.FullName
        [pscustomobject]@{ catalog_name=$md.name; skill_name=$md.name; physical_path=$f.DirectoryName; skill_file=$f.FullName; description=$md.description; kind=$(if($rel.StartsWith('.system/')){'system'}else{'user-global'}) }
    }
}
function Get-BrokenReferences([string]$Root, [string]$Boundary=$Root) {
    $boundaryPath = [IO.Path]::GetFullPath($Boundary).TrimEnd('\','/')
    foreach ($f in Get-TreeFiles $Root) {
        if ($f.Extension -ne '.md') { continue }
        $text = [IO.File]::ReadAllText($f.FullName)
        foreach ($m in [regex]::Matches($text,'\[[^\]\r\n]*\]\(([^)\r\n]+)\)')) {
            $ref = ($m.Groups[1].Value.Trim() -split ' "')[0].Trim('<','>')
            $ref = ($ref -split '#')[0]
            if (-not $ref -or $ref -match '^[a-zA-Z][\w+.-]*:' -or $ref -match '^[/\${]') { continue }
            $target = [IO.Path]::GetFullPath((Join-Path $f.DirectoryName $ref))
            $inside = $target -eq $boundaryPath -or $target.StartsWith($boundaryPath + [IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)
            if (-not $inside -or -not (Test-Path -LiteralPath $target)) { [pscustomobject]@{file=$f.FullName;target=$ref;within_boundary=$inside} }
        }
    }
}
function Invoke-SecretScan([string]$Root) {
    $rules = @{
        private_key='-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'
        github_token='\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b'
        openai_key='\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b'
        aws_key='\bAKIA[0-9A-Z]{16}\b'
        credential_assignment='(?i)(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[=:]\s*["''][A-Za-z0-9+/=_-]{24,}["'']'
    }
    foreach ($f in Get-TreeFiles $Root -IncludeGenerated) {
        if ($f.Name -match '(?i)(^\.env($|\.)|^auth\.json$|^credentials($|\.)|^id_(rsa|ed25519)$|\.pfx$|\.p12$|^cookies?($|\.))') {
            [pscustomobject]@{file=(Get-Relative $Root $f.FullName);rule='sensitive_filename'}
        }
        $text = [IO.File]::ReadAllText($f.FullName)
        foreach ($rule in $rules.Keys) {
            if ([regex]::IsMatch($text,$rules[$rule])) { [pscustomobject]@{file=(Get-Relative $Root $f.FullName);rule=$rule} }
        }
    }
}
function Read-Package([string]$PackageRoot) {
    Assert-NoReparse $PackageRoot
    $m = Get-Content -LiteralPath (Join-Path $PackageRoot 'skills-manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($m.schema_version -ne 1) { throw 'Unsupported manifest schema.' }
    $user = @($m.skills | Where-Object installable)
    $managed = @($m.skills | Where-Object { -not $_.installable })
    if ($user.Count -ne $m.expected_user_global -or $managed.Count -ne $m.expected_plugin_managed) { throw 'Manifest counts do not match.' }
    if (@($m.skills | Group-Object catalog_name | Where-Object Count -GT 1).Count) { throw 'Duplicate manifest catalog names.' }
    if (@($user | Group-Object destination_relative | Where-Object Count -GT 1).Count) { throw 'Duplicate destination paths.' }
    if (@($user | Where-Object skill_name -EQ 'full-plan').Count -ne 1) { throw 'Manifest full-plan count must be exactly 1.' }
    foreach ($e in $m.skills) {
        $root = Get-SafePath $PackageRoot $e.physical_path_in_package
        if ($e.installable) {
            if ($e.kind -ne 'user-global' -or $e.physical_path_in_package -ne ('skills/' + $e.destination_relative)) { throw 'Invalid installable mapping.' }
            if ($e.destination_relative -notmatch '^[a-zA-Z0-9][a-zA-Z0-9_-]*$' -or $e.skill_name -in $m.system_skills_excluded) { throw 'Unsafe/system skill destination.' }
        } elseif ($e.kind -ne 'plugin-managed' -or -not $e.physical_path_in_package.StartsWith('managed/plugin-skills/')) { throw 'Invalid managed snapshot mapping.' }
        if ($e.tree_hash_sha256 -notmatch '^[a-f0-9]{64}$' -or $e.file_count -ne @($e.files).Count) { throw 'Invalid manifest file metadata.' }
        $seen = @{}
        foreach ($f in $e.files) {
            [void](Get-SafePath $root $f.path)
            if ($seen.ContainsKey($f.path.ToLowerInvariant())) { throw 'Duplicate manifest file path.' }
            $seen[$f.path.ToLowerInvariant()]=$true
            if ($f.sha256 -notmatch '^[a-f0-9]{64}$') { throw 'Invalid file hash.' }
        }
    }
    return $m
}
function Assert-PackageIntegrity([string]$PackageRoot) {
    $m = Read-Package $PackageRoot
    $ip = Join-Path $PackageRoot 'package-integrity.json'
    $integrity = Get-Content -LiteralPath $ip -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($integrity.schema_version -ne 1) { throw 'Unsupported integrity schema.' }
    $expected=@{}; [string[]]$paths=@($integrity.files | ForEach-Object { $_.path }); [Array]::Sort($paths,[StringComparer]::Ordinal)
    $byPath=@{};foreach($f in $integrity.files){
        if ($byPath.ContainsKey($f.path.ToLowerInvariant())) { throw 'Duplicate integrity file.' }
        $byPath[$f.path.ToLowerInvariant()]=$f
    }
    $sb=New-Object Text.StringBuilder
    foreach ($path in $paths) {
        $f=$byPath[$path.ToLowerInvariant()]; $p=Get-SafePath $PackageRoot $path
        if (-not (Test-Path -LiteralPath $p -PathType Leaf) -or (Get-SHA256 $p) -ne $f.sha256) { throw "Package integrity mismatch: $path" }
        $expected[$path.ToLowerInvariant()]=$true
        [void]$sb.Append($path).Append([char]0).Append($f.sha256).Append("`n")
    }
    if ((Get-TextHash $sb.ToString()) -ne $integrity.package_tree_hash_sha256) { throw 'Package aggregate hash mismatch.' }
    foreach ($f in Get-TreeFiles $PackageRoot -IncludeGenerated) {
        $path=Get-Relative $PackageRoot $f.FullName
        if ($path -ne 'package-integrity.json' -and -not $expected.ContainsKey($path.ToLowerInvariant())) { throw "Unexpected package file: $path" }
    }
    $secrets=@(Invoke-SecretScan $PackageRoot)
    if ($secrets.Count) { throw ('Secret/sensitive candidates detected: '+ (($secrets | ForEach-Object { $_.file+':'+$_.rule }) -join ', ')) }
    foreach ($e in $m.skills) {
        $root=Get-SafePath $PackageRoot $e.physical_path_in_package
        if ((Get-TreeHash $root) -ne $e.tree_hash_sha256) { throw "Skill snapshot hash mismatch: $($e.catalog_name)" }
        $md=Get-SkillMetadata (Join-Path $root 'SKILL.md')
        if ($md.name -ne $e.skill_name -or $md.description -ne $e.description) { throw "Skill metadata mismatch: $($e.catalog_name)" }
        $boundary=Get-SafePath $PackageRoot $e.snapshot_root
        if (@(Get-BrokenReferences $root $boundary).Count) { throw "Broken snapshot reference: $($e.catalog_name)" }
    }
    return $m
}
function Get-ManagedState($Manifest, [string]$PluginCacheRoot, [string]$RuntimeCatalogPath) {
    $evidence=@()
    if ($RuntimeCatalogPath) {
        $ev=Get-Content -LiteralPath $RuntimeCatalogPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($ev.schema_version -ne 1 -or -not $ev.observed_utc -or -not $ev.evidence_source) { throw 'Runtime catalog needs schema_version, observed_utc and evidence_source.' }
        $observed=[DateTimeOffset]::MinValue
        if(-not [DateTimeOffset]::TryParse($ev.observed_utc,[ref]$observed) -or $observed -lt [DateTimeOffset]::UtcNow.AddDays(-1) -or $observed -gt [DateTimeOffset]::UtcNow.AddMinutes(5)){throw 'Runtime evidence must be a valid observation from the last 24 hours (no future dates).'}
        $evidence=@($ev.entries)
        if (@($evidence | Group-Object catalog_name | Where-Object Count -GT 1).Count) { throw 'Duplicate entries in supplied runtime catalog.' }
    }
    foreach ($e in $Manifest.skills | Where-Object { -not $_.installable }) {
        $entry=@($evidence | Where-Object { $_.catalog_name -ceq $e.catalog_name -and $_.plugin_name -ceq $e.plugin_name })
        $available=$false; $toolConfirmed=$false; $physical=$null; $status='MISSING RUNTIME/PLUGIN DEPENDENCY'; $hashStatus='NOT_CHECKED'
        if ($entry.Count -eq 1 -and $entry[0].enabled -eq $true) {
            $physical=[IO.Path]::GetFullPath($entry[0].physical_path)
            $cache=[IO.Path]::GetFullPath($PluginCacheRoot).TrimEnd('\','/')
            if (-not $physical.StartsWith($cache+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)) { throw "Managed evidence is outside plugin cache: $($e.catalog_name)" }
            Assert-NoReparse $physical
            $skillFile=Join-Path $physical 'SKILL.md'
            if (Test-Path -LiteralPath $skillFile -PathType Leaf) {
                $md=Get-SkillMetadata $skillFile
                if ($md.name -ceq $e.skill_name) {
                    # Verify the provider/plugin/version/skills layout and plugin identity.
                    $relative=Get-Relative $PluginCacheRoot $physical; $parts=$relative -split '/'
                    if ($parts.Count -ge 5 -and $parts[0] -ceq $e.plugin_provider -and $parts[1] -ceq $e.plugin_name -and $parts[3] -ceq 'skills') {
                        $available=$true; $toolConfirmed=$entry[0].capabilities_confirmed -eq $true
                        $status=$(if($toolConfirmed){'AVAILABLE (caller-supplied runtime evidence)'}else{'CATALOG AVAILABLE; RUNTIME CAPABILITY UNVERIFIED'})
                        $hashStatus=$(if((Get-TreeHash $physical) -eq $e.tree_hash_sha256){'MATCH'}else{'VERSION/CONTENT DIFFERENT - inspect current provider version'})
                    }
                }
            }
        }
        [pscustomobject]@{catalog_name=$e.catalog_name;plugin_id=$e.plugin_id;available=$available;capabilities_confirmed=$toolConfirmed;status=$status;physical_path=$physical;snapshot_hash_status=$hashStatus;dependencies=$e.dependencies}
    }
}
