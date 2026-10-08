# Source audit

Version 2 retains the prior verified snapshot and applies an audited delta from the current disk state: the installed `steps` tree plus the new `hand-off` and `compatible-response` trees. Source directories were read and copied, never moved, deleted, merged, rewritten or regenerated.

## Counts

- Personal/user-global: 16
- Active plugin-managed: 16
- Packaged active entries: 32
- System-managed excluded: 5
- full-plan discoverable entries: 1
- Dangling Markdown relative links observed: 0
- Symlinks/reparse links in selected source trees: 0
- Common secret-pattern candidates in included source files: 0
- Original included skill/support files containing C:\Users\Mahan or C:/Users/Mahan: 0

Plugin-cache files outside the active catalog, including the cached openai-templates examples, are not promoted into the package. They may be reported as cached candidates by inventory.ps1; candidate presence is not activation.

## Version 2 delta

- `steps` is replaced with the currently installed source tree, including `references/deep-workflow.md`.
- `hand-off` is added with its `agents`, `assets`, `references`, and `scripts` resources.
- `compatible-response` is added as a portable user-global presentation skill.
- The prior 14 retained personal skill trees and all 16 plugin-managed snapshots remain content-preserving carry-forwards.

## Pre-existing issues preserved

- `natural-persian-writing`: strict YAML parsing fails due to unquoted punctuation in its description. Current runtime exposes the skill. The bundle preserves the exact bytes and discovered name/description. Verification checks those required fields and exact hashes; it does not claim strict YAML validity.
- `ui-ux-pro-max`: its search commands use `${CLAUDE_PLUGIN_ROOT}/.claude/skills/ui-ux-pro-max/scripts/search.py`. Python 3 and appropriate path resolution are needed on Codex; the source is preserved with PARTIALLY_PORTABLE status.

## Exclusions

- `full-plan/.git/`: Non-behavioral Git/generated/runtime data. All remaining source files are individually hashed and copied byte for byte.
- `ui-ux-pro-max/scripts/__pycache__/`: Non-behavioral Git/generated/runtime data. All remaining source files are individually hashed and copied byte for byte.
- `26.915.20218/skills/presentations/container_tools/__pycache__/`: Non-behavioral Git/generated/runtime data. All remaining source files are individually hashed and copied byte for byte.

The full-plan internal .git directory is history/config/log data, not skill behavior. This exclusion does not modify full-plan or create a variant. Source/package tree equality uses the documented selected-file policy; the raw source tree including .git is intentionally not the distribution tree.

## Provenance and path audit

Absolute source paths recorded in skills-manifest.json/exclusions are intentional audit provenance and harmless to restore portability. They are never executed or used to derive destination paths. Personal payload paths contain no hardcoded source-user paths. Source and package hashes, file records and relative links are preserved in the manifest. Final package provenance-path counts appear in validation-results.json.

## Secret scan boundaries

Source and final package were scanned for common GitHub/OpenAI/AWS keys, private keys, long literal credential assignments and sensitive filenames. No matching candidates were found. Binary content was included in hashing. This is pattern-based evidence, not a claim that every possible secret format can be recognized. No account config, credentials, cookies, sessions, histories or runtime caches were selected. Existing destination backups remain local and are not added to this repository.
