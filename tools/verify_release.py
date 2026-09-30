#!/usr/bin/env python3
"""Verify preserved publication bytes and browsable v72 content offline.

Uses only the Python standard library. No scientific script is imported or run;
no files are changed, downloaded, installed, or extracted. A passing result
establishes agreement with the local manifest and archive, not scientific
validation or independent authentication of a modified manifest.
"""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile


ARCHIVE_NAME = (
    "HRF_V72_COMPOSITE_CLOSURE_LEAST_FAVORABLE_SEPARATION_AND_RAW_REPLAY.zip"
)
ARCHIVE_ROOT = ARCHIVE_NAME[:-4]
EXPECTED_RELEASE_COUNT = 15
EXPECTED_FOCUSED_COUNT = 57


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_relative(name):
    path = PurePosixPath(name)
    if (not name or "\\" in name or path.is_absolute()
            or any(part in {".", ".."} for part in path.parts)
            or path.as_posix() != name):
        raise ValueError("Unsafe or noncanonical relative path: " + repr(name))
    return path


def files_under(folder):
    if not folder.is_dir() or folder.is_symlink():
        raise ValueError("Expected an ordinary directory: " + str(folder))
    names = set()
    for path in folder.rglob("*"):
        if path.is_symlink():
            raise ValueError("Symbolic links are not admitted: " + str(path))
        if path.is_file():
            names.add(path.relative_to(folder).as_posix())
        elif not path.is_dir():
            raise ValueError("Special files are not admitted: " + str(path))
    return names


def verify(repo):
    manifest_path = repo / "MANIFEST.sha256"
    if manifest_path.is_symlink():
        raise ValueError("The manifest must be an ordinary file")
    manifest = {}
    for line_number, line in enumerate(manifest_path.read_text().splitlines(), 1):
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            raise ValueError("Malformed manifest line " + str(line_number))
        digest, name = match.groups()
        path = safe_relative(name)
        if path.parts[:2] != ("release", "v5.3") or len(path.parts) != 3:
            raise ValueError("Unexpected manifest location: " + name)
        if name in manifest:
            raise ValueError("Duplicate manifest entry: " + name)
        manifest[name] = digest
    if len(manifest) != EXPECTED_RELEASE_COUNT:
        raise ValueError("Expected exactly 15 original publication files")

    release_root = repo / "release" / "v5.3"
    expected_release = {PurePosixPath(name).name for name in manifest}
    actual_release = files_under(release_root)
    if actual_release != expected_release:
        raise ValueError("Release membership mismatch: " + json.dumps({
            "missing": sorted(expected_release - actual_release),
            "extra": sorted(actual_release - expected_release),
        }))
    if (repo / "release").is_symlink():
        raise ValueError("The release directory must not be a symbolic link")
    for name, expected in manifest.items():
        path = repo.joinpath(*PurePosixPath(name).parts)
        if sha256_file(path) != expected:
            raise ValueError("SHA-256 mismatch: " + name)

    focused_root = repo / "research" / "v72"
    if (repo / "research").is_symlink():
        raise ValueError("The research directory must not be a symbolic link")
    actual_focused = files_under(focused_root)
    archived = {}
    archive_path = release_root / ARCHIVE_NAME
    with zipfile.ZipFile(archive_path) as archive:
        seen = set()
        for member in archive.infolist():
            if member.filename in seen:
                raise ValueError("Duplicate archive member: " + member.filename)
            seen.add(member.filename)
            relative = safe_relative(member.filename.rstrip("/"))
            if relative.parts[0] != ARCHIVE_ROOT:
                raise ValueError("Unexpected archive root: " + member.filename)
            mode = member.external_attr >> 16
            kind = stat.S_IFMT(mode)
            if kind not in (0, stat.S_IFREG, stat.S_IFDIR):
                raise ValueError("Special archive member: " + member.filename)
            if member.is_dir():
                continue
            name = PurePosixPath(*relative.parts[1:]).as_posix()
            if name == ".":
                raise ValueError("Archive content lacks a relative filename")
            archived[name] = hashlib.sha256(archive.read(member)).hexdigest()
    if len(archived) != EXPECTED_FOCUSED_COUNT:
        raise ValueError("Expected exactly 57 focused archive files")
    if actual_focused != set(archived):
        raise ValueError("Focused membership mismatch: " + json.dumps({
            "missing": sorted(set(archived) - actual_focused),
            "extra": sorted(actual_focused - set(archived)),
        }))
    for name, expected in archived.items():
        path = focused_root.joinpath(*PurePosixPath(name).parts)
        if sha256_file(path) != expected:
            raise ValueError("Archive-to-extracted SHA-256 mismatch: " + name)
    return {
        "status": "PASS",
        "publication_files_verified": len(manifest),
        "focused_files_identical_to_archive": len(archived),
        "checks": "SHA-256, exact file membership, archive CRC while reading",
        "scope": "File integrity only; no research code or raw replay executed",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root", type=Path, default=Path(__file__).resolve().parents[1],
        help="Repository directory (defaults to this script's repository)",
    )
    args = parser.parse_args()
    try:
        result = verify(args.repo_root.resolve())
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError) as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, indent=2))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
