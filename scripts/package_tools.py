#!/usr/bin/env python3
"""Verify/build the v3 distribution and transactionally promote a verified staging tree.

No network, runtime configuration or plugin installation. Build is the only command
which changes the distribution. Promotion defaults to collision refusal; --replace
is a separate, explicit upgrade choice. See --help for the supported CLI contract.
"""
from __future__ import annotations

import argparse
import copy
from contextlib import contextmanager
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import uuid
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required; install scripts/requirements.txt in an isolated environment.") from exc

APPROVED_NAMES = frozenset("""apple-design architecture-review compatible-response db-impact
devil final-check full-plan hand-off multiple-pov natural-persian-writing
performance-review practical-test regression-check root-cause steps ui-ux-pro-max
integration-reliability test-engineering security-assurance docs-maintenance
maintenance-evolution skill-evals load-testing technical-proposal-discovery
release-management backup-recovery""".split())
SYSTEM_NAMES = frozenset("imagegen openai-docs review-agent skill-creator skill-installer".split())
GENERATED_DIRS = {"__pycache__", ".pytest_cache", "node_modules", ".venv", "logs", "temp", "tmp"}
GENERATED_FILES = {".DS_Store", "Thumbs.db"}
HASH = re.compile(r"^[a-f0-9]{64}$")
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TXID = re.compile(r"^\d{8}T\d{12}Z-[a-f0-9]{12}$")
TREE_ALGORITHM = "SHA256(UTF8(concat ordinal-sorted relative_path + NUL + lowercase file_sha256 + LF)); timestamps excluded"
INTEGRITY_ALGORITHM = "SHA256(UTF8(concat ordinal-sorted path + NUL + lowercase file SHA256 + LF))"


class PackageError(ValueError):
    """A failed validation or a safely refused operation."""


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def require(condition, message):
    if not condition:
        raise PackageError(message)


def absolute(path):
    # Do not resolve symlinks: their spelling must remain visible to the guard.
    return Path(os.path.abspath(os.fspath(path)))


def inside(path, root):
    return path == root or root in path.parents


def disjoint(a, b):
    return not inside(a, b) and not inside(b, a)


def no_links(path):
    """Reject symlinks/reparse points in an existing path and every ancestor."""
    path = absolute(path)
    for item in [path, *path.parents]:
        try:
            info = item.lstat()
        except FileNotFoundError:
            continue
        require(not stat.S_ISLNK(info.st_mode), f"Symlink is forbidden: {item}")
        require(not (getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)),
                f"Reparse point is forbidden: {item}")
    return path


def safe_relative(value):
    require(isinstance(value, str) and value and not any(ord(c) < 32 for c in value), "Invalid relative path")
    require("\\" not in value and ":" not in value and not value.startswith("/"), f"Unsafe relative path: {value}")
    parts = value.split("/")
    reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}
    for part in parts:
        require(part not in {"", ".", "..", ".system", ".git"}, f"Unsafe path component: {value}")
        require(not part.endswith((" ", ".")) and not any(c in part for c in '<>"|?*'), f"Nonportable path: {value}")
        require(part.split(".")[0].upper() not in reserved, f"Reserved Windows path: {value}")
    return PurePosixPath(value)


def safe_path(root, value):
    rel = safe_relative(value)
    root = no_links(root)
    path = root.joinpath(*rel.parts)
    require(inside(path, root) and path != root, f"Path escapes root: {value}")
    return no_links(path)


def walk_files(root, selected=True):
    """Ordinal path order; selected=True reproduces common.ps1's skill policy."""
    root = no_links(root)
    require(root.is_dir(), f"Missing tree: {root}")
    files = []

    def visit(folder):
        for child in folder.iterdir():
            no_links(child)  # Check before excluding .git or generated trees.
            if selected and child.name == ".git":
                continue
            if child.is_dir():
                if selected and child.name in GENERATED_DIRS:
                    continue
                visit(child)
            else:
                require(child.is_file(), f"Unsupported filesystem entry: {child}")
                if selected and (child.suffix in {".pyc", ".pyo"} or child.name in GENERATED_FILES):
                    continue
                files.append(child)
    visit(root)
    # .NET StringComparer.Ordinal orders UTF-16 code units, including astral names.
    return sorted(files, key=lambda p: p.relative_to(root).as_posix().encode("utf-16-be", "surrogatepass"))


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def records(root, selected=True):
    root = absolute(root)
    return [{"path": p.relative_to(root).as_posix(), "sha256": sha256_file(p), "bytes": p.stat().st_size}
            for p in walk_files(root, selected)]


def records_hash(rows):
    ordered = sorted(rows, key=lambda r: r["path"].encode("utf-16-be", "surrogatepass"))
    return hashlib.sha256("".join(f"{r['path']}\0{r['sha256']}\n" for r in ordered).encode("utf-8")).hexdigest()


