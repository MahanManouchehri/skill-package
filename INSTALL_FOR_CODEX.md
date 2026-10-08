# Install every portable skill in Codex

This package deliberately uses the standard Codex **skill installer**, not a plugin. A new Codex can install every portable skill in one operation from this repository.

## Prompt to give a new Codex

> Install every portable skill from `https://github.com/MahanManouchehri/skill-package`.
> 
> Use your preinstalled `skill-installer`. Read `skills-manifest.json` at the requested ref, select every entry where `installable` is `true`, and install every distinct `physical_path_in_package` in one installer invocation. Use the repository ref I requested, or the latest release tag when none is specified. Verify that the installed count equals `expected_user_global` and start a new chat afterward. Do not copy or install `managed/plugin-skills`, system skills, account settings, credentials, or plugin caches.

The Codex `skill-installer` supports several `--path` values in one invocation. For the current release those are the 16 directories below:

```text
skills/apple-design
skills/architecture-review
skills/compatible-response
skills/db-impact
skills/devil
skills/final-check
skills/full-plan
skills/hand-off
skills/multiple-pov
skills/natural-persian-writing
skills/performance-review
skills/practical-test
skills/regression-check
skills/root-cause
skills/steps
skills/ui-ux-pro-max
```

If any destination skill already exists, stop and report the conflict rather than silently overwriting it. The destination owner can then decide whether to retain, update, or back up that skill. A GitHub URL cannot safely grant a remote repository permission to write to a user's Codex directory merely by being mentioned; the Codex/user must explicitly request the installation and trust the repository.
