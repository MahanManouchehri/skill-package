[CmdletBinding(DefaultParameterSetName='DryRun')]
param(
    [Parameter(ParameterSetName='DryRun')][switch]$DryRun,
    [Parameter(Mandatory,ParameterSetName='Install')][switch]$Install,
    [string]$DestinationRoot = (Join-Path $(if($env:CODEX_HOME){$env:CODEX_HOME}else{Join-Path $env:USERPROFILE '.codex'}) 'skills'),
    [string]$PluginCacheRoot,
    [string]$RuntimeCatalogPath
)
. (Join-Path $PSScriptRoot 'common.ps1')
$packageRoot=Split-Path -Parent $PSScriptRoot
$m=Assert-PackageIntegrity $packageRoot
$DestinationRoot=[IO.Path]::GetFullPath($DestinationRoot).TrimEnd('\','/')
Assert-NoReparse $DestinationRoot
# Keep the distribution and destination disjoint; never install into source/snapshot/system paths.
$packageFull=[IO.Path]::GetFullPath($packageRoot).TrimEnd('\','/')
if ($DestinationRoot -eq $packageFull -or $DestinationRoot.StartsWith($packageFull+'\',[StringComparison]::OrdinalIgnoreCase) -or $packageFull.StartsWith($DestinationRoot+'\',[StringComparison]::OrdinalIgnoreCase) -or $DestinationRoot -match '[/\\](\.system|plugins|cache)([/\\]|$)') {throw 'Unsafe destination: package, system and plugin cache paths are protected.'}
Assert-NoReparse (Join-Path (Split-Path -Parent $DestinationRoot) 'skills-backup')
$catalog=@(Get-LocalCatalog $DestinationRoot)
$expected=@($m.skills | Where-Object installable)
$conflicts=New-Object Collections.Generic.List[string]
foreach($group in $catalog | Group-Object catalog_name | Where-Object Count -GT 1){$conflicts.Add("Duplicate destination entry: $($group.Name)")}
$managedNames=@($m.skills|Where-Object{-not $_.installable}|ForEach-Object skill_name)
foreach($c in $catalog | Where-Object { $_.skill_name -in $managedNames }){$conflicts.Add("Managed skill in user root: $($c.skill_name)")}
$plan=@()
foreach($e in $expected){
    $dest=Get-SafePath $DestinationRoot $e.destination_relative
    Assert-NoReparse $dest
    foreach($c in $catalog|Where-Object {$_.skill_name -eq $e.skill_name}){if([IO.Path]::GetFullPath($c.physical_path) -ne $dest){$conflicts.Add("Same skill at another physical location: $($e.skill_name)")}}
    $action='INSTALL'
    if(Test-Path -LiteralPath $dest){
        if(-not(Test-Path -LiteralPath $dest -PathType Container)){$conflicts.Add("Destination is not a directory: $($e.destination_relative)")}
        elseif(Test-Path -LiteralPath (Join-Path $dest 'SKILL.md')){
            Assert-TreeNoReparse $dest
            $md=Get-SkillMetadata (Join-Path $dest 'SKILL.md')
            if($md.name -cne $e.skill_name){$conflicts.Add("Different skill occupies destination: $($e.destination_relative)")}
            if((Get-TreeHash $dest) -eq $e.tree_hash_sha256){$action='UNCHANGED'}else{$action='BACKUP THEN REPLACE'}
        }else{$conflicts.Add("Unknown directory occupies destination: $($e.destination_relative)")}
    }
    $plan+=[pscustomobject]@{skill=$e.catalog_name;action=$action;destination=$dest;entry=$e}
    Write-Host "$action : $($e.catalog_name)"
    foreach($tool in $e.required_external_tools){
        if($tool -eq 'Python 3' -and -not(Get-Command python,python3,py -ErrorAction SilentlyContinue)){Write-Host "MISSING TOOL DEPENDENCY: $tool ($($e.catalog_name))"}
    }
    if($e.portability -eq 'PARTIALLY_PORTABLE'){Write-Host "PORTABILITY CONFIGURATION REQUIRED: $($e.catalog_name): $($e.dependencies -join '; ')"}
}
if(-not $PluginCacheRoot){$PluginCacheRoot=Join-Path (Get-CodexRoot) 'plugins/cache'}
foreach($state in Get-ManagedState $m $PluginCacheRoot $RuntimeCatalogPath){Write-Host "$($state.catalog_name): $($state.status)"}
if($conflicts.Count){foreach($c in $conflicts){Write-Host "CONFLICT: $c"};throw 'Resolve catalog/destination conflicts before installation.'}
if(-not $Install){Write-Host 'PASS: DryRun complete. No files or directories changed. Managed snapshots are not installed.';return}
$parent=Split-Path -Parent $DestinationRoot
$stamp=[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')+'-'+[Guid]::NewGuid().ToString('N').Substring(0,8)
$backupRoot=Join-Path (Join-Path $parent 'skills-backup') $stamp
$stageRoot=Join-Path $parent ('.skill-package-stage-'+$stamp)
Assert-NoReparse $parent
Assert-NoReparse $backupRoot
Assert-NoReparse $stageRoot
$lockPath=Join-Path $parent '.skill-package-install.lock'
$lock=$null;$changes=New-Object Collections.Generic.List[object]
try{
    if(-not(Test-Path -LiteralPath $parent)){[void](New-Item -ItemType Directory -Path $parent)}
    Assert-NoReparse $lockPath
    $lock=[IO.File]::Open($lockPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    [void](New-Item -ItemType Directory -Path $stageRoot)
    # Stage and verify everything before touching an existing skill.
    foreach($row in $plan|Where-Object action -NE 'UNCHANGED'){
        $source=Get-SafePath $packageRoot $row.entry.physical_path_in_package
        $stage=Get-SafePath $stageRoot $row.entry.destination_relative
        Copy-Item -LiteralPath $source -Destination $stage -Recurse -Force
        if((Get-TreeHash $stage) -ne $row.entry.tree_hash_sha256){throw "Staging hash failed: $($row.skill)"}
    }
    if(-not(Test-Path -LiteralPath $DestinationRoot)){[void](New-Item -ItemType Directory -Path $DestinationRoot)}
    foreach($row in $plan|Where-Object action -NE 'UNCHANGED'){
        Assert-NoReparse $row.destination
        Assert-TreeNoReparse $row.destination
        $backup=$null
        if(Test-Path -LiteralPath $row.destination){
            $backup=Get-SafePath $backupRoot $row.entry.destination_relative
            Assert-NoReparse $backup
            [void](New-Item -ItemType Directory -Path $backupRoot -Force)
            Copy-Item -LiteralPath $row.destination -Destination $backup -Recurse -Force
            if((Get-TreeHash $backup) -ne (Get-TreeHash $row.destination)){throw "Backup verification failed: $($row.skill)"}
        }
        # Record before removal so a failure during replacement can restore the backup.
        $changes.Add([pscustomobject]@{destination=$row.destination;backup=$backup;skill=$row.skill;action=$row.action})
        if(Test-Path -LiteralPath $row.destination){Remove-Item -LiteralPath $row.destination -Recurse -Force}
        $stage=Get-SafePath $stageRoot $row.entry.destination_relative
        Move-Item -LiteralPath $stage -Destination $row.destination
    }
    & (Join-Path $PSScriptRoot 'verify.ps1') -DestinationRoot $DestinationRoot -PluginCacheRoot $PluginCacheRoot -RuntimeCatalogPath $RuntimeCatalogPath
    $report=[pscustomobject]@{installed_utc=[DateTime]::UtcNow.ToString('o');destination=$DestinationRoot;backup_root=$backupRoot;changes=@($changes.ToArray());managed_snapshots_installed=0}
    if($changes.Count){[void](New-Item -ItemType Directory -Path $backupRoot -Force);$report|ConvertTo-Json -Depth 12|Set-Content -LiteralPath (Join-Path $backupRoot 'install-report.json') -Encoding UTF8}
    Write-Host "PASS: installation complete. Replacements backed up at: $backupRoot"
}catch{
    $failure=$_
    for($i=$changes.Count-1;$i -ge 0;$i--){
        $c=$changes[$i];Assert-TreeNoReparse $c.destination
        if(Test-Path -LiteralPath $c.destination){Remove-Item -LiteralPath $c.destination -Recurse -Force}
        if($c.backup){Assert-TreeNoReparse $c.backup;Copy-Item -LiteralPath $c.backup -Destination $c.destination -Recurse -Force}
    }
    throw $failure
}finally{
    if($lock){$lock.Dispose();if(Test-Path -LiteralPath $lockPath){Remove-Item -LiteralPath $lockPath -Force}}
    if(Test-Path -LiteralPath $stageRoot){
        $stageFull=[IO.Path]::GetFullPath($stageRoot);$parentFull=[IO.Path]::GetFullPath($parent).TrimEnd('\','/')
        if(-not $stageFull.StartsWith($parentFull+'\',[StringComparison]::OrdinalIgnoreCase) -or (Split-Path -Leaf $stageFull) -notlike '.skill-package-stage-*'){throw 'Unsafe staging cleanup path.'}
        Assert-TreeNoReparse $stageFull;Remove-Item -LiteralPath $stageFull -Recurse -Force
    }
}
