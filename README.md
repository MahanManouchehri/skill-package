# skill-package v2.2

Private, verifiable snapshot of the current Codex skill environment. The source skills are preserved without behavioral rewrites. This is a file backup and restore bundle, not an account clone.

## Contents

- **16 personal skills** in `skills/<skill-name>/`: installable, content-preserving copies.
- **16 active plugin-managed skill entries** in `managed/plugin-skills/<provider>/<plugin>/<version>/`: audit/reference snapshots only. Full plugin-relative supporting resources are preserved, including resources outside the individual skill folder.
- **5 system skills excluded**: imagegen, openai-docs, review-agent, skill-creator, skill-installer. The destination Codex runtime supplies system skills.
- `skills-manifest.json`: per-file hashes, deterministic skill tree hashes, metadata, dependencies, original physical sources and documented exclusions.
- `package-integrity.json`: hashes for every distribution file except itself. `.git/` is excluded. Hashes detect accidental changes; they are not signatures or independent proof of authenticity.
- `AUDIT.md`, `PORTABILITY.md`, `RESTORE.md`, `VALIDATION.md`: findings, dependencies, practical restore steps and test evidence.

Version 2.2 supersedes the previous 30-entry package: 16 personal + 16 managed = 32. It updates `steps` from the installed source and adds `hand-off` plus `compatible-response`, without rewriting the 14 retained personal skills or the managed snapshots. A new Codex installs every portable skill through its built-in `skill-installer`; the package is not a Plugin or Marketplace. Cached inactive plugins, including artifact-template examples, are not treated as active skills. Original machine paths in manifest provenance identify the audited source; they are never used as installation destinations.

## Portable skills installed in Phase A

The following 16 personal skills are installed into the destination user's global skill directory. The 16 entries under `managed/plugin-skills/` are deliberately excluded from this list because they require their own Plugin or runtime provider.

| Skill | What it does |
|---|---|
| `apple-design` | Guides Apple-inspired interface design, including motion, spatial hierarchy, typography and reduced-motion behavior. Use it for gesture-driven or polished, physical-feeling UI work. |
| `architecture-review` | Independently reviews a concrete system design or implementation plan before coding. It focuses on boundaries, coupling, maintainability and realistic structural risk. |
| `compatible-response` | Shapes user-facing Codex responses for the task at hand and keeps them concise without losing needed information. It applies across projects and other skills. |
| `db-impact` | Maps the full impact of a proposed database or migration change before execution. It covers compatibility, existing data, rollback and downstream dependencies. |
| `devil` | Stress-tests important technical decisions and plans by challenging assumptions, failure modes and reversibility. It is an evidence-based adversarial review, not an implementation skill. |
| `final-check` | Audits completed work against the original request before it is declared finished. It checks requirements, evidence, scope and remaining limitations. |
| `full-plan` | Documents API endpoints and ordered user scenarios in natural Persian before implementing an API-driven feature. It requires explicit confirmation before API-contract changes. |
| `hand-off` | Explains real source code, call paths and feature behavior for developers taking over a project. A full handoff can generate a developer guide and standalone LLM context. |
| `multiple-pov` | Runs a one-time, evidence-first design review before substantial new systems or changes. It surfaces trade-offs and decisions before planning or implementation begins. |
| `natural-persian-writing` | Produces and reviews clear, natural Persian while preserving technical facts and the intended tone. Use it for meaningful Persian prose, documentation and support text. |
| `performance-review` | Reviews recent changes or known workloads for real performance bottlenecks and scalable improvements. It avoids speculative micro-optimization. |
| `practical-test` | Performs strict browser-based acceptance testing for work implemented in the current conversation. It activates only when explicitly requested with `/practical-test`. |
| `regression-check` | Verifies that completed changes preserved important existing behavior within their realistic blast radius. It identifies what must be tested and reports residual uncertainty. |
| `root-cause` | Investigates the actual cause of a bug or unexpected behavior before proposing a fix. It prevents symptom-driven or speculative patching. |
| `steps` | Leads development work by applying governance, setting proportionate workflow and coordinating relevant specialist skills. It tracks criticality, evidence, verification and handoff. |
| `ui-ux-pro-max` | Supplies UI/UX guidance, searchable design data and stack-specific patterns for web, mobile and desktop interfaces. It covers interaction, accessibility, layout, typography and visual systems. |

## Install in Codex

Give a new Codex this exact prompt:

```text
Install every portable skill from https://github.com/MahanManouchehri/skill-package. Use your preinstalled skill-installer: read skills-manifest.json, select every entry with installable: true, and install every physical_path_in_package in one invocation. Verify the installed count equals expected_user_global. Do not install managed/plugin-skills, system skills, credentials, account settings, or plugin caches.
```

Codex will install the 16 directories under `skills/` into its user skill root. It must not install the 16 `managed/plugin-skills` snapshots: those are audit-only and require their original runtime/plugin providers. See [INSTALL_FOR_CODEX.md](INSTALL_FOR_CODEX.md) for the exact contract and current path list. Start a new chat if newly installed skills do not appear immediately.

## Manual restore fallback (Windows)

PowerShell 5.1+ is required. These scripts do not require Python, Git or a GitHub account when using a ZIP. Close any other restore process first. Review the package and choose a trusted snapshot before running code.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1 -PackageOnly
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install.ps1 -Install
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

Destination resolves to `$env:CODEX_HOME\skills` when CODEX_HOME is set, otherwise `$env:USERPROFILE\.codex\skills`. `-DestinationRoot` supports an isolated restore test or a deliberately selected user skill root. Source provenance paths are informational only.

The installer validates the entire bundle and scans for common secret patterns before any install. It defaults to a mutation-free dry-run. Existing different versions are copied to a timestamped sibling `skills-backup/` and verified before replacement. Only manifest-listed personal skill directories can be replaced. Unknown directories, duplicate names, reparse points and system/plugin destinations cause a refusal. Unrelated skills, `.system`, account config and AGENTS.md are untouched. A failed install attempts rollback from verified local backups; backups remain available for manual recovery. An exclusive installation lock prevents concurrent bundle installers.

Managed snapshots are **never** installed into user skills or plugin cache. Runtime and plugin activation use their proper destination mechanisms. Folder existence is not proof of plugin activation or tool availability. `verify.ps1` reports Phase A and Phase B separately; default success covers Phase A only. `-RequireManaged` requires all managed catalog entries and capabilities to be confirmed using fresh external evidence.

## What is excluded

System skills; full-plan's internal `.git` history; generated caches; credentials; auth state; account config; chat/session histories; machine runtime binaries; subscription entitlements. All actual source exclusions are itemized in the manifest. Skill files, relative structure, agents, references, scripts, templates and assets are copied byte for byte. No installer fetches dependencies or enables plugins automatically.

The source `natural-persian-writing` has a pre-existing strict YAML frontmatter defect; its discovered name/description and bytes are preserved. `ui-ux-pro-max` has an existing CLAUDE_PLUGIN_ROOT assumption. See AUDIT.md before expecting identical operation on a new runtime.

For another account or Windows user, use the same Phase A installer followed by Phase B plugin/runtime restoration. Authentication, account permissions, tools and entitlement must be supplied separately. GitHub access is needed only to clone the private repository; an authorized ZIP copy works offline for Phase A.

Sources for the runtime/skill distinction: [OpenAI plugin architecture](https://developers.openai.com/plugins/concepts/plugins), [Build skills](https://learn.chatgpt.com/docs/build-skills).
