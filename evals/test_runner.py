"""Executable-helper tests. These are not model routing evaluations."""
import importlib.util
import json
import tempfile
import unittest
import sys
import time
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


class IsolationTests(unittest.TestCase):
    def test_run_detects_fixture_mutation_after_returning_from_the_runtime(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            package = root / "package"
            (package / "evals").mkdir(parents=True)
            (package / "evals/cases.json").write_text("synthetic bank")
            (package / "VERSION").write_text("3.1.1")
            for i in range(26):
                folder = package / "skills" / f"skill-{i:02}"
                folder.mkdir(parents=True)
                (folder / "SKILL.md").write_text(f'---\nname: skill-{i:02}\ndescription: "Synthetic"\n---\nBody\n')
            case = {"id": "S01", "prompt": "readonly", "expected_skills": [], "forbidden_skills": []}
            with patch.object(runner, "PACKAGE", package), patch.object(runner, "case_bank", return_value=[case]), patch.object(runner.subprocess, "check_output", return_value="fixture-sha\n"):
                prepared = runner.prepare(root / "prepared")
                fixture = prepared / "S01"
                catalog = {"result": {"data": [{"skills": [{"name": f"skill-{i:02}", "path": str(fixture / ".agents/skills" / f"skill-{i:02}" / "SKILL.md"), "enabled": True} for i in range(26)]}]}}
                def modified_runtime(*args):
                    (fixture / "NOTES.md").write_text("unexpected change")
                    return '{"type":"turn.completed"}', "", 0
                with patch.object(runner, "discover", return_value=catalog), patch.object(runner, "invoke", side_effect=modified_runtime), patch.object(runner.platform, "platform", return_value="synthetic-test-host"):
                    report = runner.run(prepared, "S01", "unit-test-only")
                self.assertTrue(report["FAIL"])
                self.assertEqual(report["fixture_changed_paths"], ["NOTES.md"])
                self.assertEqual(report["fixture_integrity_after"], "FAIL")

    def test_host_skill_reads_fail_source_isolation_even_with_a_correct_name(self):
        fixture = Path(tempfile.gettempdir()).resolve() / "fixture"
        case = {"id": "S01", "expected_skills": ["steps"], "forbidden_skills": []}
        for raw in (str(fixture.parent / "host/.agents/skills/steps/SKILL.md"), "../host/.agents/skills/steps/SKILL.md"):
            report = runner.assess(case, command_event('cat ' + json.dumps(raw)), "", 0, fixture)
            self.assertTrue(report["FAIL"])
            self.assertEqual(report["external_skill_reads"], [raw])
        raw = str(fixture / ".agents/skills/steps/SKILL.md")
        report = runner.assess(case, command_event('cat ' + json.dumps(raw)), "", 0, fixture)
        self.assertFalse(report["FAIL"])
        self.assertEqual(report["external_skill_reads"], [])
        self.assertIsNone(report["LIVE_BEHAVIOR_PASS"])

    def test_project_fixture_redirects_global_skill_path_preferences_without_changing_policy(self):
        text = runner.fixture_files({"id": "S01", "prompt": "original"})["AGENTS.md"]
        self.assertIn("same named fixture-local copy", text)
        self.assertIn("not higher-priority safety instructions", text)
        self.assertIn("Do not read installed host skill bodies", text)

    def test_catalog_tamper_cannot_reduce_or_duplicate_the_26_fixture_names(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            rows = [{"name": f"s{i:02}"} for i in range(26)]
            for row in rows:
                folder = root / ".agents/skills" / row["name"]
                folder.mkdir(parents=True)
                (folder / "SKILL.md").write_text("synthetic")
            catalog = root / "available_catalog.json"
            catalog.write_text(json.dumps(rows))
            self.assertEqual(len(runner.fixture_names(root)), 26)
            for altered in (rows[:-1], rows[:-1] + [rows[0]]):
                catalog.write_text(json.dumps(altered))
                with self.assertRaises(ValueError):
                    runner.fixture_names(root)

    def test_non_shell_tool_items_and_unfinished_calls_are_not_tool_free(self):
        for kind in ("web_search", "mcp_tool_call", "file_change", "unknown_future_tool"):
            for event_type in ("item.started", "item.completed"):
                trace = runner.parse_trace(json.dumps({"type": event_type, "item": {"type": kind}}))
                self.assertEqual(trace["tool_items"], [{"event_type": event_type, "item_type": kind}])

    def test_conditional_or_background_commands_do_not_establish_skill_reads(self):
        for command in ("true || cat /tmp/.agents/skills/load-testing/SKILL.md", "cat /tmp/.agents/skills/load-testing/SKILL.md || true", "cat /tmp/.agents/skills/steps/SKILL.md & true"):
            self.assertEqual(runner.parse_trace(command_event(command))["observed_skill_reads"], [])

    def test_strict_overlay_disables_unrelated_system_and_plugin_skills(self):
        fixture = Path(tempfile.gettempdir()).resolve() / "eval-fixture"
        local = str(fixture / ".agents/skills/steps/SKILL.md")
        external = [str(fixture.parent / "host/steps/SKILL.md"), str(fixture.parent / "system/openai-docs/SKILL.md"), str(fixture.parent / "plugins/design/SKILL.md")]
        skills = [{"name": "steps", "path": local, "enabled": True}] + [{"name": "external", "path": path, "enabled": True} for path in external]
        catalog = {"result": {"data": [{"skills": skills}]}}
        self.assertEqual(runner.isolated_overlays(catalog, fixture), [{"path": path, "enabled": False} for path in sorted(external)])
        for skill in skills[1:]:
            skill["enabled"] = False
        self.assertTrue(runner.verify_catalog(catalog, fixture, {"steps"})["fixture_only"])

    def test_native_catalog_rejects_host_leak_missing_and_duplicate_fixture_skills(self):
        fixture = Path(tempfile.gettempdir()).resolve() / "fixture"
        local = {"name": "steps", "path": str(fixture / ".agents/skills/steps/SKILL.md"), "enabled": True}
        host = {"name": "steps", "path": str(fixture.parent / "host/steps/SKILL.md"), "enabled": True}
        for skills in ([], [local, host], [local, local]):
            with self.assertRaises(ValueError):
                runner.verify_catalog({"result": {"data": [{"skills": skills}]}}, fixture, {"steps"})
        with self.assertRaises(ValueError):
            runner.verify_catalog({"result": {"data": [{"skills": [local], "errors": ["bad metadata"]}]}}, fixture, {"steps"})

    def test_runtime_configuration_disables_services_without_changing_model(self):
        config = runner.runtime_config([], "medium")
        self.assertIn("features.plugins=false", config)
        self.assertIn("features.apps=false", config)
        self.assertIn("features.remote_plugin=false", config)
        self.assertIn('model_reasoning_effort="medium"', config)
        self.assertNotIn("--model", config)

    def test_appserver_discovery_handles_buffered_notifications_and_closes_child(self):
        # An actual subprocess exercises portable pipe reading, not a mocked catalog.
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            script = root / "fake_server.py"
            script.write_text('import sys,json\nfor line in sys.stdin:\n e=json.loads(line)\n if "id" in e:\n  print(json.dumps({"method":"notice"}),flush=True)\n  print(json.dumps({"id":e["id"],"result":{"data":[]}}),flush=True)\n', encoding="utf-8")
            real_popen = runner.subprocess.Popen
            with patch.object(runner.subprocess, "Popen", side_effect=lambda command, **kw: real_popen([sys.executable, "-u", str(script)], **kw)):
                self.assertEqual(runner.discover(root)["result"], {"data": []})

    def test_discovery_cleanup_is_bounded_when_descendant_retains_stdout(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            script = root / "descendant_server.py"
            script.write_text('import sys,json,subprocess\nfor line in sys.stdin:\n e=json.loads(line)\n if "id" in e:\n  if e["id"]==2: subprocess.Popen([sys.executable,"-c","import time; time.sleep(4)"],stdin=subprocess.DEVNULL,stderr=subprocess.DEVNULL)\n  print(json.dumps({"id":e["id"],"result":{"data":[]}}),flush=True)\n', encoding="utf-8")
            real_popen = runner.subprocess.Popen
            started = time.monotonic()
            with patch.object(runner.subprocess, "Popen", side_effect=lambda command, **kw: real_popen([sys.executable, "-u", str(script)], **kw)):
                self.assertEqual(runner.discover(root)["result"], {"data": []})
            self.assertLess(time.monotonic() - started, 3)

    def test_preflight_unknown_model_never_executes_a_model_turn_or_falls_back(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            replies = [("version", "", 0), ("exec options", "", 0), ("--bundled", "", 0), ('{"models":[{"slug":"supported"}]}', "", 0)]
            with patch.object(runner, "invoke", side_effect=replies) as invoke:
                result = runner.preflight(root / "out", root, "unknown")
            self.assertEqual(result["status"], "UNVERIFIED")
            self.assertEqual(result["model_turns"], 0)
            self.assertEqual(invoke.call_count, 4)
            self.assertFalse(any("exec" in call.args[0] and "--json" in call.args[0] for call in invoke.call_args_list))

    def test_timeout_retains_raw_partial_trace_and_never_retries(self):
        import subprocess
        error = subprocess.TimeoutExpired(["codex"], 1, output=b'{"type":"turn.started"}\n', stderr="partial".encode())
        with patch.object(runner.subprocess, "run", side_effect=error) as execute:
            stdout, stderr, code = runner.invoke(["codex"], "input", 1)
        self.assertEqual(code, 124)
        self.assertIn('"turn.started"', stdout)
        self.assertIn("no automatic retry", stderr)
        execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()
