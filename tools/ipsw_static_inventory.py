#!/usr/bin/env python3
"""Read-only IPSW inventory, BuildManifest metadata and SHA-256 verification.

No extraction to disk, firmware decryption, patching, execution, device connection,
or privilege-escalation attempt is performed. Standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import plistlib
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

INTERESTING_TOKENS = (
    "kernelcache", "devicetree", "trustcache", "dyld", "sep-firmware",
    "restore", "iboot", "manifest", "buildmanifest", "filesystem",
)
DEFAULT_TARGET_SHA256 = "fc87bb9da8c03d0154d87531950f4a170195f6663ee5208653fa7a26bafb9469"


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def classify_member(name: str) -> list[str]:
    lowered = name.lower()
    return [token for token in INTERESTING_TOKENS if token in lowered]


def manifest_metadata(archive: zipfile.ZipFile) -> dict[str, Any]:
    """Read plist metadata directly from the ZIP stream; do not write files."""
    candidates = ("BuildManifest.plist", "BuildManifesto.plist")
    manifest_name = next(
        (name for name in candidates if name in archive.namelist()), None
    )
    if manifest_name is None:
        return {"status": "NOT_FOUND"}
    try:
        manifest = plistlib.loads(archive.read(manifest_name))
    except (plistlib.InvalidFileException, ValueError, KeyError) as exc:
        return {"status": "PARSE_FAILED", "error": str(exc), "path": manifest_name}

    identities = []
    for identity in manifest.get("BuildIdentities", []):
        info = identity.get("Info", {})
        identities.append({
            "device_class": info.get("DeviceClass"),
            "board_config": info.get("BoardConfig"),
            "variant": info.get("Variant"),
            "restore_behavior": info.get("RestoreBehavior"),
            "has_kernelcache_path": bool(identity.get("Manifest", {}).get("KernelCache", {}).get("Info", {}).get("Path")),
            "has_device_tree_path": bool(identity.get("Manifest", {}).get("DeviceTree", {}).get("Info", {}).get("Path")),
            "has_trust_cache_path": bool(identity.get("Manifest", {}).get("StaticTrustCache", {}).get("Info", {}).get("Path")),
        })
    return {
        "status": "PARSED",
        "path": manifest_name,
        "product_version": manifest.get("ProductVersion"),
        "product_build_version": manifest.get("ProductBuildVersion"),
        "supported_product_types": manifest.get("SupportedProductTypes", []),
        "identity_count": len(identities),
        "build_identities": identities,
    }


def inspect_ipsw(path: Path, expected_sha256: str | None = None) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"IPSW file not found: {path}")
    if not zipfile.is_zipfile(path):
        raise ValueError("Input is not a readable ZIP/IPSW archive")

    entries: list[dict[str, Any]] = []
    with zipfile.ZipFile(path, "r") as archive:
        bad_member = archive.testzip()
        manifest = manifest_metadata(archive)
        for item in archive.infolist():
            entries.append({
                "path": item.filename,
                "size_bytes": item.file_size,
                "compressed_bytes": item.compress_size,
                "crc32": f"{item.CRC:08x}",
                "interesting_tags": classify_member(item.filename),
            })

    actual_sha256 = sha256_file(path)
    hash_check: dict[str, Any] = {"status": "NOT_REQUESTED"}
    if expected_sha256:
        expected = expected_sha256.strip().lower()
        if len(expected) != 64 or any(ch not in "0123456789abcdef" for ch in expected):
            raise ValueError("Expected SHA-256 must contain exactly 64 hexadecimal characters")
        hash_check = {
            "expected_sha256": expected,
            "actual_sha256": actual_sha256,
            "status": "PASS" if actual_sha256 == expected else "FAIL",
        }

    return {
        "schema_version": 2,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "input": {
            "filename": path.name,
            "size_bytes": path.stat().st_size,
            "sha256": actual_sha256,
            "expected_hash_check": hash_check,
        },
        "archive": {
            "format": "ZIP/IPSW",
            "entry_count": len(entries),
            "zip_integrity_test": "FAIL" if bad_member else "PASS",
            "first_bad_member": bad_member,
        },
        "build_manifest": manifest,
        "entries": entries,
        "limitations": [
            "Inventory only: no extraction to disk, decryption, execution, or patching.",
            "Manifest metadata and file names do not establish exploitability.",
            "A VM result is not proof of a physical-device jailbreak.",
            "The default target hash is a third-party published reference; independently verify provenance.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a read-only JSON inventory of an IPSW and its SHA-256."
    )
    parser.add_argument("ipsw", type=Path, help="Path to a local .ipsw archive")
    parser.add_argument("--output", "-o", type=Path, help="JSON output path")
    parser.add_argument(
        "--expected-sha256", default=None,
        help="Optional expected SHA-256; report PASS/FAIL on exact match",
    )
    parser.add_argument(
        "--check-iphone16-27.0.1",
        action="store_true",
        help="Compare against published iPhone17,3 / iOS 27.0.1 (24A446) reference SHA-256",
    )
    args = parser.parse_args()

    try:
        expected = args.expected_sha256
        if args.check_iphone16_27_0_1:
            if expected and expected.lower() != DEFAULT_TARGET_SHA256:
                parser.error("Do not combine --check-iphone16-27.0.1 with a different --expected-sha256")
            expected = DEFAULT_TARGET_SHA256
        report = inspect_ipsw(args.ipsw, expected)
        rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.write_text(rendered, encoding="utf-8")
            print(f"PASS: report written to {args.output}")
            print(f"IPSW SHA-256: {report['input']['sha256']}")
            if expected:
                print(f"REFERENCE HASH CHECK: {report['input']['expected_hash_check']['status']}")
        else:
            sys.stdout.write(rendered)
        return 0 if report["archive"]["zip_integrity_test"] == "PASS" and report["input"]["expected_hash_check"]["status"] != "FAIL" else 2
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
