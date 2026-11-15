# Portability and managed capability restoration

Copying files preserves instructions; it does not transfer account eligibility, authentication, tools, browser sessions or runtime software. Version 3.1.0 intentionally upgraded personal instructions; v3.1.1 preserves those payload bytes and upgrades development/verification tooling. Managed rows describe preserved historical snapshots, not current host activation. Current executed host checks are recorded in VALIDATION.md.

| Catalog entry | Kind/status | Dependencies and limitations | Restore / verify |
|---|---|---|---|
| `apple-design` | user-global / PORTABLE | Normal Codex skill support | Phase A installer; content/hash verification |
| `architecture-review` | user-global / PORTABLE | Normal Codex skill support | Phase A installer; content/hash verification |
| `compatible-response` | user-global / PORTABLE | Normal Codex skill support | Phase A installer; content/hash verification |
| `db-impact` | user-global / PORTABLE | Normal Codex skill support | Phase A installer; content/hash verification |
| `devil` | user-global / PORTABLE_WITH_DEPENDENCIES | Standard Codex skill support; PowerShell 5.1+ for optional validator | Phase A installer; content/hash verification |
| `final-check` | user-global / PORTABLE | Normal Codex skill support | Phase A installer; content/hash verification |
| `full-plan` | user-global / PORTABLE | Normal Codex skill support | Phase A installer; content/hash verification |
| `hand-off` | user-global / PORTABLE_WITH_DEPENDENCIES | Standard Codex skill support; Python 3 for the optional handoff structural validator | Phase A installer; content/hash verification |
| `multiple-pov` | user-global / PORTABLE | Normal Codex skill support | Phase A installer; content/hash verification |
| `natural-persian-writing` | user-global / PORTABLE | Normal Codex skill support | Phase A installer; content/hash verification |
| `performance-review` | user-global / PORTABLE | Normal Codex skill support | Phase A installer; content/hash verification |
| `practical-test` | user-global / PORTABLE | Normal Codex skill support | Phase A installer; content/hash verification |
| `regression-check` | user-global / PORTABLE | Normal Codex skill support | Phase A installer; content/hash verification |
| `root-cause` | user-global / PORTABLE | Normal Codex skill support | Phase A installer; content/hash verification |
| `steps` | user-global / PORTABLE | Normal Codex skill support | Phase A installer; content/hash verification |
| `ui-ux-pro-max` | user-global / PORTABLE_WITH_DEPENDENCIES | Python 3 for local search; resolve the actual loaded SKILL.md parent directory | Phase A installer; content/hash verification |
| `integration-reliability` | user-global / PORTABLE | Normal Codex skill support; workflow tools only when requested/available | Verified personal staging/promotion; see skill activation and authority contract |
| `test-engineering` | user-global / PORTABLE | Normal Codex skill support; workflow tools only when requested/available | Verified personal staging/promotion; see skill activation and authority contract |
| `security-assurance` | user-global / PORTABLE | Normal Codex skill support; workflow tools only when requested/available | Verified personal staging/promotion; see skill activation and authority contract |
| `docs-maintenance` | user-global / PORTABLE | Normal Codex skill support; workflow tools only when requested/available | Verified personal staging/promotion; see skill activation and authority contract |
| `maintenance-evolution` | user-global / PORTABLE | Normal Codex skill support; workflow tools only when requested/available | Verified personal staging/promotion; see skill activation and authority contract |
| `skill-evals` | user-global / PORTABLE | Normal Codex skill support; workflow tools only when requested/available | Verified personal staging/promotion; see skill activation and authority contract |
| `load-testing` | user-global / PORTABLE | Normal Codex skill support; workflow tools only when requested/available | Verified personal staging/promotion; see skill activation and authority contract |
| `technical-proposal-discovery` | user-global / PORTABLE | Normal Codex skill support; workflow tools only when requested/available | Verified personal staging/promotion; see skill activation and authority contract |
| `release-management` | user-global / PORTABLE | Normal Codex skill support; workflow tools only when requested/available | Verified personal staging/promotion; see skill activation and authority contract |
| `backup-recovery` | user-global / PORTABLE | Normal Codex skill support; workflow tools only when requested/available | Verified personal staging/promotion; see skill activation and authority contract |
| `computer-use:computer-use` | plugin-managed / RUNTIME_MANAGED | Compatible Windows Computer Use tools/runtime | Enable computer-use via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `computer-use@openai-bundled`. |
| `visualize:visualize` | plugin-managed / RUNTIME_MANAGED | Codex inline visualization runtime; Browser preview when needed; Python 3 for optional browser preview helper | Enable visualize via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `visualize@openai-bundled`. |
| `documents:documents` | plugin-managed / RUNTIME_MANAGED | Bundled document runtime: Python, python-docx, LibreOffice, PDF renderer; Google Drive plugin for native Google Docs; Python 3; Bundled LibreOffice; PDF renderer / Poppler | Enable documents via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `documents@openai-primary-runtime`. |
| `pdf:pdf` | plugin-managed / RUNTIME_MANAGED | Python with reportlab/pdfplumber/pypdf; Poppler pdftoppm; Python 3; Poppler pdftoppm | Enable pdf via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `pdf@openai-primary-runtime`. |
| `presentations:Presentations` | plugin-managed / RUNTIME_MANAGED | Bundled Node.js/Python presentation runtime; Slide renderer; Node.js; Python 3; Bundled slide rendering tools | Enable presentations via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `presentations@openai-primary-runtime`. |
| `spreadsheets:excel-live-control` | plugin-managed / RUNTIME_MANAGED | Bundled spreadsheet artifact runtime; Microsoft Excel + ChatGPT add-in + connected session for excel-live-control; Microsoft Excel; ChatGPT add-in for Excel | Enable spreadsheets via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `spreadsheets@openai-primary-runtime`. |
| `spreadsheets:Spreadsheets` | plugin-managed / RUNTIME_MANAGED | Bundled spreadsheet artifact runtime; Microsoft Excel + ChatGPT add-in + connected session for excel-live-control; Node.js/Python bundled artifact runtime | Enable spreadsheets via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `spreadsheets@openai-primary-runtime`. |
| `template-creator:template-creator` | plugin-managed / RUNTIME_MANAGED | Artifact-template authoring runtime; Source artifact access; relevant artifact plugin; Python 3 for artifact inspection/rendering where required | Enable template-creator via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `template-creator@openai-primary-runtime`. |
| `plugin-management:plugin-management` | plugin-managed / RUNTIME_MANAGED | Plugin Management tools and app permission access | Enable plugin-management via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `plugin-management@openai-curated-remote`. |
| `sites:sites-building` | plugin-managed / RUNTIME_MANAGED | Sites tools; Sites hosting authorization; Node.js/pnpm and compatible preview environment; Node.js; pnpm/npm; Python 3 for applicable helpers | Enable sites via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `sites@openai-curated-remote`. |
| `sites:sites-hosting` | plugin-managed / RUNTIME_MANAGED | Sites tools; Sites hosting authorization; Node.js/pnpm and compatible preview environment; Node.js; pnpm/npm; Python 3 for applicable helpers | Enable sites via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `sites@openai-curated-remote`. |
| `sites:sites-mcp` | plugin-managed / RUNTIME_MANAGED | Sites tools; Sites hosting authorization; Node.js/pnpm and compatible preview environment; Node.js; pnpm/npm; Python 3 for applicable helpers | Enable sites via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `sites@openai-curated-remote`. |
| `sites:sites-preview-troubleshooting` | plugin-managed / RUNTIME_MANAGED | Sites tools; Sites hosting authorization; Node.js/pnpm and compatible preview environment; Node.js; pnpm/npm; Python 3 for applicable helpers | Enable sites via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `sites@openai-curated-remote`. |
| `work-pets:create-pet` | plugin-managed / RUNTIME_MANAGED | ChatGPT Work Pets tools; Image generation and sprite validation runtime; Python 3 for sprite validation/rendering | Enable work-pets via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `work-pets@openai-curated-remote`. |
| `work-pets:pets` | plugin-managed / RUNTIME_MANAGED | ChatGPT Work Pets tools; Image generation and sprite validation runtime; Python 3 for sprite validation/rendering | Enable work-pets via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `work-pets@openai-curated-remote`. |
| `work-pets:update-pet` | plugin-managed / RUNTIME_MANAGED | ChatGPT Work Pets tools; Image generation and sprite validation runtime; Python 3 for sprite validation/rendering | Enable work-pets via proper destination Plugins/runtime mechanism; confirm catalog entry and tools. Candidate identity `work-pets@openai-curated-remote`. |

