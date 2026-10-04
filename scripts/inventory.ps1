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
if($OutputPath){$resolved=[IO.Path]::GetFullPath($OutputPath);Assert-NoReparse $resolved;$json|Set-Content -LiteralPath $resolved -Encoding UTF8;Write-Host "Inventory written: $resolved"}else{$json}
