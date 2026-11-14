"""Executable-helper tests. These are not model routing evaluations."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("skill_eval_runner", Path(__file__).with_name("run.py"))
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def command_event(command, exit_code=0):
    return json.dumps({"type": "item.completed", "item": {"type": "command_execution", "command": command, "exit_code": exit_code}})


class TraceTests(unittest.TestCase):
    def setUp(self):
        self.case = {"id": "S01", "expected_skills": ["steps"], "forbidden_skills": ["load-testing"]}

    def test_missing_output_is_unverified_even_with_zero_exit(self):
        result = runner.assess(self.case, "", "", 0)
        self.assertTrue(result["UNVERIFIED"])
        self.assertIsNone(result["LIVE_BEHAVIOR_PASS"])
        self.assertFalse(result["FAIL"])

    def test_invalid_json_and_nonobject_events_never_pass(self):
        result = runner.assess(self.case, 'not JSON\n[]\n{"item": [1]}\n{"type":"item.completed","item":{"type":"command_execution","command":[]}}', "", 0)
        self.assertEqual(len(result["parse_errors"]), 4)
        self.assertIsNone(result["LIVE_BEHAVIOR_PASS"])

    def test_model_declaration_is_not_a_tool_read_or_behavior_pass(self):
        text = json.dumps({"selected_skills": ["steps"]})
        stdout = json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": text}})
        result = runner.assess(self.case, stdout, "", 0)
        self.assertEqual(result["self_declared_skills"], ["steps"])
        self.assertEqual(result["observed_skill_reads"], [])
        self.assertIsNone(result["LIVE_BEHAVIOR_PASS"])

    def test_real_read_of_forbidden_skill_is_flagged(self):
        stdout = command_event('cat "/tmp/fixture/.agents/skills/load-testing/SKILL.md"')
        result = runner.assess(self.case, stdout, "", 0)
        self.assertTrue(result["FAIL"])
        self.assertEqual(result["forbidden_reads"], ["load-testing"])

    def test_failed_reads_and_printed_command_mentions_are_not_activations(self):
        stdout = "\n".join([
            command_event("cat /tmp/.agents/skills/load-testing/SKILL.md", 1),
            command_event("echo cat /tmp/.agents/skills/load-testing/SKILL.md"),
            command_event("cat README.md"),
        ])
        self.assertEqual(runner.parse_trace(stdout)["observed_skill_reads"], [])

    def test_paths_with_spaces_shell_wrapper_and_sequential_reads(self):
        command = '/bin/zsh -lc \'cd "/tmp/my fixture" && sed -n "1,80p" "/tmp/my fixture/.agents/skills/steps/SKILL.md"\''
        self.assertEqual(runner.parse_trace(command_event(command))["observed_skill_reads"], ["steps"])

    def test_model_unavailable_is_unverified_not_behavior_failure(self):
        error = "The 'gpt-6.1-sol' model is not supported when using Codex with a ChatGPT account."
        result = runner.assess(self.case, '{"type":"error","message":"model_not_found"}', error, 1)
        self.assertTrue(result["UNVERIFIED"])
        self.assertEqual(result["runtime_stderr"], error)
        self.assertFalse(result["FAIL"])

    def test_overlay_config_changes_only_matching_external_user_entries(self):
        fixture = Path("/tmp/eval-fixture")
        skills = [
            {"name": "steps", "scope": "user", "path": "/tmp/user/skills/steps/SKILL.md"},
            {"name": "steps", "scope": "repo", "path": str(fixture / ".agents/skills/steps/SKILL.md")},
            {"name": "unrelated", "scope": "user", "path": "/tmp/user/skills/unrelated/SKILL.md"},
            {"name": "steps", "scope": "system", "path": "/tmp/system/skills/steps/SKILL.md"},
        ]
        self.assertEqual(runner.disabled_overlays({"result": {"data": [{"skills": skills}]}}, fixture, {"steps"}), [{"path": "/tmp/user/skills/steps/SKILL.md", "enabled": False}])

    def test_overlay_argument_is_actual_toml_including_windows_paths(self):
        try:
            import tomllib
        except ImportError:
            self.skipTest("TOML roundtrip uses Python 3.11+ stdlib; runner itself supports 3.10+")
        disabled = [{"path": 'C:\\Users\\Some User\\skills\\steps\\SKILL.md', "enabled": False}]
        self.assertEqual(tomllib.loads(runner.overlay_argument(disabled))["skills"]["config"], disabled)


class FixtureTests(unittest.TestCase):
    def test_owner_bank_has_all_original_ids(self):
        self.assertEqual([case["id"] for case in runner.case_bank()], [f"S{i:02}" for i in range(1, 61)])

    def test_output_inside_package_and_ancestor_are_refused(self):
        for path in (runner.PACKAGE, runner.PACKAGE / "eval-output", runner.PACKAGE.parent):
            with self.assertRaises(ValueError):
                runner.outside_package(path)

    def test_symlink_payload_and_output_are_refused(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            (root / "real").mkdir()
            (root / "alias").symlink_to(root / "real", target_is_directory=True)
            with self.assertRaises(ValueError):
                runner.outside_package(root / "alias/output")
            with self.assertRaises(ValueError):
                runner.tree_files(root)

    def test_snapshot_detects_tamper_and_sensitive_files(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            (root / "SKILL.md").write_text("original")
            before = runner.digest(runner.tree_files(root))
            (root / "SKILL.md").write_text("tampered")
            self.assertNotEqual(before, runner.digest(runner.tree_files(root)))
            (root / ".env").write_text("synthetic")
            with self.assertRaises(ValueError):
                runner.tree_files(root)

    def test_actual_prepare_keeps_original_prompt_and_26_copies(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            package = root / "package"
            (package / "evals").mkdir(parents=True)
            (package / "evals/cases.json").write_text('{"synthetic":"bank fingerprint"}')
            (package / "VERSION").write_text("3.1.0\n")
            for i in range(26):
                skill = package / "skills" / f"skill-{i:02}"
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(f'---\nname: skill-{i:02}\ndescription: "Synthetic test skill"\n---\nBody\n')
            case = {"id": "S01", "prompt": "متن اصلی بدون پاسخ مورد انتظار"}
            with patch.object(runner, "PACKAGE", package), patch.object(runner, "case_bank", return_value=[case]), patch.object(runner.subprocess, "check_output", return_value="fixture-sha\n"):
                out = runner.prepare(root / "prepared")
                self.assertEqual((out / "S01/prompt.txt").read_text(), case["prompt"])
                self.assertEqual(len(list((out / "S01/.agents/skills").iterdir())), 26)
                self.assertNotIn("expected_skills", (out / "S01/available_catalog.json").read_text())
                self.assertTrue((out / "S01/.git").is_dir())
                with self.assertRaises(ValueError):
                    runner.prepare(out)
                (out / "S01/.agents/skills/skill-00/SKILL.md").write_text("tampered")
                with patch.object(runner, "discover") as discover:
                    with self.assertRaises(ValueError):
                        runner.run(out, "S01", "no-model-used")
                    discover.assert_not_called()


if __name__ == "__main__":
    unittest.main()
