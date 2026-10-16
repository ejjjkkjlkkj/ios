#!/usr/bin/env python3
"""Read-only IPSW preflight and kernelcache inventory. Python 3.10+, stdlib only.

This tool does not decrypt, patch, exploit, restore, or modify firmware. It reports
what can be established from the archive and BuildManifest.plist alone.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import plistlib
import sys
import zipfile
from pathlib import PurePosixPath
from typing import Any


def _sha256_member(archive: zipfile.ZipFile, name: str) -> str:
    digest = hashlib.sha256()
    with archive.open(name, "r") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_member_name(name: str) -> bool:
    path = PurePosixPath(name)
    return not path.is_absolute() and ".." not in path.parts and "\\" not in name


def _manifest_identities(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for identity in manifest.get("BuildIdentities", []):
        info = identity.get("Info", {}) or {}
        manifest_entries = identity.get("Manifest", {}) or {}
        kernel = manifest_entries.get("KernelCache", {}) or {}
        path = kernel.get("Path")
        results.append({
            "variant": info.get("Variant"),
            "device_class": info.get("DeviceClass"),
            "board_config": info.get("BoardConfig"),
            "security_domain": info.get("SecurityDomain"),
            "kernelcache_path": path,
            "kernelcache_sha256": None,
            "kernelcache_bytes": None,
            "kernelcache_status": "NOT_FOUND",
        })
    return results


def audit_ipsw(path: str, *, hash_kernelcache: bool = True) -> dict[str, Any]:
    report: dict[str, Any] = {
        "tool": "PhoneBridge Firmware Audit",
        "schema_version": 1,
        "input": path,
        "status": "NOT_VALIDATED",
        "scope": "read-only IPSW archive and BuildManifest metadata",
        "limitations": [
            "Archive metadata does not prove device compatibility or exploitability.",
            "Kernelcache presence and hashes do not imply decryption or successful disassembly.",
            "No firmware, device, NVRAM, boot chain, or connected hardware is modified.",
        ],
        "product_version": None,
        "product_build_version": None,
        "supported_product_types": [],
        "archive_entries": 0,
        "archive_integrity": "NOT_CHECKED",
        "build_identities": [],
        "errors": [],
    }
    try:
        with zipfile.ZipFile(path, "r") as archive:
            entries = archive.infolist()
            report["archive_entries"] = len(entries)
            names = {item.filename for item in entries}
            manifest_name = "BuildManifest.plist"
            if manifest_name not in names:
                report["errors"].append("BuildManifest.plist is missing.")
                report["archive_integrity"] = "PARTIAL"
                report["status"] = "PARTIAL"
                return report
            manifest_bytes = archive.read(manifest_name)
            manifest = plistlib.loads(manifest_bytes)
            if not isinstance(manifest, dict):
                raise ValueError("BuildManifest.plist root is not a dictionary")
            report["product_version"] = manifest.get("ProductVersion")
            report["product_build_version"] = manifest.get("ProductBuildVersion")
            report["supported_product_types"] = sorted(
                set(manifest.get("SupportedProductTypes", []) or [])
            )
            identities = _manifest_identities(manifest)
            for identity in identities:
                member = identity["kernelcache_path"]
                if not isinstance(member, str) or not member:
                    identity["kernelcache_status"] = "NO_PATH_IN_MANIFEST"
                    continue
                if not _safe_member_name(member):
                    identity["kernelcache_status"] = "UNSAFE_PATH_REJECTED"
                    report["errors"].append(f"Unsafe kernelcache path rejected: {member}")
                    continue
                if member not in names:
                    identity["kernelcache_status"] = "NOT_IN_ARCHIVE"
                    continue
                info = archive.getinfo(member)
                identity["kernelcache_bytes"] = info.file_size
                if hash_kernelcache:
                    identity["kernelcache_sha256"] = _sha256_member(archive, member)
                    identity["kernelcache_status"] = "FOUND_HASHED"
                else:
                    identity["kernelcache_status"] = "FOUND_NOT_HASHED"
            report["build_identities"] = identities
            bad_member = archive.testzip()
            report["archive_integrity"] = "PASS" if bad_member is None else "FAIL"
            if bad_member is not None:
                report["errors"].append(f"CRC failure in archive member: {bad_member}")
            report["status"] = "PARTIAL" if report["errors"] else "INVENTORIED"
    except (OSError, zipfile.BadZipFile, plistlib.InvalidFileException, ValueError) as exc:
        report["status"] = "FAIL"
        report["errors"].append(f"{type(exc).__name__}: {exc}")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only IPSW BuildManifest and kernelcache inventory (no exploit/decryption)."
    )
    parser.add_argument("ipsw", help="Path to an IPSW ZIP archive")
    parser.add_argument("--no-hash", action="store_true", help="List kernelcache paths without hashing their contents")
    parser.add_argument("--output", "-o", help="Write JSON report to this file; stdout otherwise")
    args = parser.parse_args(argv)
    report = audit_ipsw(args.ipsw, hash_kernelcache=not args.no_hash)
    rendered = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    try:
        if args.output:
            with open(args.output, "w", encoding="utf-8", newline="\n") as output:
                output.write(rendered)
        else:
            sys.stdout.write(rendered)
    except OSError as exc:
        print(f"Cannot write report: {exc}", file=sys.stderr)
        return 2
    return 0 if report["status"] in {"INVENTORIED", "PARTIAL"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
