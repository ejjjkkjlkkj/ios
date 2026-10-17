#!/usr/bin/env python3
"""Read-only inventory and SHA-256 report for an Apple IPSW archive.

This tool does not extract files, decrypt firmware, patch binaries, contact devices,
or attempt privilege escalation. It uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

INTERESTING_TOKENS = (
    "kernelcache", "devicetree", "trustcache", "dyld", "sep-firmware",
    "restore", "iboot", "manifest", "buildmanifest", "filesystem",
)


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def classify_member(name: str) -> list[str]:
    lowered = name.lower()
    return [token for token in INTERESTING_TOKENS if token in lowered]


def inspect_ipsw(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"IPSW file not found: {path}")
    if not zipfile.is_zipfile(path):
        raise ValueError("Input is not a readable ZIP/IPSW archive")

    entries: list[dict[str, Any]] = []
    with zipfile.ZipFile(path, "r") as archive:
        bad_member = archive.testzip()
        for item in archive.infolist():
            entries.append({
                "path": item.filename,
                "size_bytes": item.file_size,
                "compressed_bytes": item.compress_size,
                "crc32": f"{item.CRC:08x}",
                "interesting_tags": classify_member(item.filename),
            })

    return {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "input": {
            "filename": path.name,
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        },
        "archive": {
            "format": "ZIP/IPSW",
            "entry_count": len(entries),
            "zip_integrity_test": "FAIL" if bad_member else "PASS",
            "first_bad_member": bad_member,
        },
        "entries": entries,
        "limitations": [
            "Inventory only: no decryption, extraction, execution, or patching.",
            "File names and hashes do not establish exploitability or device compatibility.",
            "A VM result is not proof of a physical-device jailbreak.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a read-only JSON inventory of an IPSW and its SHA-256."
    )
    parser.add_argument("ipsw", type=Path, help="Path to a local .ipsw archive")
    parser.add_argument(
        "--output", "-o", type=Path,
        help="JSON output path (default: stdout; input archive remains unchanged)",
    )
    args = parser.parse_args()

    try:
        report = inspect_ipsw(args.ipsw)
        rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
            print(f"PASS: report written to {args.output}")
            print(f"IPSW SHA-256: {report['input']['sha256']}")
        else:
            sys.stdout.write(rendered)
        return 0
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
