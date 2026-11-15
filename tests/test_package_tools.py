"""Executed filesystem fixtures, never the user's installed skills or services."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PureWindowsPath
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

sys.dont_write_bytecode = True
TOOL_PATH = Path(__file__).absolute().parents[1] / "scripts" / "package_tools.py"
spec = importlib.util.spec_from_file_location("package_tools", TOOL_PATH)
tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tools)


def write_skill(folder, name, description="Fixture behavior used only for tests."):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {description}\n---\n\n# Fixture\n", encoding="utf-8")


def entry(folder, package, name, personal=True):
    rows = tools.records(folder)
    return {"catalog_name": name if personal else "fixture:" + name, "kind": "user-global" if personal else "plugin-managed",
            "installable": personal, "physical_source": "fixture-original", "source_origin": "fixture-original",
            "physical_path_in_package": folder.relative_to(package).as_posix(),
            "snapshot_root": folder.relative_to(package).as_posix(), "destination_relative": name if personal else None,
            "skill_name": name, "description": "Fixture behavior used only for tests.", "files": rows, "file_count": len(rows),
            "tree_hash_sha256": tools.records_hash(rows), "source_tree_hash_sha256": tools.records_hash(rows)}


def make_package(path):
    path.mkdir()
    (path / "VERSION").write_text("3.1.0\n")
    original_names = set("apple-design architecture-review compatible-response db-impact devil final-check full-plan hand-off multiple-pov natural-persian-writing performance-review practical-test regression-check root-cause steps ui-ux-pro-max".split())
    entries, snapshots = [], []
    for name in sorted(tools.APPROVED_NAMES):
        folder = path / "skills" / name
        write_skill(folder, name)
        if name in original_names:
            item = entry(folder, path, name)
            entries.append(item)
            snapshots.append({"snapshot_root": item["snapshot_root"], "source_origin": "fixture-original",
                              "source_selected_tree_hash_sha256": item["tree_hash_sha256"], "package_tree_hash_sha256": item["tree_hash_sha256"],
                              "source_package_equal": True, "file_count": item["file_count"], "files": item["files"]})
    for number in range(16):
        name = f"managed-{number:02}"
        folder = path / "managed" / "plugin-skills" / "fixture" / name / "1" / "skills" / name
        write_skill(folder, name)
        item = entry(folder, path, name, personal=False)
        entries.append(item)
        snapshots.append({"snapshot_root": item["snapshot_root"], "source_origin": "managed-fixture-original",
                          "source_selected_tree_hash_sha256": item["tree_hash_sha256"], "package_tree_hash_sha256": item["tree_hash_sha256"],
                          "source_package_equal": True, "file_count": item["file_count"], "files": item["files"]})
    manifest = {"schema_version": 1, "package_version": "3.0.0", "created_utc": "2026-01-01T00:00:00+00:00",
                "expected_user_global": 16, "expected_plugin_managed": 16, "system_skills_excluded": sorted(tools.SYSTEM_NAMES),
                "skills": entries, "snapshot_trees": snapshots, "exclusions": [], "hardcoded_path_findings": []}
    tools.write_json(path / "skills-manifest.json", manifest)
    return manifest


def remove_fixture_tree(root):
    """Clean owned test data, including Git's read-only Windows pack objects."""
    root = Path(root).absolute()
    if not root.name.startswith("skill-tools-"):
        raise ValueError("Refusing cleanup outside an owned package-tool fixture")
    def retry(function, path, error):
        info = os.lstat(path)
        if (os.name == "nt" and isinstance(error[1], PermissionError)
                and function in {os.unlink, os.remove}
                and Path(path).absolute().is_relative_to(root)
                and stat.S_ISREG(info.st_mode)
                and not getattr(info, "st_file_attributes", 0) & 0x400
                and not info.st_mode & stat.S_IWRITE):
            os.chmod(path, info.st_mode | stat.S_IWRITE)
            function(path)
        else:
            raise error[1]
    shutil.rmtree(root, onerror=retry)


