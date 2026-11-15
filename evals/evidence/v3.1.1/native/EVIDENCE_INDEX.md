# Published native evidence paths

Reviewer raw pointers use the original local `fixtures/native-runs/<timestamp>/<case>/...` layout. In this published directory, the same bytes are under `cases/<timestamp>/<case>/...`, or `initial-harness-attempts/<timestamp>/<case>/...` for the four early nested-seatbelt attempts. JSON review records preserve the original absolute locations and file hashes; this mapping does not change the reviewed content.

`tool-smoke.*` and the first `app-smoke.*` are under `diagnosis/`. `auth-status.json` is retained here as well as in `diagnosis/` for the reviewer-relative pointer. Bundled model catalogs stay in the owner's local work directory; `models-catalog-summary.json` preserves raw digests and discovered slugs without distributing model instruction bodies. Successful final smoke raw output is `preflight-final/stdout.jsonl`.

Review verdicts are in `reviewer/independent-native-review.*`. Automatic raw result files predate the final external-read detector and are not retroactively rewritten. Use the reviewer verdict for strict source-isolation failures S07/S12. The corrected harness has unit coverage and no new live rerun after the account usage cap.

Native help outputs containing terminal padding are stored in lossless `*-help.txt.json` envelopes (`text` plus original byte SHA256), so Git whitespace validation remains meaningful without trimming captured help. Original raw help files remain in the local work directory. Model-turn stdout/stderr JSONL/text are unchanged.
