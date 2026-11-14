# RELEASE, GIT, INSTALLATION AND ACCEPTANCE CONTRACT

**Approved for this skill-package task only.** The owner requires complete execution: create/upgrade, test, **commit**, **push to the owned GitHub repository**, **install the v3-compatible personal skills on the same Codex instance**, verify and report. Merely generating a plan, pull request draft, or download instructions is NOT the requested final outcome when actual tools/permissions allow execution.

## 1. Release identifiers

| Field | Required evidence |
|---|---|
| Repository | Existing `MahanManouchehri/skill-package`, verified canonical remote |
| Baseline | Actual working branch, current commit SHA, `VERSION`, counts, modified/untracked paths |
| Destination version | Prefer `3.1.0` if unpublished and compatible; else next valid compatible v3 release |
| Installable skills | Exactly 26 unique personal entries if 10 added to 16 originals; all contain `SKILL.md` |
| Managed skills | Preserve existing 16 plugin-managed snapshots; NOT copied into personal install root |
| System skills | Excluded from package personal skills; do not modify them |
| Source of install | Immutable published Git commit SHA/tag resolving to same commit |
| Destination | Actual active per-user Codex skills root, not assumed external user's machine |

**Version/tag conflict:** query actual current tag/release state. Do not retag, force-update tags, or force push. If any changes break v3-compatible contracts, stop release and explain needed redesign or major-version decision.

## 2. Gates and their minimum evidence

| Gate | PASS evidence | If not met |
|---|---|---|
| G0 — Repository/governance | Correct owner/repo, applicable AGENTS.md, authorized edit paths, protected dirty work and correct Git remote | No mutations; `BLOCKED` |
| G1 — Scope implementation | All 10 new skills, 16 old names maintained, approved contracts and activation boundaries | Fix before package/release |
| G2 — Structural integrity | Strict valid YAML, 26 unique SKILL.md, links/resources, deterministic hashes, manifest consistency, secret scan | Critical blocker; fix |
| G3 — Executed test evidence | Actual outputs of relevant old/new validators, fixture install/upgrade/rollback/tamper tests; runtime routing traces where supported | Mark unverified; assess severity honestly; no fabricated PASS |
| G4 — Documentation/distribution | VERSION, manifest/integrity, README/install/restore/validation/portability/audit, scripts synchronized | Fix before commit |
| G5 — Git publication | Scoped commit, verified push and remote SHA; approved tag if used | `PR_PENDING` or `BLOCKED`, not published |
| G6 — Staged install | Official installer or equivalent in isolated temp target at exact ref; all 26 hashes valid | Do not modify live skill root |
| G7 — Live user-skill upgrade | Backup 16 prior entries as applicable, safe installation/promotion, 26 postinstall hash checks, unrelated unchanged, rollback-tested | Roll back and report `BLOCKED` |
| G8 — Final audit | Git SHA, version, paths, metrics and limitations all current; no unsupported claim | `NOT_DONE` / `DONE_WITH_LIMITATIONS` appropriately |

## 3. Structural checks (minimum)

- Parse all SKILL.md YAML frontmatter with a strict parser; `name` and `description` type/format valid, names unique and matched to directory unless a verified existing policy permits difference. Repair known legacy issue in `natural-persian-writing`.
- Paths and links remain inside allowed skill subtree; no symlinks/reparse path escapes, broken Markdown relative links, missing referenced scripts/templates/assets.
- Run scripts/fixtures against a copy or read-only staging where possible. Do not report historical baseline tests as freshly executed.
- Ensure `ui-ux-pro-max` search commands work with real installed paths without relying on `${CLAUDE_PLUGIN_ROOT}` (unless a runtime explicitly supplies it); preserve its data/scripts and run focused tests.
- Verify all personal directory and file hashes against regenerated manifest; verify `package-integrity.json` with existing package rules; detect one deliberately tampered fixture.
- Secret scan source, new scripts, configs and release diff. Scanning for obvious patterns does not guarantee no leaks—inspect manually as feasible.
- Validate `skills-manifest.json` schema fields and expected counts, `INSTALL_FOR_CODEX.md` with current actual commands and `validation-results.json` timestamped accurately.
- For real behavioral routing, use a permitted Codex harness or actual isolated model runs; record positive and negative activations. No local grep mock labeled behavioral PASS.

## 4. Git publication: permitted and forbidden actions

**Permitted within this user's request:** edit the skill-package repo, add necessary tests/scripts/docs, create commits, push to verified owned GitHub remote, create an unused release tag under established repo policy, and install personal package skills after all gates.

**Forbidden even under this request:** force push, dangerous reset/clean, removing unrelated user changes, pushing a different repository, bypassing branch protections, replacing old Git history, deploy to other projects, dumping credentials, modifying system/plugin skill caches, changing unrelated `AGENTS.md`, running load/stress against production, changing production DBs, or installing cron/service on company servers.