class PackageToolTests(unittest.TestCase):
    def test_windows_spelling_guard_allows_dot_navigation_for_bounded_references(self):
        from pathlib import PureWindowsPath
        link = PureWindowsPath('D:/repo/skills/full-plan/platforms/../docs/PLATFORM-COMPATIBILITY.md')
        self.assertEqual(tools.ordinary_windows_path(link), link)
        for component in ('platforms.', 'platforms ', 'SHORT~1'):
            with self.assertRaises(tools.PackageError):
                tools.ordinary_windows_path(PureWindowsPath('D:/repo') / component / 'docs/file.md')

    @classmethod
    def setUpClass(cls):
        cls.shared = Path(tempfile.mkdtemp(prefix="skill-tools-fixture-")).resolve()
        cls.fixture = cls.shared / "package"
        cls.original_manifest = make_package(cls.fixture)
        tools.build(cls.fixture)

    @classmethod
    def tearDownClass(cls):
        remove_fixture_tree(cls.shared)

    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="skill-tools-test-")).resolve()
        self.package = self.temp / "package"
        shutil.copytree(self.fixture, self.package)
        self.stage = self.temp / "stage"
        shutil.copytree(self.package / "skills", self.stage)
        self.destination = self.temp / "codex" / "skills"
        self.backups = self.temp / "backups"

    def tearDown(self):
        remove_fixture_tree(self.temp)

    def promote(self, **kwargs):
        return tools.promote(self.package, self.stage, self.destination, self.backups, **kwargs)

    def existing(self, name="steps", extra="Local custom content\n", root=None):
        folder = (root or self.destination) / name
        write_skill(folder, name)
        (folder / "custom.txt").write_text(extra)
        return folder

    def sentinel(self, root=None):
        root = root or self.destination
        self.existing("unrelated", root=root)
        write_skill(root / ".system" / "system-fixture", "system-fixture")
        (root / ".system" / "system-fixture" / "keep.bin").write_bytes(b"\x00\xFF\x11")
        return tools.preservation_fingerprint([root], [root / name for name in tools.APPROVED_NAMES])

    def test_distribution_and_staging_inventory(self):
        result = tools.verify_package(self.package, self.stage)
        self.assertEqual(result["status"], "STATIC_PASS")
        self.assertEqual((result["personal_skills"], result["managed_snapshots"]), (26, 16))

    def test_manifest_managed_records_and_snapshots_preserved(self):
        current = tools.read_json(self.package / "skills-manifest.json")
        self.assertEqual([e for e in current["skills"] if not e["installable"]], [e for e in self.original_manifest["skills"] if not e["installable"]])
        self.assertEqual([s for s in current["snapshot_trees"] if s["snapshot_root"].startswith("managed/")],
                         [s for s in self.original_manifest["snapshot_trees"] if s["snapshot_root"].startswith("managed/")])

    def test_hash_contract_matches_powershell_ordinal_utf16(self):
        rows = [{"path": "z.txt", "sha256": "a" * 64}, {"path": "A.txt", "sha256": "b" * 64}]
        expected = hashlib.sha256(("A.txt\0" + "b" * 64 + "\nz.txt\0" + "a" * 64 + "\n").encode()).hexdigest()
        self.assertEqual(tools.records_hash(rows), expected)
        self.assertEqual(tools.records_hash(list(reversed(rows))), expected)

    def test_tampered_package_file_is_refused(self):
        (self.package / "skills" / "steps" / "SKILL.md").write_text("tampered")
        with self.assertRaisesRegex(tools.PackageError, "integrity"):
            tools.verify_package(self.package)

    def test_omitted_integrity_record_detected_even_with_new_aggregate(self):
        path = self.package / "package-integrity.json"
        data = tools.read_json(path)
        data["files"].pop()
        data["package_tree_hash_sha256"] = tools.records_hash(data["files"])
        tools.write_json(path, data)
        with self.assertRaisesRegex(tools.PackageError, "coverage"):
            tools.verify_package(self.package)

    def test_unlisted_extra_distribution_file_is_refused(self):
        (self.package / "unexpected.txt").write_text("extra")
        with self.assertRaisesRegex(tools.PackageError, "coverage"):
            tools.verify_package(self.package)

    def test_integrity_case_colliding_paths_refused(self):
        path = self.package / "package-integrity.json"
        data = tools.read_json(path)
        duplicate = copy.deepcopy(data["files"][0])
        duplicate["path"] = duplicate["path"].upper()
        data["files"].append(duplicate)
        tools.write_json(path, data)
        with self.assertRaisesRegex(tools.PackageError, "Duplicate file"):
            tools.verify_package(self.package)

    def test_path_traversal_and_windows_paths_refused(self):
        for value in ["../outside", "a/../outside", "C:/outside", "/etc/passwd", "a\\b", ".system/a", "a//b", "a/CON", "a.",
                      "..\\outside", "\\\\server\\share\\file", "C:file", "x:stream", "a/aux.txt", "a/COM¹.log",
                      ".SYSTEM/a", ".GIT/config", "a /file", "a./file", "a/\x00file", "a/file?"]:
            with self.subTest(value=value), self.assertRaises(tools.PackageError):
                tools.safe_path(self.temp, value)

    def test_windows_root_policy_on_drive_unc_unicode_and_extended_paths(self):
        for value in [r"C:\Users\sample\.codex\skills", r"C:\Users\sample\.agents\Skills",
                      "\\\\server\\share\\کاربر\\.codex\\skills", "C:\\Users\\" + "long\\" * 60 + "skills"]:
            with self.subTest(value=value):
                path = PureWindowsPath(value)
                self.assertEqual(tools.validate_personal_root_path(path), path)
        for value in [r"C:\skills", r"\\server\share\skills", r"C:profile\skills", r"\profile\skills",
                      r"\\?\C:\Users\sample\.codex\skills", r"\\.\C:\Users\sample\.codex\skills",
                      r"C:\Users\sample\plugins.\skills", "C:\\Users\\sample\\cache \\skills",
                      r"C:\Users\sample\PLUGI~1\skills",
                      r"C:\Users\sample\.SYSTEM\skills", r"C:\Users\sample\Plugins\skills",
                      r"C:\Users\sample\cache\skills", r"C:\Users\sample\managed\skills"]:
            with self.subTest(value=value), self.assertRaises(tools.PackageError):
                tools.validate_personal_root_path(PureWindowsPath(value))
        # Simulate the OS's alias expansion, then exercise the actual overlap
        # decision. This does not certify the Win32 resolver on a non-Windows OS.
        alias = PureWindowsPath(r"C:\TEMPLO~1\package\skills")
        canonical = PureWindowsPath(r"C:\TempLongName\package\skills")
        package = PureWindowsPath(r"C:\TempLongName\package")
        with mock.patch.object(tools, "Path", PureWindowsPath), \
                mock.patch.object(tools.os.path, "realpath", side_effect=[str(canonical), str(package)]), \
                mock.patch.object(tools.os, "name", "nt"):
            self.assertFalse(tools.disjoint(alias, package), "Native alias expansion must prevent source overlap")
        for value in [r"C:\Users\sample\.system\backup", r"C:\Users\sample\plugins\backup",
                      r"C:\Users\sample\cache\backup", r"C:\Users\sample\managed\backup",
                      r"C:\Users\sample\PLUGI~1\backup", r"C:\Users\sample\plugins.\backup",
                      "C:\\Users\\sample\\cache \\backup"]:
            with self.subTest(backup=value), self.assertRaises(tools.PackageError):
                tools.validate_backup_path(PureWindowsPath(value))
        # A mapped drive can hide a protected component even without '~'.
        # Stub only native resolution; the production component guard stays real.
        original = PureWindowsPath(r"X:\profile\skills")
        protected = PureWindowsPath(r"C:\Users\sample\plugins\profile\skills")
        with mock.patch.object(tools, "no_links", return_value=original), \
                mock.patch.object(tools, "Path", PureWindowsPath), \
                mock.patch.object(tools.os.path, "realpath", return_value=str(protected)), \
                mock.patch.object(tools.os, "name", "nt"):
            with self.assertRaisesRegex(tools.PackageError, "protected"):
                tools.protected_root(original)
            with self.assertRaisesRegex(tools.PackageError, "outside system/plugin"):
                tools.protected_backup(original)

    def test_unicode_bom_crlf_metadata_and_raw_hashes(self):
        folder = self.temp / "پوشه با فاصله"
        folder.mkdir()
        file = folder / "SKILL.md"
        text = "---\r\nname: steps\r\ndescription: Persian مسیر fixture.\r\n---\r\n"
        file.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))
        self.assertEqual(tools.metadata(file)["description"], "Persian مسیر fixture.")
        expected = hashlib.sha256(file.read_bytes()).hexdigest()
        self.assertEqual(tools.records(folder)[0]["sha256"], expected)
        before = tools.tree_hash(folder)
        os.utime(file, (1000000000, 1000000000))
        self.assertEqual(tools.tree_hash(folder), before, "Timestamps must not affect byte fingerprints")
        file.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))
        self.assertNotEqual(tools.tree_hash(folder), before, "BOM/newline changes must remain visible")

    def test_unicode_and_shell_metacharacter_cli_paths_are_literal_and_read_only(self):
        self.package = self.package.rename(self.temp / "بسته & $(literal) ' [x]")
        self.stage = self.stage.rename(self.temp / "مرحله با فاصله")
        self.destination = self.temp / "کاربر & $(literal)" / ".codex" / "skills"
        before = tools.records(self.temp, selected=False)
        command = [sys.executable, "-B", str(TOOL_PATH), "plan", "--package-root", str(self.package),
                   "--stage-root", str(self.stage), "--destination-root", str(self.destination)]
        process = subprocess.run(command, capture_output=True, encoding="utf-8",
                                 env={**os.environ, "PYTHONIOENCODING": "ascii", "PYTHONUTF8": "0"}, timeout=30)
        self.assertEqual(process.returncode, 0, process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual(result["roots"], [str(self.destination)])
        self.assertEqual(result["status"], "PLAN")
        self.assertEqual(before, tools.records(self.temp, selected=False))
        self.assertFalse(self.destination.parent.exists())

    def test_mixed_case_duplicate_catalog_is_refused_without_mutation(self):
        write_skill(self.destination / "nested" / "STEPS", "STEPS")
        before = tools.records(self.temp, selected=False)
        with self.assertRaisesRegex(tools.PackageError, "Duplicate skill"):
            self.promote(replace=True)
        self.assertEqual(before, tools.records(self.temp, selected=False))
        self.assertFalse(self.backups.exists())

    def test_mixed_case_managed_catalog_is_refused_without_mutation(self):
        write_skill(self.destination / "MANAGED-00", "MANAGED-00")
        before = tools.records(self.temp, selected=False)
        with self.assertRaisesRegex(tools.PackageError, "Managed skill"):
            self.promote(replace=True)
        self.assertEqual(before, tools.records(self.temp, selected=False))

    def test_manifest_catalog_case_collision_refused(self):
        path = self.package / "skills-manifest.json"
        manifest = tools.read_json(path)
        managed = next(item for item in manifest["skills"] if not item["installable"])
        managed["catalog_name"] = "STEPS"
        tools.write_json(path, manifest)
        with self.assertRaisesRegex(tools.PackageError, "Duplicate/empty catalog"):
            tools.read_manifest(self.package)

    def test_windows_liveness_query_never_sends_a_signal(self):
        for result, expected in [(0, False), (258, True), (0xFFFFFFFF, True)]:
            kernel = mock.MagicMock()
            kernel.OpenProcess.return_value = 123
            kernel.WaitForSingleObject.return_value = result
            with self.subTest(result=result), mock.patch("ctypes.WinDLL", return_value=kernel, create=True), \
                    mock.patch.object(tools.os, "name", "nt"), mock.patch.object(tools.os, "kill") as kill:
                self.assertEqual(tools.process_alive(1234), expected)
                kernel.OpenProcess.assert_called_once_with(0x00100000, False, 1234)
                kernel.WaitForSingleObject.assert_called_once_with(123, 0)
                kernel.CloseHandle.assert_called_once_with(123)
                kill.assert_not_called()

    def test_windows_liveness_unknown_access_fails_closed(self):
        for error, expected in [(87, False), (5, True), (123, True)]:
            kernel = mock.MagicMock()
            kernel.OpenProcess.return_value = None
            with self.subTest(error=error), mock.patch("ctypes.WinDLL", return_value=kernel, create=True), \
                    mock.patch("ctypes.get_last_error", return_value=error, create=True):
                self.assertEqual(tools.windows_process_alive(1234), expected)
                kernel.WaitForSingleObject.assert_not_called()
                kernel.CloseHandle.assert_not_called()

    def test_liveness_probe_preserves_live_child_and_detects_exit(self):
        child = subprocess.Popen([sys.executable, "-B", "-c", "import sys; sys.stdin.buffer.read(1)"],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            self.assertTrue(tools.process_alive(child.pid))
            self.assertIsNone(child.poll(), "A liveness probe must not terminate its target")
            child.communicate(b"x", timeout=10)
            self.assertEqual(child.returncode, 0)
            self.assertFalse(tools.process_alive(child.pid))
        finally:
            if child.poll() is None:
                child.communicate(b"x", timeout=10)

    @unittest.skipUnless(shutil.which("git"), "Git is required for the checkout byte-integrity fixture")
    def test_git_autocrlf_checkouts_preserve_bom_newlines_binary_and_unicode(self):
        source = self.temp / "git-source"
        source.mkdir()
        attributes = TOOL_PATH.parents[1] / ".gitattributes"
        (source / ".gitattributes").write_bytes(attributes.read_bytes())
        payloads = {"LF.txt": b"line 1\nline 2\n", "CRLF.txt": b"line 1\r\nline 2\r\n",
                    "BOM.txt": b"\xef\xbb\xbfline\n", "داده.bin": bytes(range(256))}
        for name, content in payloads.items():
            (source / name).write_bytes(content)
        environment = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}
        hooks = self.temp / "empty-hooks"
        hooks.mkdir()
        def git(*args):
            process = subprocess.run(["git", "-c", "core.hooksPath=" + str(hooks), *args],
                                     capture_output=True, text=True, env=environment, timeout=30)
            self.assertEqual(process.returncode, 0, process.stderr)
        git("-C", str(source), "init", "--quiet")
        git("-C", str(source), "-c", "core.autocrlf=false", "add", ".")
        git("-C", str(source), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
            "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "byte fixture")
        expected = tools.tree_hash(source)
        for setting in ["true", "false", "input"]:
            with self.subTest(autocrlf=setting):
                checkout = self.temp / ("checkout-" + setting)
                git("clone", "--quiet", "--no-local", "-c", "core.autocrlf=" + setting, str(source), str(checkout))
                self.assertEqual(tools.tree_hash(checkout), expected)
                for name, content in payloads.items():
                    self.assertEqual((checkout / name).read_bytes(), content)

    def test_malicious_manifest_mapping_refused(self):
        path = self.package / "skills-manifest.json"
        data = tools.read_json(path)
        data["skills"][0]["physical_path_in_package"] = "../outside"
        tools.write_json(path, data)
        with self.assertRaises(tools.PackageError):
            tools.read_manifest(self.package)

    def test_name_directory_mismatch_refused(self):
        write_skill(self.package / "skills" / "steps", "wrong-name")
        with self.assertRaisesRegex(tools.PackageError, "Name/directory"):
            tools.build(self.package)

    def test_build_reconciles_resolved_platform_issue_and_preserves_provenance(self):
        path = self.package / "skills-manifest.json"
        manifest = tools.read_json(path)
        ui = next(e for e in manifest["skills"] if e["skill_name"] == "ui-ux-pro-max")
        ui.pop("baseline_notes", None)
        ui.pop("baseline_platform_assumption_evidence", None)
        ui["notes"] = ["Historical plugin environment assumption is preserved."]
        ui["platform_assumption_evidence"] = [{"file": "SKILL.md", "line": 42, "text": "old plugin path"}]
        tools.write_json(path, manifest)
        tools.build(self.package)
        current = tools.read_json(path)
        updated = next(e for e in current["skills"] if e["skill_name"] == "ui-ux-pro-max")
        self.assertEqual(updated["baseline_notes"], ui["notes"])
        self.assertEqual(updated["baseline_platform_assumption_evidence"], ui["platform_assumption_evidence"])
        self.assertEqual(updated["platform_assumption_evidence"], [])
        self.assertIn("no plugin environment variable", updated["notes"][0])
        self.assertEqual(next(e for e in current["skills"] if e["skill_name"] == "apple-design")["platform_requirements"], [])
        tools.build(self.package)
        rebuilt = next(e for e in tools.read_json(path)["skills"] if e["skill_name"] == "ui-ux-pro-max")
        self.assertEqual(rebuilt["baseline_notes"], ui["notes"])

    def test_strict_yaml_duplicate_keys_and_aliases_refused(self):
        skill = self.temp / "SKILL.md"
        for description in ["description: text\ndescription: other", "description: &anchor text\nmetadata: *anchor", "description: invalid: mapping"]:
            skill.write_text("---\nname: steps\n" + description + "\n---\n")
            with self.subTest(description=description), self.assertRaises(tools.PackageError):
                tools.metadata(skill)

    def test_nested_discoverable_skill_refused(self):
        write_skill(self.package / "skills" / "steps" / "nested", "steps")
        # Hashes may agree after rebuild, but discoverability must still fail.
        with self.assertRaisesRegex(tools.PackageError, "Nested discoverable"):
            tools.build(self.package)

    def test_relative_link_escape_and_missing_resource_refused(self):
        skill = self.package / "skills" / "steps" / "SKILL.md"
        for target in ["../../VERSION", "missing.md", "%2e%2e/%2e%2e/VERSION"]:
            original = self.fixture / "skills" / "steps" / "SKILL.md"
            skill.write_text(original.read_text() + f"\n[reference]({target})\n")
            with self.subTest(target=target), self.assertRaisesRegex(tools.PackageError, "reference"):
                tools.build(self.package)

    @unittest.skipUnless(hasattr(os, "symlink"), "Host has no symlink support")
    def test_symlink_resource_and_nested_git_link_refused(self):
        outside = self.temp / "outside"
        outside.mkdir()
        for name in ["linked", ".git"]:
            link = self.package / "skills" / "steps" / name
            link.symlink_to(outside, target_is_directory=True)
            try:
                with self.subTest(name=name), self.assertRaisesRegex(tools.PackageError, "Symlink"):
                    tools.build(self.package)
            finally:
                link.unlink()

    def test_secret_scan_reports_rule_without_secret_content(self):
        fake = "ghp_" + "X" * 40
        (self.package / "fixture.txt").write_text(fake)
        result = tools.scan_secrets(self.package)
        self.assertEqual(result, [{"file": "fixture.txt", "rule": "github_token"}])
        self.assertNotIn(fake, json.dumps(result))

    def test_generated_stage_files_are_refused(self):
        cache = self.stage / "steps" / "__pycache__"
        cache.mkdir()
        (cache / "stale.pyc").write_bytes(b"cached")
        with self.assertRaisesRegex(tools.PackageError, "Unexpected excluded"):
            tools.verify_package(self.package, self.stage)

    def test_stage_missing_or_managed_directory_refused(self):
        shutil.rmtree(self.stage / "steps")
        with self.assertRaisesRegex(tools.PackageError, "exactly"):
            tools.verify_package(self.package, self.stage)
        shutil.copytree(self.package / "skills" / "steps", self.stage / "steps")
        (self.stage / "managed").mkdir()
        with self.assertRaisesRegex(tools.PackageError, "exactly"):
            tools.verify_package(self.package, self.stage)

    def test_plan_does_not_mutate_filesystem(self):
        before = tools.records(self.temp, selected=False)
        plan = tools.plan_install(self.package, self.stage, self.destination)
        self.assertEqual(plan["status"], "PLAN")
        self.assertEqual(before, tools.records(self.temp, selected=False))

    def test_clean_install_and_idempotency(self):
        preserved = self.sentinel()
        first = self.promote()
        self.assertEqual((first["status"], first["personal_verified"]), ("COMMITTED", 26))
        for name in tools.APPROVED_NAMES:
            self.assertEqual(tools.tree_hash(self.stage / name), tools.tree_hash(self.destination / name))
        self.assertEqual(preserved, tools.preservation_fingerprint([self.destination], [self.destination / name for name in tools.APPROVED_NAMES]))
        second = self.promote()
        self.assertEqual(second["status"], "UNCHANGED")
        self.assertIsNone(second["backup_root"])
        self.assertFalse(any(p.name.startswith("managed-") for p in self.destination.iterdir()))
        self.assertFalse((self.destination.parent / ".skill-package-install.lock").exists())

    def test_existing_collision_requires_explicit_replace(self):
        folder = self.existing()
        before = tools.tree_hash(folder, selected=False)
        with self.assertRaisesRegex(tools.PackageError, "--replace"):
            self.promote()
        self.assertEqual(before, tools.tree_hash(folder, selected=False))
        self.assertFalse(self.backups.exists())

    def test_unknown_directory_collision_refused(self):
        folder = self.destination / "steps"
        folder.mkdir(parents=True)
        (folder / "private.txt").write_text("preserve unknown data")
        with self.assertRaisesRegex(tools.PackageError, "Unrecognized"):
            self.promote(replace=True)
        self.assertTrue((folder / "private.txt").exists())

    def test_wrong_skill_at_destination_refused(self):
        write_skill(self.destination / "steps", "unrelated")
        with self.assertRaisesRegex(tools.PackageError, "Different skill"):
            self.promote(replace=True)

    def test_backup_exact_bytes_permissions_and_rollback(self):
        folder = self.existing()
        (folder / "private.bin").write_bytes(bytes(range(256)))
        os.chmod(folder / "private.bin", 0o600)
        original = tools.tree_hash(folder, selected=False)
        before_mode = (folder / "private.bin").stat().st_mode
        self.sentinel()
        result = self.promote(replace=True)
        data = tools.read_json(result["journal"])
        old = next(row for row in data["rows"] if row["skill"] == "steps")
        self.assertEqual(original, tools.tree_hash(old["backup"], selected=False))
        restored = tools.rollback(result["journal"], [self.destination])
        self.assertEqual(restored["status"], "ROLLED_BACK")
        self.assertEqual(original, tools.tree_hash(folder, selected=False))
        self.assertEqual(before_mode, (folder / "private.bin").stat().st_mode)
        self.assertEqual({p.name for p in self.destination.iterdir()}, {"steps", "unrelated", ".system"})
        self.assertTrue(Path(old["backup"]).exists())
        self.assertTrue(tools.rollback(result["journal"], [self.destination])["already_restored"])

    def test_readonly_original_is_backed_up_replaced_and_restored(self):
        folder = self.existing()
        file = folder / "custom.txt"
        file.chmod(stat.S_IREAD)
        before = tools.tree_hash(folder, selected=False)
        mode = file.stat().st_mode
        try:
            result = self.promote(replace=True)
            journal = tools.read_json(result["journal"])
            row = next(item for item in journal["rows"] if item["skill"] == "steps")
            backup_file = Path(row["backup"]) / "custom.txt"
            self.assertEqual(backup_file.stat().st_mode, mode)
            self.assertEqual(tools.tree_hash(row["backup"], selected=False), before)
            self.assertFalse(list(self.destination.parent.glob(".skill-package-stage-*")))
            tools.rollback(result["journal"], [self.destination])
            self.assertEqual(tools.tree_hash(folder, selected=False), before)
            self.assertEqual(file.stat().st_mode, mode)
            self.assertEqual(backup_file.stat().st_mode, mode, "The retained backup must remain read-only")
        finally:
            # Fixture teardown also runs on Windows, where read-only files cannot
            # be unlinked. This cleanup is confined to this synthetic temp tree.
            for owned in self.temp.rglob("*"):
                if owned.is_file():
                    owned.chmod(owned.stat().st_mode | stat.S_IWRITE)

    def test_backup_permission_failure_preserves_destination_and_releases_lock(self):
        self.existing()
        before = tools.records(self.destination, selected=False)
        real_copy = tools.shutil.copytree
        def fail_backup(source, target, *args, **kwargs):
            if Path(target).parent.name == "backups":
                raise PermissionError("Injected isolated backup permission failure")
            return real_copy(source, target, *args, **kwargs)
        with mock.patch.object(tools.shutil, "copytree", side_effect=fail_backup), \
                self.assertRaisesRegex(PermissionError, "backup permission"):
            self.promote(replace=True)
        self.assertEqual(before, tools.records(self.destination, selected=False))
        self.assertFalse((self.destination.parent / ".skill-package-install.lock").exists())
        self.assertFalse(list(self.destination.parent.glob(".skill-package-stage-*")))
        self.assertFalse(list(self.backups.glob("*/transaction.json")))

    def test_rollback_does_not_recursively_delete_live_skill(self):
        self.existing("ui-ux-pro-max")
        before = tools.records(self.destination, selected=False)
        result = self.promote(replace=True)
        original_rmtree = tools.shutil.rmtree

        def guarded_rmtree(path, *args, **kwargs):
            self.assertFalse(tools.inside(tools.absolute(path), self.destination), "Live skill must be atomically displaced")
            return original_rmtree(path, *args, **kwargs)

        with mock.patch.object(tools.shutil, "rmtree", guarded_rmtree):
            tools.rollback(result["journal"], [self.destination])
        self.assertEqual(before, tools.records(self.destination, selected=False))

    def test_rollback_process_crash_at_atomic_rename_boundaries_is_resumable(self):
        for boundary in ("displaced", "restored"):
            with self.subTest(boundary=boundary):
                self.existing("ui-ux-pro-max", extra="Original bytes retained\n")
                self.sentinel()
                before = tools.records(self.destination, selected=False)
                result = self.promote(replace=True)
                script = """
import importlib.util, os, sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('tools',sys.argv[1]); tools=importlib.util.module_from_spec(spec); spec.loader.exec_module(tools)
destination=Path(sys.argv[3])/'ui-ux-pro-max'; boundary=sys.argv[4]; real=tools.os.replace
def crash(source,target):
    value=real(source,target)
    if (boundary=='displaced' and Path(source)==destination) or (boundary=='restored' and Path(target)==destination):
        os._exit(87)
    return value
tools.os.replace=crash
tools.rollback(sys.argv[2],[Path(sys.argv[3])])
"""
                process = subprocess.run([sys.executable,"-B","-c",script,str(TOOL_PATH),result["journal"],str(self.destination),boundary], capture_output=True,text=True)
                self.assertEqual(process.returncode,87,process.stderr)
                self.assertEqual(tools.read_json(result["journal"])["status"],"ROLLING_BACK")
                self.assertFalse(tools.process_alive(tools.read_json(result["journal"])["pid"]))
                tools.rollback(result["journal"],[self.destination])
                self.assertEqual(before,tools.records(self.destination,selected=False))
                self.assertFalse(list(self.destination.parent.glob(".skill-package-stage-*")))
                self.assertFalse((self.destination.parent/".skill-package-install.lock").exists())

    def test_rollback_process_crash_during_backup_copy_is_resumable(self):
        self.existing("ui-ux-pro-max",extra="Custom original data\n")
        before = tools.records(self.destination,selected=False)
        result = self.promote(replace=True)
        script = """
import importlib.util, os, sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('tools',sys.argv[1]); tools=importlib.util.module_from_spec(spec); spec.loader.exec_module(tools)
real=tools.shutil.copytree
def crash(source,target,*args,**kwargs):
    target=Path(target)
    if target.name.startswith('restore-'):
        target.mkdir(); (target/'SKILL.md').write_bytes((Path(source)/'SKILL.md').read_bytes()); os._exit(88)
    return real(source,target,*args,**kwargs)
tools.shutil.copytree=crash
tools.rollback(sys.argv[2],[Path(sys.argv[3])])
"""
        process = subprocess.run([sys.executable,"-B","-c",script,str(TOOL_PATH),result["journal"],str(self.destination)],capture_output=True,text=True)
        self.assertEqual(process.returncode,88,process.stderr)
        tools.rollback(result["journal"],[self.destination])
        self.assertEqual(before,tools.records(self.destination,selected=False))

    def test_concurrent_crash_recovery_admits_only_one_process(self):
        self.existing("ui-ux-pro-max")
        self.sentinel()
        before = tools.records(self.destination, selected=False)
        crash_installer = """
import importlib.util, sys
from pathlib import Path
spec=importlib.util.spec_from_file_location('tools',sys.argv[1]); tools=importlib.util.module_from_spec(spec); spec.loader.exec_module(tools)
tools.promote(Path(sys.argv[2]),Path(sys.argv[3]),Path(sys.argv[4]),Path(sys.argv[5]),replace=True,crash_after=26)
"""
        crashed = subprocess.run([sys.executable,"-B","-c",crash_installer,str(TOOL_PATH),str(self.package),str(self.stage),str(self.destination),str(self.backups)],capture_output=True,text=True)
        self.assertEqual(crashed.returncode,86,crashed.stderr)
        journal = str(next(self.backups.glob("*/transaction.json")))
        ready, release = self.temp/"recovery-ready", self.temp/"recovery-release"
        recovery = """
import importlib.util, sys, time
from pathlib import Path
spec=importlib.util.spec_from_file_location('tools',sys.argv[1]); tools=importlib.util.module_from_spec(spec); spec.loader.exec_module(tools)
ready,release=Path(sys.argv[4]),Path(sys.argv[5]); real=tools.write_json
def hold(path,value):
    if value.get('status')=='ROLLING_BACK' and not ready.exists():
        ready.write_text('exclusive claim held')
        deadline=time.monotonic()+10
        while not release.exists():
            if time.monotonic()>deadline: raise RuntimeError('test release timeout')
            time.sleep(0.01)
    return real(path,value)
if sys.argv[6]=='holder': tools.write_json=hold
tools.rollback(Path(sys.argv[2]),[Path(sys.argv[3])])
"""
        args=[sys.executable,"-B","-c",recovery,str(TOOL_PATH),journal,str(self.destination),str(ready),str(release)]
        holder=subprocess.Popen(args+["holder"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        try:
            deadline=time.monotonic()+10
            while not ready.exists():
                if holder.poll() is not None or time.monotonic()>deadline:
                    self.fail("Recovery holder did not reach its exclusive admission boundary")
                time.sleep(0.01)
            contender=subprocess.run(args+["contender"],capture_output=True,text=True,timeout=10)
            self.assertNotEqual(contender.returncode,0,"Second recovery was admitted while the first held the transaction")
            self.assertIn("Another recovery holds the lock",contender.stderr)
            self.assertEqual(tools.read_json(journal)["status"],"IN_PROGRESS")
        finally:
            release.write_text("continue")
            stdout,stderr=holder.communicate(timeout=10)
        self.assertEqual(holder.returncode,0,stderr)
        self.assertEqual(tools.read_json(journal)["status"],"ROLLED_BACK")
        self.assertEqual(before,tools.records(self.destination,selected=False))
        self.assertFalse((self.destination.parent/".skill-package-install.lock").exists())

    def test_legacy_invalid_description_can_be_backed_up_and_repaired(self):
        folder = self.existing("natural-persian-writing")
        file = folder / "SKILL.md"
        file.write_text("---\nname: natural-persian-writing\ndescription: legacy: malformed\n---\n")
        old = tools.tree_hash(folder, selected=False)
        result = self.promote(replace=True)
        tools.metadata(folder / "SKILL.md")
        tools.rollback(result["journal"], [self.destination])
        self.assertEqual(old, tools.tree_hash(folder, selected=False))

    def test_partial_failure_restores_all_originals_and_preserves_unrelated(self):
        first = self.existing("apple-design")
        second = self.existing("architecture-review")
        self.sentinel()
        before = tools.records(self.destination, selected=False)
        with self.assertRaisesRegex(tools.PackageError, "Injected"):
            self.promote(replace=True, fail_after=4)
        self.assertEqual(before, tools.records(self.destination, selected=False))
        journal = next(self.backups.glob("*/transaction.json"))
        self.assertEqual(tools.read_json(journal)["status"], "ROLLED_BACK")
        self.assertFalse((self.destination.parent / ".skill-package-install.lock").exists())
        self.assertFalse(list(self.destination.parent.glob(".skill-package-stage-*")))

    def test_lock_collision_preserves_other_installer_lock(self):
        self.destination.parent.mkdir()
        lock = self.destination.parent / ".skill-package-install.lock"
        lock.write_text("existing other lock")
        with self.assertRaises(FileExistsError):
            self.promote()
        self.assertEqual(lock.read_text(), "existing other lock")
        self.assertFalse(self.destination.exists())

    def test_protected_and_overlapping_destinations_refused(self):
        for root in [self.package / "skills", self.temp / "plugins" / "x" / "skills", self.temp / ".system" / "skills", self.stage]:
            with self.subTest(root=root), self.assertRaises(tools.PackageError):
                tools.plan_install(self.package, self.stage, root)

    def test_backup_inside_destination_refused(self):
        with self.assertRaisesRegex(tools.PackageError, "Backup root overlaps"):
            tools.promote(self.package, self.stage, self.destination, self.destination / "backups")

    def test_backup_protected_ancestors_refused_without_destination_writes(self):
        self.existing()
        before = tools.records(self.destination, selected=False)
        for part in [".system", "plugins", "cache", "managed"]:
            backup = self.temp / part / "ordinary-backups"
            with self.subTest(part=part), self.assertRaisesRegex(tools.PackageError, "outside system/plugin"):
                tools.promote(self.package, self.stage, self.destination, backup, replace=True)
            self.assertFalse(backup.exists())
            self.assertEqual(before, tools.records(self.destination, selected=False))

    def test_recovery_journal_under_protected_backup_ancestor_refused(self):
        result = self.promote()
        moved = self.temp / "plugins" / Path(result["backup_root"]).name
        moved.parent.mkdir()
        shutil.copytree(result["backup_root"], moved)
        with self.assertRaisesRegex(tools.PackageError, "outside system/plugin"):
            tools.rollback(moved / "transaction.json", [self.destination])

    def test_later_unrelated_changes_are_preserved_during_rollback(self):
        result = self.promote()
        folder = self.existing("unrelated", extra="Created after installation\n")
        before = tools.tree_hash(folder)
        tools.rollback(result["journal"], [self.destination])
        self.assertEqual(before, tools.tree_hash(folder))

    def test_rollback_refuses_other_lock_and_releases_only_newly_acquired_locks(self):
        agents = self.temp / "agents" / "skills"
        mapping = {"roots": [str(agents)], "destinations": {"hand-off": str(agents / "hand-off")}}
        result = self.promote(mapping=mapping)
        # Roots are sorted agents first, codex second. Failure on the latter must
        # remove the new former lock while preserving the competing lock.
        lock = self.destination.parent / ".skill-package-install.lock"
        lock.write_text(json.dumps({"transaction_id": "another", "pid": os.getpid()}))
        with self.assertRaisesRegex(tools.PackageError, "Another transaction"):
            tools.rollback(result["journal"], [self.destination, agents])
        self.assertTrue(lock.exists())
        self.assertFalse((agents.parent / ".skill-package-install.lock").exists())

    def test_duplicate_unmapped_skill_refused(self):
        self.existing("steps")
        write_skill(self.destination / "nested" / "steps", "steps")
        with self.assertRaisesRegex(tools.PackageError, "Duplicate skill"):
            self.promote(replace=True)

    def test_overlay_mapping_duplicate_removal_and_rollback(self):
        agents = self.temp / "agents" / "skills"
        self.existing("natural-persian-writing")
        self.existing("natural-persian-writing", extra="Active variant\n", root=agents)
        self.existing("compatible-response", root=agents)
        self.sentinel()
        self.sentinel(agents)
        before_codex = tools.records(self.destination, selected=False)
        before_agents = tools.records(agents, selected=False)
        mapping = {"roots": [str(agents)], "destinations": {name: str(agents / name) for name in ["natural-persian-writing", "compatible-response", "hand-off"]},
                   "remove_duplicates": {"natural-persian-writing": [str(self.destination / "natural-persian-writing")]}}
        result = self.promote(mapping=mapping, replace=True)
        self.assertFalse((self.destination / "natural-persian-writing").exists())
        for name in ["natural-persian-writing", "compatible-response", "hand-off"]:
            self.assertEqual(tools.tree_hash(agents / name), tools.tree_hash(self.stage / name))
        self.assertEqual(result["changed_paths"], 27)
        tools.rollback(result["journal"], [self.destination, agents])
        self.assertEqual(before_codex, tools.records(self.destination, selected=False))
        self.assertEqual(before_agents, tools.records(agents, selected=False))

    def test_duplicate_mapping_cannot_remove_unrelated_or_escape_roots(self):
        for mapping in [{"remove_duplicates": {"unrelated": [str(self.destination / "unrelated")]}},
                        {"destinations": {"steps": str(self.temp / "other" / "skills" / "steps")}},
                        {"remove_duplicates": {"steps": [str(self.destination / "steps")]}}]:
            with self.subTest(mapping=mapping), self.assertRaises(tools.PackageError):
                self.promote(mapping=mapping, replace=True)

    def test_tampered_backup_refuses_rollback_without_destination_change(self):
        self.existing()
        result = self.promote(replace=True)
        data = tools.read_json(result["journal"])
        old = next(row for row in data["rows"] if row["backup"])
        (Path(old["backup"]) / "custom.txt").write_text("tampered backup")
        before = tools.records(self.destination, selected=False)
        with self.assertRaisesRegex(tools.PackageError, "Backup hash"):
            tools.rollback(result["journal"], [self.destination])
        self.assertEqual(before, tools.records(self.destination, selected=False))

    def test_untrusted_journal_cannot_expand_allowed_roots(self):
        result = self.promote()
        before = tools.records(self.destination, selected=False)
        data = tools.read_json(result["journal"])
        data["roots"] = [str(self.temp / "victim" / "skills")]
        tools.write_json(result["journal"], data)
        with self.assertRaisesRegex(tools.PackageError, "allowed roots"):
            tools.rollback(result["journal"], [self.destination])
        self.assertEqual(before, tools.records(self.destination, selected=False))

    def test_new_user_changes_after_install_are_preserved_on_rollback_refusal(self):
        result = self.promote()
        file = self.destination / "steps" / "user-change.txt"
        file.write_text("do not discard this")
        with self.assertRaisesRegex(tools.PackageError, "unrelated edits"):
            tools.rollback(result["journal"], [self.destination])
        self.assertEqual(file.read_text(), "do not discard this")

    def test_cli_verify_and_safe_crash_recovery(self):
        self.existing("apple-design")
        self.sentinel()
        before = tools.records(self.destination, selected=False)
        program = "import importlib.util,sys; s=importlib.util.spec_from_file_location('t',sys.argv[1]); t=importlib.util.module_from_spec(s); s.loader.exec_module(t); t.promote(*sys.argv[2:6],replace=True,crash_after=3)"
        child = subprocess.run([sys.executable, "-B", "-c", program, str(TOOL_PATH), str(self.package), str(self.stage), str(self.destination), str(self.backups)], capture_output=True, text=True)
        self.assertEqual(child.returncode, 86, child.stderr)
        journal = next(self.backups.glob("*/transaction.json"))
        self.assertEqual(tools.read_json(journal)["status"], "IN_PROGRESS")
        result = subprocess.run([sys.executable, "-B", str(TOOL_PATH), "rollback", "--journal", str(journal), "--allow-root", str(self.destination)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "ROLLED_BACK")
        self.assertEqual(before, tools.records(self.destination, selected=False))
        verify = subprocess.run([sys.executable, "-B", str(TOOL_PATH), "verify", "--package-root", str(self.package), "--stage-root", str(self.stage)], capture_output=True, text=True)
        self.assertEqual(verify.returncode, 0, verify.stderr)
        self.assertEqual(json.loads(verify.stdout)["status"], "STATIC_PASS")


if __name__ == "__main__":
    unittest.main(verbosity=2)
