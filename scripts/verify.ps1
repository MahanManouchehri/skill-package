[CmdletBinding()]
param(
    [string]$DestinationRoot = (Join-Path $(if($env:CODEX_HOME){$env:CODEX_HOME}else{Join-Path $env:USERPROFILE '.codex'}) 'skills'),
    [string]$PluginCacheRoot,
    [string]$RuntimeCatalogPath,
    [switch]$PackageOnly,
    [switch]$RequireManaged,
    [switch]$PassThru
)
. (Join-Path $PSScriptRoot 'common.ps1')
$packageRoot=Split-Path -Parent $PSScriptRoot
$m=Assert-PackageIntegrity $packageRoot
if ($PackageOnly) { Write-Host 'PASS: package integrity, snapshot hashes, metadata, references and secret scan.'; return }
Assert-NoReparse $DestinationRoot
if (-not $PluginCacheRoot) { $PluginCacheRoot=Join-Path (Get-CodexRoot) 'plugins/cache' }
$catalog=@(Get-LocalCatalog $DestinationRoot)
$missing=0; $mismatch=0; $broken=0; $metadata=0; $verified=0; $installed=0
foreach ($e in $m.skills | Where-Object installable) {
    $root=Get-SafePath $DestinationRoot $e.destination_relative
    if (-not (Test-Path -LiteralPath (Join-Path $root 'SKILL.md') -PathType Leaf)) { $missing++; Write-Host "MISSING: $($e.catalog_name)"; continue }
    $installed++; $ok=$true
    if ((Get-TreeHash $root) -ne $e.tree_hash_sha256) { $mismatch++;$ok=$false;Write-Host "HASH MISMATCH: $($e.catalog_name)" }
    $md=Get-SkillMetadata (Join-Path $root 'SKILL.md')
    if ($md.name -cne $e.skill_name -or $md.description -cne $e.description) {$metadata++;$ok=$false}
    $refs=@(Get-BrokenReferences $root);$broken+=$refs.Count;if($refs.Count){$ok=$false}
    foreach ($f in $e.files) { if (-not (Test-Path -LiteralPath (Get-SafePath $root $f.path) -PathType Leaf)) {$ok=$false} }
    if ($ok) { $verified++ }
}
$duplicates=@($catalog | Group-Object catalog_name | Where-Object Count -GT 1)
$fullPlan=@($catalog | Where-Object skill_name -EQ 'full-plan').Count
$devil=Get-SafePath $DestinationRoot 'devil'
if (Test-Path -LiteralPath (Join-Path $devil 'scripts/validate-skill.ps1')) {
    # Only execute the validator when the complete trusted devil snapshot matches.
    $devilEntry=@($m.skills | Where-Object { $_.installable -and $_.skill_name -eq 'devil' })[0]
    if ((Get-TreeHash $devil) -eq $devilEntry.tree_hash_sha256) { & (Join-Path $devil 'scripts/validate-skill.ps1') -SkillPath $devil | Write-Host }
}
$managed=@(Get-ManagedState $m $PluginCacheRoot $RuntimeCatalogPath)
$activeManaged=@($managed | Where-Object available)
# A managed skill copied manually into the user root is a conflict even when its plugin is unavailable.
$manualManaged=@($catalog | Where-Object { $_.skill_name -in @($m.skills | Where-Object { -not $_.installable } | ForEach-Object skill_name) })
$dupCount=$duplicates.Count+$manualManaged.Count
$systems=@(Get-LocalCatalog $DestinationRoot -System | Where-Object kind -EQ 'system').Count
$result=[pscustomobject]@{ user_global_expected=$m.expected_user_global;user_global_installed=$installed;user_global_verified=$verified;missing=$missing;hash_mismatch=$mismatch;metadata_mismatch=$metadata;broken_references=$broken;full_plan_discoverable_entries=$fullPlan;plugin_managed_expected=$m.expected_plugin_managed;plugin_managed_available=$activeManaged.Count;plugin_capabilities_confirmed=@($managed|Where-Object capabilities_confirmed).Count;system_skills=$systems;unexpected_duplicates=$dupCount;managed=$managed;phase_a_pass=($verified -eq $m.expected_user_global -and $dupCount -eq 0 -and $fullPlan -eq 1);phase_b_pass=($activeManaged.Count -eq $m.expected_plugin_managed -and @($managed|Where-Object capabilities_confirmed).Count -eq $m.expected_plugin_managed) }
Write-Host "USER/GLOBAL EXPECTED: $($result.user_global_expected)"
Write-Host "USER/GLOBAL VERIFIED: $verified"
Write-Host "INSTALLED: $installed | MISSING: $missing | HASH MISMATCH: $mismatch | BROKEN REFERENCES: $broken"
Write-Host "FULL-PLAN DISCOVERABLE ENTRIES: $fullPlan"
Write-Host "PLUGIN-MANAGED EXPECTED: $($result.plugin_managed_expected)"
Write-Host "PLUGIN-MANAGED AVAILABLE: $($activeManaged.Count)"
Write-Host "PLUGIN CAPABILITIES CONFIRMED: $($result.plugin_capabilities_confirmed)"
Write-Host "SYSTEM SKILLS: $systems (informational only)"
Write-Host "UNEXPECTED DUPLICATES: $dupCount"
foreach($entry in $managed){Write-Host "$($entry.catalog_name): $($entry.status)"}
if (-not $result.phase_a_pass) { throw 'FAIL: user/global restore or duplicate verification failed.' }
Write-Host 'PASS: Phase A - personal skills restored and hash-verified.'
if (-not $result.phase_b_pass) {
    Write-Host 'Phase B incomplete: enable the proper plugins/runtime and supply fresh catalog evidence.'
    if ($RequireManaged) { throw 'MISSING RUNTIME/PLUGIN DEPENDENCY: complete environment verification failed.' }
} else { Write-Host 'PASS: Phase B - plugin catalog and capability evidence verified.' }
if ($PassThru) { return $result }