If `main` is protected, prefer safe feature branch and PR. Merge only if policy/capability permits. A pushed feature branch/PR is not equivalent to published main release. If merge blocked, report `PR_PENDING` and do not claim that the final release is installed from official main. Do not use silent workarounds.

## 5. Safe installation plan and rollback

The official `skill-installer` currently supports multi-`--path` installation from GitHub and refuses existing destination folders. Its behavior must be **checked locally** before use. Accordingly:

1. Identify real active `$CODEX_HOME/skills` (or documented equivalent for current environment). Inspect symlinks/duplicates/overlays and detect if the environment is remote/cloud rather than owner's computer.
2. Verify target install source is exactly the **published SHA**, not an unreviewed local checkout or floating `main`; validate source checksum tree.
3. Use a clean staging temp destination with the available native installer (or documented equivalent). For 26 paths, pass all `skills/<name>` paths. If native installer has different CLI options, inspect its help/source; do not guess.
4. Validate all staged folders and hashes. Prepare a **tested promotion/rollback algorithm** for all existing personal skill folders. Backup existing entries to a timestamped, user-readable root outside system/plugin directories. Reject unexpected path ownership/unsafe symlinks. Handle crashes/partial writes with a journal/lock or equivalent safe mechanism.
5. Snapshot/update only the 26 approved names, not the entire skill root. If local modifications conflict and cannot be reconciled safely, preserve backup and surface a targeted blocker rather than deleting custom work.
6. Promote clean verified staged directories. Ensure complete exact tree hash match to release manifest and no extraneous stale managed caches. Protect permissions where meaningful. Remove any staging work only if clearly owned and safe.
7. Deliberately exercise simulated failure/rollback **in an isolated fixture**, then inspect actual installation result. On failure, restore all prior backed-up entries, verify restoration and report errors instead of leaving a partial installation.
8. Report installed path, count, hashes, backup location, whether actual Codex runtime discovers new skills and whether a new session/restart is needed. A modified filesystem is not proof that the current session has hot reloaded skills.

**Special rule:** if the Codex session can edit GitHub but cannot reach the actual local/user Codex skill directory, remote publication may succeed but local install MUST be `BLOCKED` with truthful next action. Do not claim a local install happened on the user's machine.

## 6. Release quality philosophy

- Do not halt development for unneeded approval when within agreed scope; do stop genuinely restricted operations.
- Preserve performance for trivial tasks: new skills must not cause full security, architecture, release or stress workflows on every request.
- Have at least one actual executed tool/integration check per newly introduced executable helper (if any), and enough behavioral evaluation to substantiate critical routing claims. If no evaluation execution capability exists, produce runnable test cases, mark behavioral checks `UNVERIFIED`, and call out the confidence/release implication. If a critical safety invariant is unverified, do not certify the release as fully verified.
- A `PASS` needs source/check command + result + revision/time. Document test environment (local/test/staging) precisely; success on local is not a production guarantee.
- Prefer small maintainable specialist instructions, lazy loaded references and avoiding tools/frameworks forced onto unrelated projects.

## 7. Final report template (Persian)

```markdown
# Skill Package — نتیجه اجرای نسخه <resolved-version>

## GitHub
- Repository / Branch / Remote verified:
- Published commit SHA:
- Tag / PR status:
- GitHub published URL:

## Changes
- New skills: (10 list)
- Upgraded existing skills: (16 list or any justified exceptions)
- Managed/system snapshots: untouched / deviations with evidence
- Version and manifest count:

## Tests and evaluations
- Structural: exact commands, counts and verdicts
- Script/integration: exact commands and verdicts
- Behavioral: tested scenario IDs, observed model/agent traces; PASS/FAIL/UNVERIFIED
- Known blockers, unsupported claims rejected:

## Codex installation
- Actual environment and destination:
- Source SHA pinned:
- Backup path and verified content:
- Installation state (26/26 / partial rolled back / blocked):
- Post-install hash verification:
- Codex discovery/refresh requirement:

## Final verdict
- DONE | DONE_WITH_LIMITATIONS | BLOCKED | NOT_DONE
- Remaining steps requiring owner action (if any):
```

## 8. Source references to confirm in environment

- Existing repository: `https://github.com/MahanManouchehri/skill-package`
- Existing local `README.md`, `INSTALL_FOR_CODEX.md`, `VALIDATION.md`, `RESTORE.md` and `scripts/` are canonical for current distribution mechanics; check versions before editing.
- Codex's locally installed system `skill-creator` and `skill-installer` instructions are primary for their CURRENT runtime. Do not assume every installation is the same or that a remote GitHub link installs automatically.
- GitHub web confirmation and remote Git SHA are authoritative for publication, not a successful local `git commit` message.
