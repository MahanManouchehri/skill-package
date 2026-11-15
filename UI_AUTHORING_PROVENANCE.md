# UI authoring tools and frozen relevance oracle

The root `scripts/refresh-google-fonts.py`, `refresh-icon-catalog.py`, `evaluate-relevance.py` and `relevance_metrics.py` are **package development/test utilities**. They are outside every installable `skills/<name>/` snapshot. The installer does not copy them into either live skill root. All 70 tracked files in `skills/ui-ux-pro-max/`, including the existing tests, fixtures, catalog data and runtime scripts, remain byte-identical to `v3.1.0`.

The restored implementations come from [Next Level Builder UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/6ae86f61f520d6ca229d2f40e070410638c908c5), pinned at `6ae86f61f520d6ca229d2f40e070410638c908c5`. Each downloaded source was checked against the commit tree's Git blob SHA and its SHA-256. The upstream MIT notice, copyright 2024 Next Level Builder, is retained verbatim in [LICENSES/ui-ux-pro-max-MIT.txt](LICENSES/ui-ux-pro-max-MIT.txt).

| Upstream path | Package path | Source SHA-256 |
|---|---|---|
| `scripts/refresh-google-fonts.py` | `scripts/refresh-google-fonts.py`, unmodified | `e29e9b19ec69e73214ebe22b2488e1da42e7e30ba75e882e7a7aca336f006a77` |
| `scripts/refresh-icon-catalog.py` | `scripts/refresh-icon-catalog.py`, unmodified | `18b51278d8c2236692aa117325f83d2d1c4b82d513e48a2d9e614d376e033235` |
| `scripts/evaluate-relevance.py` | `scripts/vendor/ui-ux-pro-max/evaluate-relevance.py`, unmodified | `1294b92d3242af84092b37aea7a5a93f7df5cb07721fee36c534de2cdda7703e` |
| `scripts/relevance_metrics.py` | `scripts/relevance_metrics.py`, unmodified | `a5126f734365380b3f3390453f25d2f504a6488c6af0fc88256a9529c02e1547` |
| `LICENSE` | `LICENSES/ui-ux-pro-max-MIT.txt`, unmodified | `738f69dfa83db5c347c678fb9d90e560877059f0de93a327c39001bff92dc014` |

This upstream commit is a source pin for the authoring tools, not a claim that the entire runtime snapshot equals upstream HEAD. Of the 70 tracked UI files, 49 match this commit exactly; the two formerly unimportable test modules, all catalog fixtures and `relevance-cases.json` are among those matches. Existing package runtime customizations and historical threshold/baseline files were preserved. The pristine pinned evaluator, metric helper and existing cases produce the exact frozen `oracleFingerprint`, while the existing runtime/data produce the exact frozen `runtimeFingerprint` when addressed by their original logical `src/...` paths. These checks establish the relevant authoring contracts without replacing current catalogs with upstream data.

The package's `scripts/evaluate-relevance.py` is a small original launcher and import adapter, SHA-256 `665dd38264164312847b67a2d75ecfdba997687159fae35367c608c0d5bbd5c5`. Upstream's frozen runtime fingerprint includes `src/ui-ux-pro-max/...` filenames, and its oracle fingerprint includes the evaluator's own source bytes. Changing its directory constant to `skills/...` would invalidate both approvals despite unchanged grading and runtime behavior. The default launcher therefore creates an ephemeral canonical checkout containing only the pristine evaluator, the actual metric helper, three actual runtime modules, actual CSV data, the three existing relevance fixtures and the retained MIT notice. Every projected file is copied as complete bytes and checked against its source; symlinked inputs are rejected. The real upstream CLI executes with the same interpreter, caller arguments and cwd, then its output and exit status are passed through. The temporary checkout is removed afterwards. No persistent `src/` runtime duplicate is shipped, no line endings are normalized, and no threshold, judgment or approval is rewritten. Imported unit-test APIs execute the real pinned source with this package's runtime bindings.

The unchanged frozen contract is:

- Runtime fingerprint: `0d096d52499c2dd84ef80b2e45a1793bc4ed7c9be8fe5948b08151790959b376`.
- Oracle fingerprint: `02e7226428c64a995ec24ae104ce4d186f5f91bf0f062556e90ef9b0fcb6d67a`.
- Threshold status: `provisional-baseline-regression-gate`, baseline revision `97eb2a2`. Passing preserves that historical regression floor; it does not approve the proposed final quality targets.

The tools use Python's standard library. Catalog tests consume bundled JSON/CSV fixtures and require no token or network. The font tool performs a network request only with explicit `--live`; without `GOOGLE_FONTS_API_KEY`, that mode fails before requesting data. The icon tool and relevance evaluator consume local files. Package verification separately requires the existing PyYAML dependency. Use a detected working Python 3 interpreter; the commands below use `python3`. Set `PYTHONDONTWRITEBYTECODE=1` in the test process environment as well as using `-B`, because the inherited upstream tests launch Python subprocesses.

```bash
python3 -B -m unittest discover -s skills/ui-ux-pro-max/scripts/tests -p 'test_*.py' -v
python3 -B -m unittest discover -s skills/ui-ux-pro-max/scripts/tests -p 'test_catalog_refresh.py' -v
python3 -B -m unittest discover -s tests -p 'test_ui_authoring.py' -v
python3 -B scripts/evaluate-relevance.py
```

On macOS with Python 3.14.2, the exact full UI discovery changed from **132 entries: 130 actual passes plus two failed-import placeholders** to **153 actual tests executed and passed, zero failures, errors or skips**. Restoring imports exposes the original 11 catalog and 12 relevance unit tests; no tests were removed, skipped or weakened. Five additional launcher regression tests pass, covering complete projection byte identity, default strict execution of all 90 relevance cases, changed runtime/CRLF rejection, changed grading-source rejection and replaced-vendor rejection. The default strict CLI passes with the unchanged frozen fingerprints and thresholds. A prior one-line layout-only port's fingerprint failure is retained in evidence as an intermediate failure, not reported as a successful run.

Independent smoke checks cover normal/style and UX search, Laravel and Next.js stack search, unmatched style/stack output, existing programmatic style fallback, and relative/absolute script paths from unrelated Unicode cwd paths. Django is not in the unchanged 22-stack catalog: its explicit stack option is rejected; a separate UX-domain search is verified as a framework-neutral fallback, not Django-specific database coverage. `python3` was available; `python` and Windows `py` were unavailable on this macOS host.

The repository's existing `.gitattributes` contains `* -text`, preserving byte-level catalog/oracle fingerprints across checkout instead of converting LF to CRLF. The regression test deliberately converts a runtime source to CRLF and confirms that the frozen gate rejects the changed bytes. These are macOS/cross-platform fixture checks; they do not establish Windows runtime execution.