def tree_hash(root, selected=True):
    return records_hash(records(root, selected))


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    output = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        require(isinstance(key, str) and key not in output, "YAML has duplicate/non-string mapping keys")
        output[key] = loader.construct_object(value_node, deep=deep)
    return output


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def strict_yaml(text, label):
    require(len(text.encode("utf-8")) <= 65536, f"YAML exceeds 64 KiB: {label}")
    try:
        require(not any(isinstance(t, (yaml.tokens.AnchorToken, yaml.tokens.AliasToken)) for t in yaml.scan(text)),
                f"YAML anchors/aliases are unsupported: {label}")
        return yaml.load(text, Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise PackageError(f"Invalid YAML: {label}: {exc}") from exc


def metadata(path):
    no_links(path)
    text = Path(path).read_text(encoding="utf-8-sig")
    match = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---(?:\s|$)", text, re.S)
    require(match is not None, f"Missing frontmatter: {path}")
    front = strict_yaml(match.group(1), str(path))
    require(isinstance(front, dict), f"Frontmatter must be a mapping: {path}")
    name, description = front.get("name"), front.get("description")
    require(isinstance(name, str) and len(name) <= 64 and bool(NAME.fullmatch(name)), f"Invalid skill name: {path}")
    require(isinstance(description, str) and bool(description.strip()) and len(description) <= 1024,
            f"Invalid skill description: {path}")
    return {**front, "_strict_yaml_valid": True,
            "_raw_frontmatter_sha256": hashlib.sha256(match.group(1).encode("utf-8")).hexdigest()}


def legacy_name(path):
    """Only identify an existing folder; never execute or trust its body as authority.

    Older package releases shipped one malformed description. Requiring strict
    YAML here would make a backed-up repair of that known defect impossible.
    """
    no_links(path)
    text = Path(path).read_text(encoding="utf-8-sig")
    match = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---(?:\s|$)", text, re.S)
    require(match is not None, f"Unrecognized existing skill: {path}")
    names = re.findall(r"(?m)^name:\s*([^\r\n]+)$", match.group(1))
    require(len(names) == 1, f"Ambiguous existing skill name: {path}")
    value = names[0].strip().strip("\"'")
    require(re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]*", value) is not None, f"Invalid existing skill name: {path}")
    return value


def relative_links(root, boundary=None):
    """Validate actual Markdown links, retaining common.ps1's documented examples."""
    root = no_links(root)
    boundary = no_links(boundary or root)
    result = []
    for file in walk_files(root):
        if file.suffix.lower() != ".md":
            continue
        text = file.read_text(encoding="utf-8-sig")
        for match in re.finditer(r"\[[^\]\r\n]*\]\(([^)\r\n]+)\)", text):
            ref = match.group(1).strip().split(' "')[0].strip("<>")
            if not ref or ref.startswith(("#", "/", "$", "{")) or re.match(r"^[a-zA-Z][\w+.-]*:", ref):
                continue  # Runtime examples/remote links, not distribution resources.
            value = unquote(urlsplit(ref).path)
            require("\\" not in value and "\0" not in value, f"Unsafe link in {file}: {ref}")
            target = no_links(absolute(file.parent / value))
            require(inside(target, boundary) and target.exists(), f"Broken/escaping Markdown reference in {file}: {ref}")
            result.append({"file": file.relative_to(root).as_posix(), "target": ref})
    return result


def validate_agent_yaml(root):
    path = root / "agents" / "openai.yaml"
    if not path.exists():
        return
    agent = strict_yaml(path.read_text(encoding="utf-8-sig"), str(path))
    require(isinstance(agent, dict), f"Agent metadata must be a mapping: {path}")
    for key in ("icon_small", "icon_large"):
        value = agent.get("interface", {}).get(key)
        if value:
            # Metadata paths conventionally start './'; normalize that one prefix.
            resource = safe_path(root, value.removeprefix("./"))
            require(resource.is_file(), f"Missing agent resource: {resource}")
    policy = agent.get("policy", {})
    if "allow_implicit_invocation" in policy:
        require(type(policy["allow_implicit_invocation"]) is bool, f"Invalid invocation policy: {path}")


def scan_secrets(root):
    rules = {
        "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
        "github_token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
        "openai_key": re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{32,}\b"),
        "aws_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "credential_assignment": re.compile(r"(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[=:]\s*[\"'][A-Za-z0-9+/=_-]{24,}[\"']", re.I),
    }
    sensitive = re.compile(r"(^\.env($|\.)|^auth\.json$|^credentials($|\.)|^id_(rsa|ed25519)$|\.pfx$|\.p12$|^cookies?($|\.))", re.I)
    found = []
    for file in distribution_files(root):
        if sensitive.search(file.name):
            found.append({"file": file.relative_to(root).as_posix(), "rule": "sensitive_filename"})
        content = file.read_bytes().decode("utf-8", errors="replace")
        for name, pattern in rules.items():
            if pattern.search(content):
                found.append({"file": file.relative_to(root).as_posix(), "rule": name})
    return found  # Never include matched credential text.


def distribution_files(root):
    # Existing integrity contract: all distribution files, except .git and itself.
    root = no_links(root)
    files = []
    def visit(folder):
        for item in folder.iterdir():
            no_links(item)
            if item.name == ".git":
                continue
            if item.is_dir():
                visit(item)
            else:
                require(item.is_file(), f"Unsupported distribution entry: {item}")
                if item != root / "package-integrity.json":
                    files.append(item)
    visit(root)
    return sorted(files, key=lambda p: p.relative_to(root).as_posix().encode("utf-16-be", "surrogatepass"))


def read_json(path):
    no_links(path)
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"Duplicate JSON key in {path}: {key}")
            result[key] = value
        return result
    try:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
    except (ValueError, OSError) as exc:
        raise PackageError(f"Cannot read JSON: {path}: {exc}") from exc


def write_json(path, value):
    path = no_links(path)
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    temp = path.with_name(path.name + ".new-" + uuid.uuid4().hex)
    try:
        with open(temp, "xb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp, path)
        sync_directory(path.parent)
    finally:
        if temp.exists():
            temp.unlink()


def sync_directory(path):
    if os.name != "nt":
        descriptor = os.open(path, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


def validate_rows(rows, root, label):
    require(isinstance(rows, list), f"Missing file records: {label}")
    names = []
    for row in rows:
        require(isinstance(row, dict), f"Invalid file record: {label}")
        safe_path(root, row.get("path"))
        require(bool(HASH.fullmatch(str(row.get("sha256", "")))), f"Invalid SHA256: {label}")
        require(type(row.get("bytes")) is int and row["bytes"] >= 0, f"Invalid byte length: {label}")
        names.append(row["path"].casefold())
    require(len(names) == len(set(names)), f"Duplicate file paths: {label}")


def read_manifest(root):
    root = no_links(root)
    manifest = read_json(root / "skills-manifest.json")
    require(manifest.get("schema_version") == 1, "Unsupported manifest schema")
    entries = manifest.get("skills", [])
    require(isinstance(entries, list) and all(isinstance(e, dict) and type(e.get("installable")) is bool for e in entries), "Invalid skill entries")
    personal = [e for e in entries if e["installable"]]
    managed = [e for e in entries if not e["installable"]]
    require(len(personal) == manifest.get("expected_user_global") and len(managed) == manifest.get("expected_plugin_managed"), "Manifest counts differ")
    catalogs = [str(e.get("catalog_name", "")).casefold() for e in entries]
    require(all(catalogs) and len(catalogs) == len(set(catalogs)), "Duplicate/empty catalog names")
    names = [e.get("skill_name") for e in personal]
    require(len(names) == len(set(names)), "Duplicate personal names")
    require(set(names) <= APPROVED_NAMES and len(set(names) & SYSTEM_NAMES) == 0, "Unexpected/system personal skill")
    for entry in entries:
        path = safe_path(root, entry.get("physical_path_in_package"))
        safe_path(root, entry.get("snapshot_root"))
        if entry["installable"]:
            name = entry["skill_name"]
            require(entry.get("kind") == "user-global" and entry.get("destination_relative") == name and entry.get("catalog_name") == name
                    and entry["physical_path_in_package"] == f"skills/{name}" and entry["snapshot_root"] == f"skills/{name}", "Unsafe personal mapping")
        else:
            require(entry.get("kind") == "plugin-managed" and entry["physical_path_in_package"].startswith("managed/plugin-skills/"), "Unsafe managed mapping")
        validate_rows(entry.get("files"), path, entry["catalog_name"])
        require(entry.get("file_count") == len(entry["files"]) and HASH.fullmatch(str(entry.get("tree_hash_sha256", ""))), "Invalid tree metadata")
    return manifest


def verify_skill(root, entry, boundary=None, strict=True):
    expected = entry["files"]
    actual = records(root)
    require(actual == expected, f"File hashes/counts differ: {entry['catalog_name']}")
    # Excluded generated files cannot conceal stale state in a staged install.
    require(len(walk_files(root, selected=False)) == len(actual), f"Unexpected excluded files: {root}")
    require(records_hash(actual) == entry["tree_hash_sha256"], f"Tree hash differs: {entry['catalog_name']}")
    if strict:
        md = metadata(root / "SKILL.md")
        require(md["name"] == entry["skill_name"] and md["description"] == entry["description"], f"Metadata differs: {entry['catalog_name']}")
        discoverable = [p.relative_to(root).as_posix() for p in walk_files(root) if p.name == "SKILL.md"]
        require(discoverable == ["SKILL.md"], f"Nested discoverable skill: {root}")
        validate_agent_yaml(root)
    else:
        require(legacy_name(root / "SKILL.md") == entry["skill_name"], f"Managed metadata differs: {entry['catalog_name']}")
    relative_links(root, boundary)


def verify_package(root, stage_root=None):
    root = no_links(root)
    manifest = read_manifest(root)
    require(manifest["expected_user_global"] == 26 and manifest["expected_plugin_managed"] == 16, "Release must contain 26 personal / 16 managed entries")
    personal = [e for e in manifest["skills"] if e["installable"]]
    require({e["skill_name"] for e in personal} == APPROVED_NAMES, "Approved personal inventory differs")
    physical = {p.name for p in (root / "skills").iterdir()}
    require(physical == APPROVED_NAMES, "Physical skill directories differ from manifest")
    integrity = read_json(root / "package-integrity.json")
    require(integrity.get("schema_version") == 1, "Unsupported integrity schema")
    expected = integrity.get("files")
    validate_rows(expected, root, "package-integrity")
    actual = [{"path": p.relative_to(root).as_posix(), "sha256": sha256_file(p), "bytes": p.stat().st_size} for p in distribution_files(root)]
    require(actual == expected, "Package integrity file/hash coverage differs (tampered, omitted or extra file)")
    require(records_hash(actual) == integrity.get("package_tree_hash_sha256"), "Package aggregate hash differs")
    require((root / "VERSION").read_text().strip() == manifest.get("package_version"), "VERSION and manifest differ")
    for entry in manifest["skills"]:
        verify_skill(safe_path(root, entry["physical_path_in_package"]), entry, safe_path(root, entry["snapshot_root"]), entry["installable"])
    for snapshot in manifest.get("snapshot_trees", []):
        snapshot_root = safe_path(root, snapshot["snapshot_root"])
        current = records(snapshot_root)
        require(current == snapshot["files"] and len(current) == snapshot["file_count"]
                and records_hash(current) == snapshot["package_tree_hash_sha256"], f"Snapshot tree differs: {snapshot_root}")
    candidates = scan_secrets(root)
    require(not candidates, "Secret/sensitive candidates: " + json.dumps(candidates, ensure_ascii=False))
    if stage_root is not None:
        verify_stage(stage_root, manifest)
    return {"status": "STATIC_PASS", "version": manifest["package_version"], "personal_skills": len(personal),
            "managed_snapshots": 16, "distribution_files": len(actual), "package_tree_hash_sha256": records_hash(actual), "verified_utc": utc_now()}


def verify_stage(root, manifest):
    root = no_links(root)
    require(root.is_dir(), f"Missing staged root: {root}")
    require({p.name for p in root.iterdir()} == APPROVED_NAMES, "Stage must contain exactly the 26 approved directories")
    for entry in manifest["skills"]:
        if entry["installable"]:
            verify_skill(safe_path(root, entry["destination_relative"]), entry)


def build(root):
    """Explicitly rebuild personal metadata/hashes while preserving managed records."""
    root = no_links(root)
    old = read_manifest(root)
    updated = copy.deepcopy(old)
    version = (root / "VERSION").read_text().strip()
    require(re.fullmatch(r"3\.\d+\.\d+", version), "Only compatible v3 versions are supported")
    directories = {p.name for p in (root / "skills").iterdir()}
    require(directories == APPROVED_NAMES, "Build requires exactly the 26 approved personal skill directories")
    existing = {e["skill_name"]: e for e in old["skills"] if e["installable"]}
    personal = []
    for name in sorted(APPROVED_NAMES):
        directory = safe_path(root, f"skills/{name}")
        md = metadata(directory / "SKILL.md")
        require(md["name"] == name, f"Name/directory mismatch: {name}")
        files = records(directory)
        require(len(files) == len(walk_files(directory, selected=False)), f"Remove generated/Git files before build: {directory}")
        require([f["path"] for f in files if Path(f["path"]).name == "SKILL.md"] == ["SKILL.md"], f"Nested discoverable skill: {directory}")
        validate_rows(files, directory, name)
        relative_links(directory)
        validate_agent_yaml(directory)
        entry = copy.deepcopy(existing.get(name, {}))
        if entry:
            entry.setdefault("baseline_source_tree_hash_sha256", entry.get("source_tree_hash_sha256"))
        else:
            entry.update({"physical_source": f"repository:skills/{name}", "source_origin": f"repository:skills/{name}",
                          "source_tree_hash_sha256": None, "dependencies": [], "required_external_tools": [],
                          "required_runtime_capabilities": ["Standard Codex skill support"], "platform_requirements": [],
                          "plugin_provider": None, "plugin_name": None, "plugin_version": None, "plugin_id": None, "plugin_id_basis": None,
                          "notes": [], "symlinks": [], "platform_assumption_evidence": []})
        entry.update({"catalog_name": name, "kind": "user-global", "installable": True, "physical_path_in_package": f"skills/{name}",
                      "snapshot_root": f"skills/{name}", "destination_relative": name, "skill_name": name, "description": md["description"],
                      "frontmatter": md, "portability": "PORTABLE_WITH_DEPENDENCIES" if name in {"devil", "hand-off", "ui-ux-pro-max"} else "PORTABLE",
                      "file_count": len(files), "tree_hash_sha256": records_hash(files), "files": files,
                      "discoverable_entries": [f["path"] for f in files if Path(f["path"]).name == "SKILL.md"],
                      "relative_links": relative_links(directory), "restore_method": "Official skill-installer into staging, then scripts/package_tools.py promote",
                      "post_enable_verification": "Verify staged/live hashes and inspect a fresh Codex skill catalog."})
        if name == "ui-ux-pro-max":
            entry.setdefault("baseline_notes", copy.deepcopy(entry.get("notes", [])))
            entry.setdefault("baseline_platform_assumption_evidence", copy.deepcopy(entry.get("platform_assumption_evidence", [])))
            entry["dependencies"] = ["Python 3 for optional local search; resolve the actual installed skill directory"]
            entry["notes"] = ["Search uses the actual loaded skill directory; no plugin environment variable is required."]
            entry["platform_assumption_evidence"] = []
        entry.setdefault("baseline_platform_requirements", copy.deepcopy(entry.get("platform_requirements", [])))
        entry["platform_requirements"] = (["PowerShell 5.1+ for the optional skill validator"] if name == "devil"
                                           else ["Python 3 for optional skill helpers"] if name in {"hand-off", "ui-ux-pro-max"}
                                           else [])
        for key in ("agents", "references", "scripts", "templates", "assets"):
            entry[key] = [f["path"] for f in files if f["path"].startswith(key + "/")]
        entry["supporting_configs"] = [f["path"] for f in files if f["path"].endswith((".yaml", ".yml", ".json", ".toml")) and not f["path"].startswith("agents/")]
        personal.append(entry)
    updated["skills"] = personal + [copy.deepcopy(e) for e in old["skills"] if not e["installable"]]
    # Personal source hashes remain historical provenance; do not assert equality
    # to the original machine after a deliberate behavior upgrade.
    old_snapshots = {s["snapshot_root"]: s for s in old.get("snapshot_trees", [])}
    snapshots = [copy.deepcopy(s) for s in old.get("snapshot_trees", []) if s["snapshot_root"].startswith("managed/")]
    for entry in personal:
        previous = old_snapshots.get(entry["snapshot_root"], {})
        source_hash = previous.get("source_selected_tree_hash_sha256", entry.get("source_tree_hash_sha256"))
        snapshots.append({"snapshot_root": entry["snapshot_root"], "source_origin": entry["source_origin"], "file_count": entry["file_count"],
                          "source_selected_tree_hash_sha256": source_hash, "package_tree_hash_sha256": entry["tree_hash_sha256"],
                          "source_package_equal": source_hash == entry["tree_hash_sha256"] if source_hash else None,
                          "files": entry["files"], "provenance_note": "Historical source retained; package is intentionally upgraded in v3.1."})
    updated.update({"package_version": version, "created_utc": utc_now(), "expected_user_global": 26,
                    "tree_hash_algorithm": TREE_ALGORITHM, "snapshot_trees": snapshots,
                    "catalog_basis": "26 personal skills: 16 retained/upgraded and 10 approved specialists; 16 managed audit-only snapshots preserved."})
    write_json(root / "skills-manifest.json", updated)
    rows = [{"path": p.relative_to(root).as_posix(), "sha256": sha256_file(p), "bytes": p.stat().st_size} for p in distribution_files(root)]
    write_json(root / "package-integrity.json", {"schema_version": 1, "algorithm": INTEGRITY_ALGORITHM,
               "excluded": [".git/", "package-integrity.json"], "package_tree_hash_sha256": records_hash(rows), "files": rows})
    return verify_package(root)


def protected_root(path):
    path = no_links(path)
    require(path.name == "skills" and path.parent != path.anchor and len(path.parts) >= 3,
            f"Destination must be an explicit personal .../skills root: {path}")
    require(not any(p.casefold() in {".system", "plugins", "cache", "managed", "node_modules"} for p in path.parts),
            f"System/plugin/managed destination is protected: {path}")
    return path


def protected_backup(path):
    path = no_links(path)
    require(not any(p.casefold() in {".system", "plugins", "cache", "managed"} for p in path.parts),
            f"Backup must be outside system/plugin/managed paths: {path}")
    return path


def normalize_mapping(destination_root, mapping=None):
    mapping = mapping or {}
    require(isinstance(mapping, dict) and set(mapping) <= {"roots", "destinations", "remove_duplicates"}, "Invalid destination mapping")
    default = protected_root(destination_root)
    roots = sorted({default, *(protected_root(p) for p in mapping.get("roots", []))}, key=str)
    require(all(disjoint(a, b) for i, a in enumerate(roots) for b in roots[i + 1:]), "Overlapping destination roots")
    destinations = mapping.get("destinations", {})
    removals = mapping.get("remove_duplicates", {})
    require(isinstance(destinations, dict) and isinstance(removals, dict), "Mapping must use objects")
    require(set(destinations) <= APPROVED_NAMES and set(removals) <= APPROVED_NAMES, "Mapping contains unapproved names")
    rows = []
    for name in sorted(APPROVED_NAMES):
        dest = no_links(destinations.get(name, default / name))
        require(dest.parent in roots and dest.name == name, f"Destination is not a direct approved child: {dest}")
        rows.append({"skill": name, "destination": str(dest), "operation": "PROMOTE"})
        extra = removals.get(name, [])
        require(isinstance(extra, list), "remove_duplicates values must be arrays")
        for item in extra:
            duplicate = no_links(item)
            require(duplicate.parent in roots and duplicate.name == name, f"Unsafe duplicate removal: {duplicate}")
            rows.append({"skill": name, "destination": str(duplicate), "operation": "REMOVE_DUPLICATE"})
    paths = [r["destination"].casefold() for r in rows]
    require(len(paths) == len(set(paths)), "Duplicate/overlapping destination operations")
    return roots, rows


def catalog_entries(root):
    """Read names without treating bodies as instructions; no system traversal."""
    if not root.exists():
        return []
    found = []
    def visit(folder):
        for item in folder.iterdir():
            if item.name in {".system", ".git"} or item.is_symlink():
                continue
            if item.is_dir():
                visit(item)
            elif item.name == "SKILL.md":
                try:
                    name = legacy_name(item)
                except PackageError:
                    continue  # Unknown unrelated content is preserved, not rewritten.
                found.append((name, item.parent))
    visit(root)
    return found


def preservation_fingerprint(roots, owned_paths):
    """Hash unrelated files; record links as links, never traverse their targets."""
    owned = set(map(absolute, owned_paths))
    output = []
    def visit(path, root):
        if path in owned:
            return
        info = path.lstat()
        rel = str(path.relative_to(root))
        if stat.S_ISLNK(info.st_mode):
            output.append((str(root), rel, "symlink", os.readlink(path)))
        elif stat.S_ISDIR(info.st_mode):
            output.append((str(root), rel, "directory"))
            for item in sorted(path.iterdir()):
                visit(item, root)
        elif stat.S_ISREG(info.st_mode):
            output.append((str(root), rel, "file", sha256_file(path), stat.S_IMODE(info.st_mode)))
        else:
            output.append((str(root), rel, "other", info.st_mode))
    for root in roots:
        if root.exists():
            for item in sorted(root.iterdir()):
                visit(item, root)
    return hashlib.sha256(json.dumps(output, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()


def plan_install(package_root, stage_root, destination_root, mapping=None, replace=False):
    package_root, stage_root = no_links(package_root), no_links(stage_root)
    verify_package(package_root, stage_root)
    require(disjoint(package_root, stage_root), "Stage must be disjoint from the package")
    manifest = read_manifest(package_root)
    expected = {e["skill_name"]: e for e in manifest["skills"] if e["installable"]}
    roots, rows = normalize_mapping(destination_root, mapping)
    require(all(disjoint(root, package_root) and disjoint(root, stage_root) for root in roots), "Destination/package/stage overlap")
    authorized = {(r["skill"], Path(r["destination"])) for r in rows}
    managed_names = {e["skill_name"] for e in manifest["skills"] if not e["installable"]}
    for root in roots:
        for name, physical in catalog_entries(root):
            require(name not in managed_names, f"Managed skill manually copied into personal root: {name}")
            if name in APPROVED_NAMES:
                require((name, physical) in authorized, f"Duplicate skill needs an explicit mapping: {name} at {physical}")
    for row in rows:
        dest = Path(row["destination"])
        if dest.exists():
            require(dest.is_dir() and (dest / "SKILL.md").is_file(), f"Unrecognized directory collision: {dest}")
            require(legacy_name(dest / "SKILL.md") == row["skill"], f"Different skill occupies destination: {dest}")
            original = tree_hash(dest, selected=False)
        else:
            original = None
        row.update({"original_hash": original, "installed_hash": expected[row["skill"]]["tree_hash_sha256"] if row["operation"] == "PROMOTE" else None})
        if row["operation"] == "REMOVE_DUPLICATE":
            row["action"] = "REMOVE_DUPLICATE" if original is not None else "UNCHANGED"
        else:
            row["action"] = "UNCHANGED" if original == row["installed_hash"] else ("REPLACE" if original else "INSTALL")
        require(replace or row["action"] not in {"REPLACE", "REMOVE_DUPLICATE"}, f"Collision; explicit --replace is required: {dest}")
    return {"status": "PLAN", "version": manifest["package_version"], "package_root": str(package_root), "stage_root": str(stage_root),
            "roots": [str(r) for r in roots], "rows": rows,
            "owned_paths": [r["destination"] for r in rows],
            "preserved_fingerprint": preservation_fingerprint(roots, [r["destination"] for r in rows])}


def acquire_locks(roots, transaction_id, journal):
    owned = []
    try:
        for root in roots:
            root.parent.mkdir(parents=True, exist_ok=True)
            lock = no_links(root.parent / ".skill-package-install.lock")
            descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
                json.dump({"transaction_id": transaction_id, "pid": os.getpid(), "journal": str(journal)}, stream)
                stream.flush()
                os.fsync(stream.fileno())
            owned.append(str(lock))
        return owned
    except BaseException:
        release_locks(owned, transaction_id)
        raise


def release_locks(paths, transaction_id):
    for item in paths:
        path = no_links(item)
        if path.exists():
            require(read_json(path).get("transaction_id") == transaction_id, f"Lock ownership changed; preserving it: {path}")
            path.unlink()


def scratch_for(root, transaction_id):
    return no_links(root.parent / (".skill-package-stage-" + transaction_id))


def clean_scratch(root, transaction_id):
    scratch = scratch_for(root, transaction_id)
    if scratch.exists():
        marker = scratch / ".owner.json"
        require(marker.is_file() and read_json(marker).get("transaction_id") == transaction_id, f"Scratch ownership missing: {scratch}")
        walk_files(scratch, selected=False)
        shutil.rmtree(scratch)


def current_hash(path):
    path = no_links(path)
    return tree_hash(path, selected=False) if path.exists() else None


def promote(package_root, stage_root, destination_root, backup_parent, mapping=None, replace=False, *, fail_after=None, crash_after=None):
    """Promote all approved skills. Fault injection arguments are test-only APIs."""
    plan = plan_install(package_root, stage_root, destination_root, mapping, replace)
    changed = [r for r in plan["rows"] if r["action"] != "UNCHANGED"]
    if not changed:
        return {**plan, "status": "UNCHANGED", "personal_verified": 26, "backup_root": None}
    roots = list(map(Path, plan["roots"]))
    backup_parent = protected_backup(backup_parent)
    require(all(disjoint(backup_parent, p) for p in [Path(plan["package_root"]), Path(plan["stage_root"]), *roots]), "Backup root overlaps source/stage/destination")
    transaction_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ-") + uuid.uuid4().hex[:12]
    backup = backup_parent / transaction_id
    journal_path = backup / "transaction.json"
    locks = acquire_locks(roots, transaction_id, journal_path)
    journal = {**plan, "schema_version": 1, "transaction_id": transaction_id, "pid": os.getpid(), "started_utc": utc_now(),
               "status": "PREPARING", "backup_root": str(backup), "locks": locks, "rows": changed}
    try:
        backup.mkdir(parents=True)
        (backup / "backups").mkdir()
        for root in roots:
            scratch = scratch_for(root, transaction_id)
            scratch.mkdir()
            write_json(scratch / ".owner.json", {"transaction_id": transaction_id})
            (scratch / "incoming").mkdir()
            (scratch / "previous").mkdir()
        # All copies and backups must be complete and hash-verified BEFORE any
        # destination is renamed. The journal records exact paths and hashes.
        for index, row in enumerate(changed):
            destination = Path(row["destination"])
            scratch = scratch_for(destination.parent, transaction_id)
            row.update({"index": index, "state": "READY", "backup": None,
                        "incoming": str(scratch / "incoming" / f"{index:03}-{row['skill']}"),
                        "previous": str(scratch / "previous" / f"{index:03}-{row['skill']}")})
            require(current_hash(destination) == row["original_hash"], f"Destination changed during preparation: {destination}")
            if row["original_hash"] is not None:
                target = backup / "backups" / f"{index:03}-{row['skill']}"
                shutil.copytree(destination, target, copy_function=shutil.copy2)
                require(tree_hash(target, selected=False) == row["original_hash"] == current_hash(destination), f"Backup verification failed: {destination}")
                row["backup"] = str(target)
            if row["operation"] == "PROMOTE":
                shutil.copytree(Path(stage_root) / row["skill"], row["incoming"], copy_function=shutil.copy2)
                require(current_hash(row["incoming"]) == row["installed_hash"], f"Promotion staging hash failed: {row['skill']}")
        journal["status"] = "PREPARED"
        write_json(journal_path, journal)
        journal["status"] = "IN_PROGRESS"
        write_json(journal_path, journal)
        for count, row in enumerate(changed, 1):
            destination = Path(row["destination"])
            no_links(destination)
            require(current_hash(destination) == row["original_hash"], f"Destination changed before promotion: {destination}")
            # Write intent before the first rename; rollback handles a crash at
            # either side of either rename without assuming a complete install.
            row["state"] = "INTENT"
            write_json(journal_path, journal)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if row["original_hash"] is not None:
                os.replace(destination, row["previous"])
            if row["operation"] == "PROMOTE":
                os.replace(row["incoming"], destination)
            sync_directory(destination.parent)
            row["state"] = "PROMOTED"
            write_json(journal_path, journal)
            if fail_after == count:
                raise PackageError("Injected isolated-fixture promotion failure")
            if crash_after == count:
                os._exit(86)  # Only callable via a test importing the API.
        for row in plan["rows"]:
            expected = row["installed_hash"]
            require(current_hash(row["destination"]) == expected, f"Post-install hash differs: {row['destination']}")
        require(preservation_fingerprint(roots, [r["destination"] for r in plan["rows"]]) == plan["preserved_fingerprint"], "Unrelated/system content changed")
        journal.update({"status": "COMMITTED", "completed_utc": utc_now(), "personal_verified": 26,
                        "managed_snapshots_installed": 0, "unrelated_unchanged": True})
        write_json(journal_path, journal)
    except BaseException as exc:
        if journal_path.exists():
            try:
                rollback(journal_path, roots, _in_process=True)
            except BaseException as rollback_exc:
                raise PackageError(f"Promotion failed; recovery required from {journal_path}: {rollback_exc}") from exc
        else:
            # PREPARING never mutates a destination; only owned scratch can go.
            for root in roots:
                clean_scratch(root, transaction_id)
            release_locks(locks, transaction_id)
        raise
    for root in roots:
        clean_scratch(root, transaction_id)
    release_locks(locks, transaction_id)
    return {"status": "COMMITTED", "version": plan["version"], "personal_verified": 26, "backup_root": str(backup),
            "journal": str(journal_path), "roots": plan["roots"], "changed_paths": len(changed), "unrelated_unchanged": True}


def validate_journal(path, allowed_roots):
    """The caller supplies trusted scope; a journal cannot grant itself authority."""
    path = no_links(path)
    protected_backup(path.parent)
    require(path.name == "transaction.json" and TXID.fullmatch(path.parent.name), "Not a recognized transaction journal path")
    require(path.stat().st_size < 1024 * 1024, "Oversized transaction journal")
    data = read_json(path)
    tid = data.get("transaction_id", "")
    require(TXID.fullmatch(tid) and tid == path.parent.name and data.get("schema_version") == 1, "Invalid transaction identity")
    require(absolute(data.get("backup_root", "")) == path.parent, "Journal backup path does not match its location")
    roots = sorted({protected_root(p) for p in allowed_roots}, key=str)
    require(roots and [str(p) for p in roots] == sorted(data.get("roots", [])), "Explicit allowed roots do not match journal scope")
    require(all(disjoint(path.parent, root) for root in roots), "Backup must be outside destinations")
    owned = data.get("owned_paths", [])
    require(isinstance(owned, list) and 26 <= len(owned) <= 52 and len(owned) == len(set(owned)), "Invalid journal owned paths")
    for item in owned:
        owned_path = no_links(item)
        require(owned_path.parent in roots and owned_path.name in APPROVED_NAMES, "Unsafe journal ownership scope")
    expected_locks = [str(root.parent / ".skill-package-install.lock") for root in roots]
    require(data.get("locks") == expected_locks, "Unexpected journal lock paths")
    require(data.get("status") in {"PREPARED", "IN_PROGRESS", "COMMITTED", "ROLLING_BACK", "ROLLED_BACK"}, "Invalid journal state")
    rows = data.get("rows", [])
    require(isinstance(rows, list) and 0 < len(rows) <= 52, "Invalid journal row count")
    seen = set()
    for index, row in enumerate(rows):
        require(isinstance(row, dict) and row.get("skill") in APPROVED_NAMES and row.get("index") == index, "Invalid journal skill/index")
        dest = no_links(row.get("destination", ""))
        require(dest.parent in roots and dest.name == row["skill"] and str(dest).casefold() not in seen, "Unsafe/duplicate journal destination")
        require(str(dest) in owned, "Journal operation outside declared ownership")
        seen.add(str(dest).casefold())
        require(row.get("operation") in {"PROMOTE", "REMOVE_DUPLICATE"} and row.get("state") in {"READY", "INTENT", "PROMOTED", "ROLLBACK_INTENT", "RESTORED"}, "Invalid journal operation/state")
        original = row.get("original_hash")
        installed = row.get("installed_hash")
        require(original is None or (isinstance(original, str) and HASH.fullmatch(original)), "Invalid original journal hash")
        require((row["operation"] == "PROMOTE" and isinstance(installed, str) and HASH.fullmatch(installed))
                or (row["operation"] == "REMOVE_DUPLICATE" and installed is None), "Invalid installed journal hash")
        expected_backup = path.parent / "backups" / f"{index:03}-{row['skill']}"
        require(row.get("backup") == (str(expected_backup) if original is not None else None), "Unsafe journal backup")
        if original is not None:
            require(current_hash(expected_backup) == original, "Backup hash differs; refusing destructive recovery")
        scratch = scratch_for(dest.parent, tid)
        for field, sub in (("incoming", "incoming"), ("previous", "previous")):
            require(row.get(field) == str(scratch / sub / f"{index:03}-{row['skill']}"), f"Unsafe journal {field}")
    return data, roots


def process_alive(pid):
    if not isinstance(pid, int) or pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


@contextmanager
def recovery_locks(journal, roots, in_process=False):
    """Hold kernel locks on the installation-lock inodes during all recovery.

    File existence alone cannot serialize two recoveries of a crashed installer.
    Kernel ownership is automatically released on process death; the immutable
    JSON marker stays usable for the next validated recovery.
    """
    handles, created = [], []
    admitted = False
    try:
        for root in roots:
            path = no_links(root.parent / ".skill-package-install.lock")
            path.parent.mkdir(parents=True, exist_ok=True)
            fresh = False
            flags = os.O_RDWR | getattr(os, "O_BINARY", 0)
            try:
                descriptor = os.open(path, flags | os.O_CREAT | os.O_EXCL, 0o600)
                fresh = True
            except FileExistsError:
                descriptor = os.open(path, flags)
            stream = os.fdopen(descriptor, "r+b")
            handles.append(stream)
            if fresh:
                created.append((path, os.fstat(stream.fileno())))
                marker = {"transaction_id": journal["transaction_id"], "pid": os.getpid(), "journal": journal["backup_root"] + "/transaction.json"}
                stream.write(json.dumps(marker).encode("utf-8"))
                stream.flush()
                os.fsync(stream.fileno())
            try:
                stream.seek(0)
                if os.name == "nt":
                    import msvcrt
                    msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                raise PackageError(f"Another recovery holds the lock: {path}") from exc
            require(os.path.samestat(os.fstat(stream.fileno()), no_links(path).stat()), "Recovery lock inode changed")
            stream.seek(0)
            try:
                owner = json.loads(stream.read().decode("utf-8"))
            except (ValueError, UnicodeError) as exc:
                raise PackageError(f"Invalid existing recovery lock: {path}") from exc
            require(owner.get("transaction_id") == journal["transaction_id"], f"Another transaction owns the lock: {path}")
            require(fresh or in_process or not process_alive(owner.get("pid")), "Installer still holds a live transaction lock")
        admitted = True
        yield
    finally:
        for stream in reversed(handles):
            stream.close()  # Kernel locks also release automatically on crash.
        if not admitted:
            # Only files created by this failed acquisition belong to us.
            for path, identity in reversed(created):
                if path.exists() and os.path.samestat(identity, no_links(path).stat()):
                    path.unlink()


def rollback(journal_path, allowed_roots, *, _in_process=False):
    # The first pass rejects untrusted scope before creating any lock. Re-read
    # under the exclusive kernel claim before deciding or changing live state.
    journal, roots = validate_journal(journal_path, allowed_roots)
    with recovery_locks(journal, roots, _in_process):
        result = _rollback_locked(journal_path, roots, _in_process=_in_process)
    release_locks(journal["locks"], journal["transaction_id"])
    return result


def _rollback_locked(journal_path, allowed_roots, *, _in_process=False):
    journal_path = no_links(journal_path)
    journal, roots = validate_journal(journal_path, allowed_roots)
    tid = journal["transaction_id"]
    require(_in_process or journal["status"] in {"COMMITTED", "ROLLED_BACK"} or not process_alive(journal.get("pid")),
            "Transaction process is still alive; stop it before crash recovery")
    if journal["status"] == "ROLLED_BACK":
        for row in journal["rows"]:
            require(current_hash(row["destination"]) == row["original_hash"], "Rolled-back destination has subsequently changed")
        for root in roots:
            clean_scratch(root, tid)
        return {"status": "ROLLED_BACK", "journal": str(journal_path), "already_restored": True}
    # Validate ALL current states before changing even one. An edited new skill
    # is user work; do not silently discard it while restoring an old release.
    for row in journal["rows"]:
        current = current_hash(row["destination"])
        require(current in {None, row["original_hash"], row["installed_hash"]}, f"Destination has unrelated edits; recovery refused: {row['destination']}")
        if row["state"] == "READY":
            require(current == row["original_hash"], "Untouched destination changed; refusing rollback")
    preserved_before = preservation_fingerprint(roots, journal["owned_paths"])
    journal["status"] = "ROLLING_BACK"
    # Attribute recovery to this process so another process can resume after
    # a rollback crash even when the earlier installer PID is still alive.
    journal["pid"] = os.getpid()
    write_json(journal_path, journal)
    for row in reversed(journal["rows"]):
        destination = Path(row["destination"])
        if current_hash(destination) != row["original_hash"]:
            scratch = scratch_for(destination.parent, tid)
            if not scratch.exists():
                scratch.mkdir()
                write_json(scratch / ".owner.json", {"transaction_id": tid})
            marker = scratch / ".owner.json"
            require(marker.is_file() and read_json(marker).get("transaction_id") == tid, "Rollback scratch ownership missing")
            replacement = scratch / ("restore-" + str(row["index"]))
            if row["original_hash"] is not None:
                # Recreate an interrupted owned scratch copy from the still
                # verified backup, without touching the live tree.
                if replacement.exists() and current_hash(replacement) != row["original_hash"]:
                    walk_files(replacement, selected=False)
                    shutil.rmtree(replacement)
                if not replacement.exists():
                    shutil.copytree(row["backup"], replacement, copy_function=shutil.copy2)
                require(current_hash(replacement) == row["original_hash"], "Restore staging hash differs")
            require(current_hash(destination) in {None, row["original_hash"], row["installed_hash"]},
                    f"Destination changed during rollback: {destination}")
            row["state"] = "ROLLBACK_INTENT"
            write_json(journal_path, journal)
            if destination.exists():
                no_links(destination)
                displaced = scratch / ("rollback-displaced-" + str(row["index"]))
                require(not displaced.exists(), "Unexpected occupied rollback displacement path")
                # Both rename boundaries leave a complete tree or absence;
                # recursive deletion is confined to owned scratch cleanup.
                os.replace(destination, displaced)
                sync_directory(scratch)
                sync_directory(destination.parent)
            if row["original_hash"] is not None:
                os.replace(replacement, destination)
            sync_directory(destination.parent)
        require(current_hash(destination) == row["original_hash"], f"Restore verification failed: {destination}")
        row["state"] = "RESTORED"
        write_json(journal_path, journal)
    require(preservation_fingerprint(roots, journal["owned_paths"]) == preserved_before, "Unrelated/system content changed during rollback")
    journal.update({"status": "ROLLED_BACK", "restored_utc": utc_now()})
    write_json(journal_path, journal)
    for root in roots:
        clean_scratch(root, tid)
    return {"status": "ROLLED_BACK", "journal": str(journal_path), "restored_paths": len(journal["rows"]), "backups_retained": True}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("build", "verify", "plan", "promote"):
        command = sub.add_parser(name)
        command.add_argument("--package-root", type=Path, default=Path(__file__).absolute().parent.parent)
        if name in {"verify", "plan", "promote"}:
            command.add_argument("--stage-root", type=Path, required=name in {"plan", "promote"})
        if name in {"plan", "promote"}:
            command.add_argument("--destination-root", type=Path, required=True)
            command.add_argument("--mapping", type=Path, help="Explicit destinations/duplicate-removal JSON; see normalize_mapping")
            command.add_argument("--replace", action="store_true", help="Allow verified backup and replacement of existing approved skills")
        if name == "promote":
            command.add_argument("--backup-parent", type=Path, required=True)
    recovery = sub.add_parser("rollback")
    recovery.add_argument("--journal", type=Path, required=True)
    recovery.add_argument("--allow-root", type=Path, action="append", required=True, help="Explicit allowed personal skills root; repeat for overlays")
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            result = build(args.package_root)
        elif args.command == "verify":
            result = verify_package(args.package_root, args.stage_root)
        elif args.command == "rollback":
            result = rollback(args.journal, args.allow_root)
        else:
            mapping = read_json(args.mapping) if args.mapping else None
            if args.command == "plan":
                result = plan_install(args.package_root, args.stage_root, args.destination_root, mapping, args.replace)
            else:
                result = promote(args.package_root, args.stage_root, args.destination_root, args.backup_parent, mapping, args.replace)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (PackageError, OSError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
