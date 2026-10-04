[CmdletBinding()]
param(
    [string]$DestinationRoot = (Join-Path $(if($env:CODEX_HOME){$env:CODEX_HOME}else{Join-Path $env:USERPROFILE '.codex'}) 'skills'),
    [string]$PluginCacheRoot,
    [string]$RuntimeCatalogPath,
    [string]$OutputPath
)
. (Join-Path $PSScriptRoot 'common.ps1')
$m=Assert-PackageIntegrity (Split-Path -Parent $PSScriptRoot)
if(-not $PluginCacheRoot){$PluginCacheRoot=Join-Path (Get-CodexRoot) 'plugins/cache'}
$local=@(Get-LocalCatalog $DestinationRoot -System)
$personal=@($local|Where-Object kind -EQ 'user-global')
$expectedNames=@($m.skills|Where-Object installable|ForEach-Object skill_name)
foreach($skill in $personal){
    $fileRecords=@(Get-TreeFiles $skill.physical_path | ForEach-Object {
        [pscustomobject]@{path=(Get-Relative $skill.physical_path $_.FullName);sha256=(Get-SHA256 $_.FullName);bytes=$_.Length}
    })
    $hash=Get-TreeHash $skill.physical_path
    $expectedEntry=@($m.skills|Where-Object {$_.installable -and $_.skill_name -ceq $skill.skill_name})
    $match=$null;$fileDifferences=@()
    if($expectedEntry.Count -eq 1){
        $match=$hash -ceq $expectedEntry[0].tree_hash_sha256
        $fileDifferences=@(Compare-Object @($expectedEntry[0].files|ForEach-Object path) @($fileRecords|ForEach-Object path))
    }
    $skill|Add-Member -NotePropertyName file_count -NotePropertyValue $fileRecords.Count
    $skill|Add-Member -NotePropertyName files -NotePropertyValue $fileRecords
    $skill|Add-Member -NotePropertyName tree_hash_sha256 -NotePropertyValue $hash
    $skill|Add-Member -NotePropertyName manifest_hash_match -NotePropertyValue $match
    $skill|Add-Member -NotePropertyName file_path_differences -NotePropertyValue $fileDifferences
}
$managed=@(Get-ManagedState $m $PluginCacheRoot $RuntimeCatalogPath)
$cacheEntries=@()
# Cache entries are candidates only. They never count as enabled/available.
if(Test-Path -LiteralPath $PluginCacheRoot){
    foreach($f in Get-TreeFiles $PluginCacheRoot){
        if($f.Name -ne 'SKILL.md'){continue}
        $rel=Get-Relative $PluginCacheRoot $f.FullName;$parts=$rel -split '/'
        if($parts.Count -lt 6 -or $parts[3] -ne 'skills'){continue}
        $md=Get-SkillMetadata $f.FullName
        $cacheEntries+=[pscustomobject]@{catalog_name=($parts[1]+':'+$md.name);provider=$parts[0];plugin=$parts[1];version=$parts[2];physical_path=$f.DirectoryName;status='CACHED ONLY - activation unknown'}
    }
}
$inventory=[pscustomobject]@{schema_version=1;observed_utc=[DateTime]::UtcNow.ToString('o');user_global_expected=$m.expected_user_global;user_global_found=$personal.Count;user_global=$personal;missing=@($expectedNames|Where-Object {$_ -notin @($personal|ForEach-Object skill_name)});extra=@($personal|Where-Object {$_.skill_name -notin $expectedNames});duplicates=@($personal|Group-Object skill_name|Where-Object Count -GT 1|ForEach-Object {[pscustomobject]@{name=$_.Name;count=$_.Count}});system_skills=@($local|Where-Object kind -EQ 'system');plugin_managed_expected=$m.expected_plugin_managed;plugin_managed_available=@($managed|Where-Object available).Count;managed=$managed;plugin_cache_candidates=$cacheEntries}
$json=$inventory|ConvertTo-Json -Depth 15
if($OutputPath){
    $resolved=[IO.Path]::GetFullPath($OutputPath);Assert-NoReparse $resolved
    foreach($protected in @($DestinationRoot,$PluginCacheRoot,(Split-Path -Parent $PSScriptRoot))){
        $protectedFull=[IO.Path]::GetFullPath($protected).TrimEnd('\','/')
        if($resolved -eq $protectedFull -or $resolved.StartsWith($protectedFull+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Inventory output must be outside skill, plugin-cache and package trees.'}
    }
    $json|Set-Content -LiteralPath $resolved -Encoding UTF8;Write-Host "Inventory written: $resolved"
}else{$json}
