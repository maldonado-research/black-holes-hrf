#!/usr/bin/env python3
"""Read-only exact verifier for a GW250114 v72 full-package manifest.

The manifest itself is excluded from the expected member set.  This program
prints a deterministic JSON report to stdout, writes no files, and exits
nonzero on every schema, path-safety, membership, size, or SHA-256 mismatch.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any


SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")


class DuplicateJsonKey(ValueError):
    """Raised when a JSON object repeats a key."""


def no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKey(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_manifest_path(value: object) -> tuple[bool, str]:
    if not isinstance(value, str):
        return False, "path is not a string"
    if not value:
        return False, "path is empty"
    if any(ord(character) < 32 for character in value):
        return False, "control character is not allowed"
    if "\\" in value:
        return False, "backslash is not allowed"
    candidate = PurePosixPath(value)
    if candidate.is_absolute():
        return False, "absolute path is not allowed"
    if candidate.parts and candidate.parts[0].endswith(":"):
        return False, "drive-qualified path is not allowed"
    if any(part in {"", ".", ".."} for part in candidate.parts):
        return False, "dot or parent segment is not allowed"
    if candidate.as_posix() != value:
        return False, "path is not normalized POSIX form"
    return True, "ok"


def relative_to_root(path: Path, root: Path) -> str | None:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return None


def verify(root: Path, manifest_path: Path) -> dict[str, object]:
    errors: list[str] = []
    root = root.resolve()
    manifest_path = manifest_path.resolve()

    if not root.is_dir():
        return {
            "status": "FAIL",
            "root": str(root),
            "manifest": str(manifest_path),
            "listed_files": 0,
            "actual_files_excluding_manifest": 0,
            "errors": ["root is not a directory"],
        }
    if not manifest_path.is_file():
        return {
            "status": "FAIL",
            "root": str(root),
            "manifest": str(manifest_path),
            "listed_files": 0,
            "actual_files_excluding_manifest": 0,
            "errors": ["manifest is not a regular file"],
        }

    try:
        manifest = json.loads(
            manifest_path.read_text(), object_pairs_hook=no_duplicate_keys
        )
    except Exception as exc:
        return {
            "status": "FAIL",
            "root": str(root),
            "manifest": str(manifest_path),
            "listed_files": 0,
            "actual_files_excluding_manifest": 0,
            "errors": [f"manifest JSON error: {exc}"],
        }

    if not isinstance(manifest, dict):
        errors.append("manifest top level is not an object")
        manifest = {}
    entries = manifest.get("files")
    if not isinstance(entries, list):
        errors.append("manifest 'files' is not an array")
        entries = []

    listed: dict[str, dict[str, object]] = {}
    for index, entry in enumerate(entries):
        label = f"files[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label}: entry is not an object")
            continue
        value = entry.get("path")
        safe, reason = safe_manifest_path(value)
        if not safe:
            errors.append(f"{label}: unsafe path ({reason})")
            continue
        rel = str(value)
        if rel in listed:
            errors.append(f"{label}: duplicate path {rel!r}")
            continue
        size = entry.get("bytes")
        digest = entry.get("sha256")
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            errors.append(f"{label}: invalid byte count for {rel!r}")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            errors.append(f"{label}: invalid SHA-256 for {rel!r}")
        listed[rel] = entry

    declared_count = manifest.get("file_count_excluding_manifest")
    if declared_count is not None:
        if isinstance(declared_count, bool) or not isinstance(declared_count, int):
            errors.append("file_count_excluding_manifest is not an integer")
        elif declared_count != len(entries):
            errors.append(
                "file_count_excluding_manifest does not equal the number of entries "
                f"({declared_count!r} != {len(entries)})"
            )

    actual: dict[str, Path] = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            rel = relative_to_root(path, root) or str(path)
            errors.append(f"symlink is not allowed: {rel}")
            continue
        if path.is_dir():
            continue
        if not path.is_file():
            rel = relative_to_root(path, root) or str(path)
            errors.append(f"non-regular package member: {rel}")
            continue
        if path.resolve() == manifest_path:
            continue
        rel = relative_to_root(path.resolve(), root)
        if rel is None:
            errors.append(f"file resolves outside package root: {path}")
            continue
        actual[rel] = path

    listed_names = set(listed)
    actual_names = set(actual)
    for rel in sorted(listed_names - actual_names):
        errors.append(f"listed file missing: {rel}")
    for rel in sorted(actual_names - listed_names):
        errors.append(f"unlisted file present: {rel}")

    for rel in sorted(listed_names & actual_names):
        entry = listed[rel]
        path = actual[rel]
        expected_size = entry.get("bytes")
        expected_digest = entry.get("sha256")
        if isinstance(expected_size, int) and not isinstance(expected_size, bool):
            actual_size = path.stat().st_size
            if actual_size != expected_size:
                errors.append(
                    f"size mismatch: {rel} ({actual_size} != {expected_size})"
                )
        if isinstance(expected_digest, str) and SHA256_RE.fullmatch(expected_digest):
            actual_digest = sha256(path)
            if actual_digest != expected_digest:
                errors.append(
                    f"SHA-256 mismatch: {rel} ({actual_digest} != {expected_digest})"
                )

    return {
        "status": "PASS" if not errors else "FAIL",
        "root": str(root),
        "manifest": str(manifest_path),
        "listed_files": len(listed),
        "actual_files_excluding_manifest": len(actual),
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify exact v72 package membership, sizes, and SHA-256 hashes."
    )
    parser.add_argument("--root", type=Path, required=True, help="package root directory")
    parser.add_argument("--manifest", type=Path, required=True, help="full manifest JSON")
    args = parser.parse_args()

    report = verify(args.root, args.manifest)
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
