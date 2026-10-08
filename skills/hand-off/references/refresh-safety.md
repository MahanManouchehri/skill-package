# Refresh, Snapshot and Safe Export Contract

## Snapshot metadata

Include repo identifier/path, branch, HEAD hash if available, analysis date/time + timezone, dirty tree status, scope, important source paths, and how freshness should be rechecked. Dirty Git means this analysis describes the **working tree** and not merely HEAD; don't conceal divergence. A file fingerprint or file list may aid future comparison, but never claim hashes prove semantic behavior.

## REFRESH algorithm

1. Inspect both existing output files and any manually authored sections.
2. Compare current source and saved snapshot via Git diffs and relevant file fingerprints when available. Check uncommitted changes, renames and regenerated files.
3. Re-trace each changed main edge and its callers/consumers; verify unchanged critical paths if evidence is stale/uncertain. Do not trust prior docs as independent source truth.
4. Report added, removed, changed and unresolved routes/symbols/contracts/test coverage.
5. Update only generated content that can be safely replaced. Preserve manual notes, editorial annotations and unrelated files. Prefer manual annotation blocks delimited with `<!-- HAND-OFF:MANUAL:BEGIN -->` and `<!-- HAND-OFF:MANUAL:END -->`; keep any pre-existing unmarked user prose too.
6. On merge conflict or ambiguous ownership, do **not** destructively overwrite. Leave originals and supply a proposed patch/separate candidate copy if user has authorized that artifact.
7. Re-check all important coordinates, repo diff, exported secrets and coverage statuses. Mark unresolved material as `Stale` or `Partial`.

## Security and operational boundaries

- Never execute migrations, seeders, destructive data scripts, production HTTP changes or commands with side effects by default.
- Never quote secrets or sensitive customer data in docs. Sensitive architecture should be summarized minimally and clearly flagged for redaction before external sharing.
- If user asks to export LLM context, explain where disclosure may expose private routes, access controls or business logic. Do not pretend redaction makes material public-safe.
- Do not alter global/project `AGENTS.md`, `compatible-response`, source code, git settings, environment variables or other skills while doing an ordinary handoff. Those are installation concerns only.
