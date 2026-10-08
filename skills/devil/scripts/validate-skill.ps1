[CmdletBinding()]
param(
    [Parameter()]
    [string]$SkillPath = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
$required = @(
    'SKILL.md',
    'agents/openai.yaml',
    'references/engineering.md',
    'references/architecture-data.md',
    'references/security-operations.md',
    'references/product-strategy.md',
    'references/decision-debate.md',
    'references/output-format.md'
)

foreach ($relative in $required) {
    $path = Join-Path $SkillPath $relative
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing required skill file: $relative"
    }
}

$skill = Get-Content -Raw -LiteralPath (Join-Path $SkillPath 'SKILL.md')
if ($skill -notmatch '(?s)^---\s*\r?\nname:\s*devil\s*\r?\ndescription:\s*.+?\r?\n---') {
    throw 'SKILL.md frontmatter must declare name: devil and a description.'
}

$yaml = Get-Content -Raw -LiteralPath (Join-Path $SkillPath 'agents/openai.yaml')
if ($yaml -notmatch 'allow_implicit_invocation:\s*true') {
    throw 'Implicit invocation must remain explicitly enabled.'
}
if ($yaml -notmatch 'default_prompt:\s*"Use \$devil') {
    throw 'The default prompt must demonstrate $devil invocation.'
}

$links = [regex]::Matches($skill, '\[[^\]]+\]\((references/[^)]+)\)')
foreach ($link in $links) {
    $target = Join-Path $SkillPath $link.Groups[1].Value
    if (-not (Test-Path -LiteralPath $target -PathType Leaf)) {
        throw "Dead reference in SKILL.md: $($link.Groups[1].Value)"
    }
}

$mustContain = @('Steelman first', 'GO WITH CONDITIONS', 'Do **not** activate implicitly', 'read-only')
foreach ($phrase in $mustContain) {
    if (-not $skill.Contains($phrase)) {
        throw "Missing required behavioral guardrail: $phrase"
    }
}

Write-Output "PASS: devil skill structure, metadata, and references are valid."
