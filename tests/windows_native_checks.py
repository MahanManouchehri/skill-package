"""Windows-only filesystem evidence; all writes stay in a new temporary fixture.

Run explicitly on Windows, in addition to test_package_tools.py. This is not a
simulation of junctions, sharing violations, or the Windows kernel lock backend.
"""
from __future__ import annotations

import ctypes
from ctypes import wintypes
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
from test_package_tools import make_package, tools, write_skill


class WindowsNativeTests(unittest.TestCase):
    def setUp(self):
        self.temp = Path(tempfile.mkdtemp(prefix="skill-windows-native-")).resolve()
        self.package = self.temp / "package"
        make_package(self.package)
        tools.build(self.package)
        self.stage = self.temp / "stage"
        shutil.copytree(self.package / "skills", self.stage)
        self.destination = self.temp / "profile" / ".codex" / "skills"
        self.backups = self.temp / "backups"
        self.junctions = []

    def tearDown(self):
        for junction in reversed(self.junctions):
            if junction.exists():
                os.rmdir(junction)  # Remove the junction, never its target.
        shutil.rmtree(self.temp)

    def junction(self, path, target):
        path.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            ["powershell.exe", "-NoLogo", "-NoProfile", "-NonInteractive", "-Command",
             "$ErrorActionPreference='Stop'; New-Item -ItemType Junction -Path $env:SKILL_TEST_JUNCTION "
             "-Target $env:SKILL_TEST_TARGET | Out-Null"],
            env={**os.environ, "SKILL_TEST_JUNCTION": str(path), "SKILL_TEST_TARGET": str(target)},
            capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(path.lstat().st_file_attributes & 0x400)
        self.junctions.append(path)

    def test_junction_ancestor_refused_without_following_target(self):
        target = self.temp / "junction-target"
        target.mkdir()
        (target / "keep.bin").write_bytes(b"original\x00\xff")
        before = tools.tree_hash(target)
        link = self.temp / "junction-link"
        self.junction(link, target)
        with self.assertRaisesRegex(tools.PackageError, "Reparse point"):
            tools.plan_install(self.package, self.stage, link / "skills")
        self.assertEqual(tools.tree_hash(target), before)
        self.assertFalse((target / "skills").exists())
        self.assertFalse(self.backups.exists())

    def test_unrelated_junction_is_preserved_and_catalog_does_not_traverse_it(self):
        target = self.temp / "outside-catalog"
        write_skill(target / "steps", "steps")
        before = tools.tree_hash(target)
        link = self.destination / "unrelated-junction"
        self.junction(link, target)
        self.assertEqual(tools.catalog_entries(self.destination), [])
        result = tools.promote(self.package, self.stage, self.destination, self.backups)
        self.assertEqual(result["status"], "COMMITTED")
        self.assertTrue(link.lstat().st_file_attributes & 0x400)
        self.assertEqual(tools.tree_hash(target), before)
        tools.rollback(result["journal"], [self.destination])
        self.assertEqual(tools.tree_hash(target), before)
        self.assertTrue(link.exists())

    def test_locked_original_failure_is_recoverable_without_losing_bytes(self):
        old = self.destination / "steps"
        write_skill(old, "steps")
        file = old / "private.bin"
        file.write_bytes(b"locked original\x00\xff")
        before = tools.records(self.destination, selected=False)
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                                      ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
        kernel.CreateFileW.restype = wintypes.HANDLE
        kernel.CloseHandle.argtypes = [wintypes.HANDLE]
        kernel.CloseHandle.restype = wintypes.BOOL
        # Allow reading/backups, deny FILE_SHARE_DELETE so the live rename fails.
        handle = kernel.CreateFileW(str(file), 0x80000000, 0x3, None, 3, 0, None)
        self.assertNotEqual(handle, ctypes.c_void_p(-1).value)
        try:
            with self.assertRaises((OSError, tools.PackageError)):
                tools.promote(self.package, self.stage, self.destination, self.backups, replace=True)
            self.assertEqual(tools.records(self.destination, selected=False), before)
        finally:
            kernel.CloseHandle(handle)
        # A sharing violation must remain visible; after it is removed a normal
        # retry, verified backup, and explicit rollback must still work.
        result = tools.promote(self.package, self.stage, self.destination, self.backups, replace=True)
        self.assertEqual(result["status"], "COMMITTED")
        tools.rollback(result["journal"], [self.destination])
        self.assertEqual(tools.records(self.destination, selected=False), before)

    def test_long_unicode_destination_round_trip_and_namespace_alias_refusal(self):
        # Hosted Windows must support ordinary long paths. Namespace aliases are
        # refused because their alternative spelling could bypass overlap guards.
        nested = self.temp / ("مسیر-" * 12) / ("long-" * 20) / ("deep-" * 20) / "profile" / "skills"
        with self.assertRaisesRegex(tools.PackageError, "namespace"):
            tools.plan_install(self.package, self.stage, Path("\\\\?\\" + str(self.package / "skills")))
        destination = nested
        self.assertGreater(len(str(destination)), 260)
        result = tools.promote(self.package, self.stage, destination, self.backups)
        self.assertEqual(result["status"], "COMMITTED")
        self.assertEqual(len(list(destination.iterdir())), 26)
        self.assertEqual(tools.promote(self.package, self.stage, destination, self.backups)["status"], "UNCHANGED")
        tools.rollback(result["journal"], [destination])
        self.assertEqual(list(destination.iterdir()), [])


if __name__ == "__main__":
    if os.name != "nt":
        raise SystemExit("WINDOWS_RUNTIME_UNVERIFIED: this driver requires an actual Windows host")
    if len(sys.argv) == 3 and sys.argv[1] == "--tree-hash":
        print(tools.tree_hash(Path(sys.argv[2])))
        raise SystemExit(0)
    unittest.main(verbosity=2)
