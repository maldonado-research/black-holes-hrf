#!/usr/bin/env python3
"""Build a deterministic recursive manifest for the standalone v72 directory."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "GW250114_V72_manifest.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    files = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path == OUTPUT or "__pycache__" in path.parts:
            continue
        files.append({
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    payload = {
        "version": "GW250114_HRF_v72",
        "date": "2026-07-12",
        "root": ROOT.name,
        "file_count_excluding_manifest": len(files),
        "files": files,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"wrote {OUTPUT.name}: {len(files)} entries")


if __name__ == "__main__":
    main()
