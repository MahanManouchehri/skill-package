#!/usr/bin/env python3
"""Run the pinned UI relevance oracle in its canonical development layout.

The package ships runtime files under skills/; the frozen upstream fingerprints
include src/ filenames and the evaluator's own bytes. A temporary, byte-verified
projection preserves that contract without changing runtime files or approvals.
Imports expose the authentic upstream functions for the existing unit tests.
"""

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile

_ENTRYPOINT_PATH = Path(__file__).resolve()
_PACKAGE_ROOT = _ENTRYPOINT_PATH.parents[1]
_RUNTIME_PATH = _PACKAGE_ROOT / "skills/ui-ux-pro-max/scripts"
_UPSTREAM_PATH = _PACKAGE_ROOT / "scripts/vendor/ui-ux-pro-max/evaluate-relevance.py"
_UPSTREAM_SHA256 = "1294b92d3242af84092b37aea7a5a93f7df5cb07721fee36c534de2cdda7703e"
_UPSTREAM_SOURCE = _UPSTREAM_PATH.read_bytes()
if hashlib.sha256(_UPSTREAM_SOURCE).hexdigest() != _UPSTREAM_SHA256:
    raise RuntimeError("Pinned UI relevance evaluator source differs; review its provenance")

# Execute the unmodified source in this module's namespace so its real functions
# observe the ROOT/RUNTIME_DIR/DATA_DIR bindings used by the existing unit tests.
# The oracle's __file__ still identifies the byte-pristine grading source.
sys.path.insert(0, str(_RUNTIME_PATH))
sys.path.insert(0, str(_PACKAGE_ROOT / "scripts"))
_ENTRYPOINT_NAME = __name__
__name__ = "_ui_ux_pro_max_upstream"
__file__ = str(_UPSTREAM_PATH)
exec(compile(_UPSTREAM_SOURCE, str(_UPSTREAM_PATH), "exec"), globals())
__name__ = _ENTRYPOINT_NAME
ROOT = _PACKAGE_ROOT
RUNTIME_DIR = _RUNTIME_PATH
FIXTURE_DIR = RUNTIME_DIR / "tests/fixtures"


def _copy_exact(source, target):
    """Copy only a declared development input and verify its complete bytes."""
    if source.is_symlink() or source.resolve() != source:
        raise ValueError(f"UI authoring input must not be a symlink: {source}")
    content = source.read_bytes()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)
    if target.read_bytes() != content:
        raise OSError(f"UI authoring projection differs from its source: {source}")


def _project_canonical_checkout(destination):
    """Project the grader, helper, runtime inputs and their retained MIT notice."""
    _copy_exact(_PACKAGE_ROOT / "LICENSES/ui-ux-pro-max-MIT.txt", destination / "LICENSE")
    _copy_exact(_UPSTREAM_PATH, destination / "scripts/evaluate-relevance.py")
    _copy_exact(_PACKAGE_ROOT / "scripts/relevance_metrics.py",
                destination / "scripts/relevance_metrics.py")
    runtime = destination / "src/ui-ux-pro-max/scripts"
    for name in ("core.py", "design_system.py", "reasoning_contract.py"):
        _copy_exact(_RUNTIME_PATH / name, runtime / name)
    data = _PACKAGE_ROOT / "skills/ui-ux-pro-max/data"
    for source in sorted(data.rglob("*.csv")):
        _copy_exact(source, destination / "src/ui-ux-pro-max/data" / source.relative_to(data))
    for name in ("relevance-cases.json", "relevance-thresholds.json", "relevance-baseline.json"):
        _copy_exact(FIXTURE_DIR / name, runtime / "tests/fixtures" / name)


def _launch_upstream_cli(arguments=None):
    """Pass through caller arguments, cwd, output and the real grader's status."""
    arguments = sys.argv[1:] if arguments is None else arguments
    with tempfile.TemporaryDirectory(prefix="ui-relevance-") as raw:
        checkout = Path(raw).resolve()
        _project_canonical_checkout(checkout)
        command = [sys.executable, "-B", str(checkout / "scripts/evaluate-relevance.py"),
                   *arguments]
        return subprocess.run(command, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                              check=False).returncode


if __name__ == "__main__":
    try:
        raise SystemExit(_launch_upstream_cli())
    except (OSError, ValueError) as error:
        print(f"evaluate-relevance launcher: {error}", file=sys.stderr)
        raise SystemExit(2) from error
