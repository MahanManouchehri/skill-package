"""Regression checks for the offline UI authoring entry point and frozen oracle."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "skills/ui-ux-pro-max"
VENDOR = ROOT / "scripts/vendor/ui-ux-pro-max/evaluate-relevance.py"
SPEC = importlib.util.spec_from_file_location(
    "ui_authoring_entrypoint", ROOT / "scripts/evaluate-relevance.py")
entrypoint = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(entrypoint)


class UIAuthoringLauncherTest(unittest.TestCase):
    @staticmethod
    def runtime_inputs():
        return ([UI / "scripts" / name for name in (
            "core.py", "design_system.py", "reasoning_contract.py")]
            + sorted((UI / "data").rglob("*.csv"))
            + [UI / "scripts/tests/fixtures" / name for name in (
                "relevance-cases.json", "relevance-thresholds.json", "relevance-baseline.json")])

    def copy_package(self, destination):
        inputs = self.runtime_inputs() + [VENDOR,
            ROOT / "scripts/evaluate-relevance.py", ROOT / "scripts/relevance_metrics.py",
            ROOT / "LICENSES/ui-ux-pro-max-MIT.txt"]
        for source in inputs:
            target = destination / source.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())

    def run_cli(self, script, cwd, *arguments):
        return subprocess.run(
            [sys.executable, "-B", str(script), *map(str, arguments)], cwd=cwd,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True, text=True, encoding="utf-8", check=False,
        )

    def test_projection_preserves_every_input_byte_and_contains_no_runtime_duplicate(self):
        expected = {
            "LICENSE": ROOT / "LICENSES/ui-ux-pro-max-MIT.txt",
            "scripts/evaluate-relevance.py": VENDOR,
            "scripts/relevance_metrics.py": ROOT / "scripts/relevance_metrics.py",
        }
        expected.update({"src/ui-ux-pro-max/" + path.relative_to(UI).as_posix(): path
                         for path in self.runtime_inputs()})
        with tempfile.TemporaryDirectory() as raw:
            destination = Path(raw).resolve()
            entrypoint._project_canonical_checkout(destination)
            actual = {path.relative_to(destination).as_posix(): path
                      for path in destination.rglob("*") if path.is_file()}
            self.assertEqual(set(expected), set(actual))
            for logical, source in expected.items():
                with self.subTest(path=logical):
                    self.assertEqual(source.read_bytes(), actual[logical].read_bytes())
            self.assertFalse((destination / "skills").exists())

    def test_default_strict_cli_preserves_frozen_fingerprints_from_another_cwd(self):
        with tempfile.TemporaryDirectory(prefix="ui-تست-") as raw:
            directory = Path(raw)
            result = self.run_cli(ROOT / "scripts/evaluate-relevance.py", directory,
                                  "--write-baseline", "relevance report.json")
            self.assertEqual(0, result.returncode, result.stderr)
            report = json.loads((directory / "relevance report.json").read_text(encoding="utf-8"))
            thresholds = json.loads(
                (UI / "scripts/tests/fixtures/relevance-thresholds.json").read_text(encoding="utf-8"))
            self.assertEqual(90, report["samples"]["cases"])
            self.assertEqual(90, len(report["cases"]))
            self.assertEqual(thresholds["runtimeFingerprint"], report["runtimeFingerprint"])
            self.assertEqual(thresholds["oracleFingerprint"], report["oracleFingerprint"])
            self.assertEqual(report["metrics"], json.loads(result.stdout)["metrics"])
            self.assertEqual(["relevance report.json"], sorted(path.name for path in directory.iterdir()))

    def test_runtime_source_or_crlf_changes_remain_rejected_by_the_frozen_gate(self):
        original = (UI / "scripts/core.py").read_bytes()
        changes = {"source": original + b"\n# changed runtime\n",
                   "crlf": original.replace(b"\n", b"\r\n")}
        for label, changed in changes.items():
            with self.subTest(change=label), tempfile.TemporaryDirectory() as raw:
                directory = Path(raw).resolve()
                self.copy_package(directory)
                (directory / "skills/ui-ux-pro-max/scripts/core.py").write_bytes(changed)
                result = self.run_cli(directory / "scripts/evaluate-relevance.py", directory)
                self.assertEqual(1, result.returncode, result.stderr)
                self.assertIn("runtimeFingerprint does not match", result.stderr)
                self.assertNotIn("oracleFingerprint does not match", result.stderr)

    def test_changed_grading_source_remains_rejected_by_the_frozen_gate(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw).resolve()
            self.copy_package(directory)
            helper = directory / "scripts/relevance_metrics.py"
            helper.write_bytes(helper.read_bytes() + b"\n# changed grading source\n")
            result = self.run_cli(directory / "scripts/evaluate-relevance.py", directory)
            self.assertEqual(1, result.returncode, result.stderr)
            self.assertIn("oracleFingerprint does not match", result.stderr)
            self.assertNotIn("runtimeFingerprint does not match", result.stderr)

    def test_replaced_vendor_source_is_rejected_before_execution(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw).resolve()
            self.copy_package(directory)
            source = directory / VENDOR.relative_to(ROOT)
            source.write_bytes(source.read_bytes() + b"\n# replaced pinned source\n")
            result = self.run_cli(directory / "scripts/evaluate-relevance.py", directory)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("Pinned UI relevance evaluator source differs", result.stderr)


if __name__ == "__main__":
    unittest.main()