## Provider identities

Plugin IDs in the manifest are derived from observed provider directory plus manifest name. Plugin name/version/provider are confirmed on disk; full marketplace identifiers are candidate identities and must be checked in the destination UI. Do not assume a copied plugin manifest registers a plugin. No installed account settings are transferred.

The computer-use snapshot preserves sibling docs referenced by ../../docs/. Pets preserve shared references. Other snapshots retain their scripts, templates and assets at the original relative locations. These supporting files are for audit, not runtime installation.

Document, PDF, slide and spreadsheet workflows require their corresponding supported artifact runtime. Dependencies in examples such as /mnt/data are environment-specific example paths and are preserved. The runtime dependency resolver on the destination should identify its own paths. No machine runtime executable or runtime library cache is bundled.

Excel live control additionally requires Microsoft Excel, the ChatGPT add-in, an authenticated connected session, and live workbook tools. The presence of spreadsheets:excel-live-control in a catalog is not evidence of a connected workbook.

Sites and Pets require their actual tools/service capabilities; source instructions cannot recreate hosted services or account access. Plugin Management requires its tools. Visualize requires compatible inline rendering and, where requested, browser preview. Computer Use requires a supported Windows computer-use runtime.

For every managed entry after activation: verify provider identity, active catalog name, actual SKILL.md metadata and required tools. Record version/content differences from the snapshot separately. If unavailable, report MISSING RUNTIME/PLUGIN DEPENDENCY and keep the managed snapshot inactive.

