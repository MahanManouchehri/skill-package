# Validation evidence

## Scope

This report verifies backup/distribution preparation and isolated restore logic. It does not claim that another account has been restored or that entitlement-dependent capabilities work on that account. All restore mutations used isolated work/test directories, never the source skill root. Source verification was read-only.

## Results

- 52 executed checks passed.
- 14/14 personal skill entries restored and hash-verified in isolated destinations.
- 16 managed entries snapshot/hash-verified; zero managed skill copies installed in the default user root.
- 24 complete snapshot roots (14 personal + 10 plugins) compared with source selected-file trees; all 541 included source/support files identical.
- Source catalog/disk corroboration: personal 14, managed 16, systems 5, unexpected duplicates 0. Required runtime capabilities were not independently exercised.
- full-plan has exactly one discoverable entry. No merge or rewrite performed.
- devil validator passed in the packaged/restored copies; all nine files preserved.
- steps SKILL.md and deep-workflow reference preserved; references and hashes passed.
- 0 broken Markdown relative links, 0 agent YAML parse issues, 0 original payload hardcoded source-user paths, 0 common secret-pattern candidates.
- The pre-existing natural-persian-writing strict YAML issue and ui-ux-pro-max platform path assumption remain documented.

| Test | Result |
|---|---|
| package validation PowerShell 5.1 | PASS |
| dry run new user | PASS |
| dry run has zero filesystem mutations | PASS |
| isolated restore | PASS |
| personal restore verification | PASS |
| managed snapshots not installed | PASS |
| strict managed verification without evidence fails | PASS |
| repeat install is idempotent | PASS |
| tampered destination fails hash verification | PASS |
| replacement dry run | PASS |
| replacement dry run zero mutation | PASS |
| replacement with backup | PASS |
| original destination bytes backed up | PASS |
| unrelated and system content preserved | PASS |
| inventory source and extras | PASS |
| inventory extra detection | PASS |
| full-plan duplicate verifier refusal | PASS |
| duplicate dry run refusal | PASS |
| managed manual copy refusal | PASS |
| protected system destination refusal | PASS |
| protected package destination refusal | PASS |
| path traversal refusal | PASS |
| reparse point refusal | PASS |
| concurrent installer lock refusal | PASS |
| other installer lock preserved | PASS |
| managed cache alone never means available | PASS |
| synthetic managed catalog evidence success | PASS |
| managed user-root evidence refused | PASS |
| tampered distribution refused | PASS |
| tampered package zero destination writes | PASS |
| secret scanner negative fixture | PASS |
| final scripts package validation | PASS |
| final scripts clean restore | PASS |
| final scripts dry run | PASS |
| final scripts clean verification | PASS |
| nested excluded git reparse refusal | PASS |
| installer refuses nested git junction | PASS |
| nested junction rejection preserves external data | PASS |
| create backup junction fixture | PASS |
| backup junction refused in dry run | PASS |
| backup junction refused in install | PASS |
| backup junction rejection no writes | PASS |
| forced post-install failure | PASS |
| rollback restores original exact bytes | PASS |
| rollback retains verified backup | PASS |
| rollback cleans staging and owned lock | PASS |
| stale runtime catalog refused | PASS |
| final inventory physical file audit | PASS |
| inventory all 14 hashes and physical file records match | PASS |
| inventory cannot overwrite package payload | PASS |
| inventory cannot overwrite skill payload | PASS |
| inventory protection preserves payload bytes | PASS |

Managed-catalog success in synthetic fixtures tests the verifier logic only. It is not second-account evidence. Default Phase A verification intentionally reports unavailable managed dependencies without declaring full environment restoration complete; -RequireManaged fails until all required catalog and capability evidence is provided. Runtime evidence must be observed within the last 24 hours and refreshed when the environment changes.

# Regression Check

## Verdict

PASS

This verdict applies only to regression safety within the verified scope.

## Change Summary

Created a separate distribution folder and restore tools; original skill content and source environment were preserved.

## Regression Risk

LOW — source files were only read; installer mutations were exercised in isolated fixtures.

## Regression Surface

Personal skill bytes and progressive-disclosure structure; full-plan uniqueness; system/unrelated destination preservation; managed/user separation; backup/rollback.

## Dependency Findings

Runtime tools/plugins are separate dependencies. ui-ux-pro-max retains its existing platform assumption. natural-persian-writing retains its pre-existing strict YAML defect.

## Protected Existing Behaviors

No source rewrites, merges, moves or deletions. Full original relative structure retained except explicit Git/generated-cache exclusions.

## Checks Performed

| Area | Verification | Result | Evidence |
|---|---|---|---|
| Source preservation | Selected-file hashes for all roots | PASS | Manifest snapshot_trees |
| Restore preservation | 14 personal trees and references | PASS | Isolated restore tests |
| System/unrelated skills | Sentinel fixtures unchanged | PASS | Tests |
| Backup and rollback | Original bytes recovered after forced failure | PASS | Tests |
| Managed separation | No snapshot installed as user skill | PASS | Tests |

## Confirmed Regressions

No confirmed regressions found within the verified scope.

## Potential Risks

Destination runtime discovery or capability behavior may differ. Existing source YAML/path issues can affect a different runtime and are explicitly preserved.

## Pre-Existing / Unrelated Failures

natural-persian-writing strict YAML parsing issue; ui-ux-pro-max CLAUDE_PLUGIN_ROOT assumption.

## Unverified Areas

Actual second-account live catalog/tool behavior and account eligibility.

## Residual Risk

LOW for distribution integrity and Phase A file restoration; runtime activation must be verified at the destination.

## Governance

Original source and AGENTS.md untouched. Tests never installed into the real skill root. Publication is separately authorized by the user and private-only.

## Final Assessment

No regressions were found within the verified scope. Critical and high-risk affected behaviors passed the performed checks.