## v3.1 host boundary

All26 personal folders use portable distribution paths. Optional skill helpers retain their real dependencies: Python3 for UI search/handoff validation and PowerShell for the optional devil validator. Package Python tools require PyYAML. No tool/framework/DB server is installed automatically. SQL engine, browser, provider, advisory and infrastructure evidence must come from an actually available authorized environment. A missing capability is UNVERIFIED/BLOCKED for that operation, not an invented pass.

Current native Codex supports both legacy CODEX_HOME/skills and user .agents/skills on the audited host. Inspect actual discovery elsewhere rather than assuming the same roots. Plugin/system snapshots and their historical versions are not upgraded or installed by this task.

## v3.1.1 tooling and runtime evidence

The installable 26-skill payload is byte-identical to v3.1.0. Root UI authoring scripts are development-only and are not copied to live skill roots; see [source pins and MIT license](UI_AUTHORING_PROVENANCE.md). Default authoring tests and relevance grading are offline. Unsupported Django stack selection remains an explicit error; UX-domain search is a documented framework-neutral alternative.

Windows restrictions, Python/PowerShell requirements, safe runner-temp dry runs and observed evidence classes are in [WINDOWS_COMPATIBILITY.md](WINDOWS_COMPATIBILITY.md). The Python tool accepts ordinary absolute drive/UNC spellings subject to native guards; actual SMB/network semantics are unverified. The standalone PowerShell installer accepts only the documented local fixed-drive subset and rejects SUBST/network/UNC mappings. Both refuse extended/device namespaces and ambiguous short aliases. Actual hosted Windows results are linked from current validation, separately from macOS simulations.

Native evaluation requires an explicitly selected model confirmed by an actual turn. An installed model catalog alone is not an entitlement check. The app-bundled CLI can differ from the default shell binary; select it with `--codex` without upgrading or replacing the user's default CLI. Invocation-only overlays leave installed skill/config files intact; the native client may refresh its own runtime cache. No credential files are copied or inspected by the harness.

## Published verification boundary

The [final commit CI](https://github.com/MahanManouchehri/skill-package/actions/runs/43764630393) and [tag CI](https://github.com/MahanManouchehri/skill-package/actions/runs/43765443386) verify release `80ca761864da9134141df432224015390afe8ea6` on Windows Server 2025 with Python 3.12.10 and PowerShell 5.1/7; [closure records](evals/evidence/v3.1.1/publication/README.md) include exact source/tag binding and the owner's NO_REINSTALL_NEEDED observation. Later documentation changes on main do not imply fresh account access, model turns, installed-state refresh or managed capability activation. Native routing remains eight scoped plan PASS, two source-isolation FAIL, two quota-blocked and48 unexecuted cases.
