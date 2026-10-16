#!/usr/bin/env python3
"""Verify local IPSW archive integrity and target metadata; never modifies a device."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import plistlib
import sys
import zipfile
from pathlib import Path

TARGET_MODEL = "iPhone17,3"
TARGET_BOARD = "D47AP"
TARGET_VERSION = "27.0.1"
TARGET_BUILD = "24A446"
MANIFEST = "BuildManifest.plist"
MAX_MANIFEST_BYTES = 128 * 1024 * 1024
MAX_ENTRIES = 200_000


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_ipsw(path: Path, model: str = TARGET_MODEL, board: str = TARGET_BOARD,
                version: str = TARGET_VERSION, build: str = TARGET_BUILD) -> dict:
    path = path.expanduser().resolve(strict=True)
    if not path.is_file():
        raise ValueError("IPSW input must be a regular file")

    report = {
        "tool": "PhoneBridge Target Firmware Verifier",
        "schema_version": 1,
        "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "input": {"filename": path.name, "size_bytes": path.stat().st_size,
                  "sha256": sha256_file(path)},
        "expected": {"product_type": model, "device_class": board,
                     "product_version": version, "product_build_version": build},
        "observed": {},
        "checks": {},
        "limitations": [
            "A matching SHA-256 identifies these bytes; it does not prove Apple authenticity.",
            "ZIP integrity and BuildManifest metadata do not prove the firmware is installed on a device.",
            "No firmware is flashed, no connected device is contacted, and no exploit is attempted.",
        ],
    }
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        if len(infos) > MAX_ENTRIES:
            raise ValueError(f"Archive entry count {len(infos)} exceeds safety limit {MAX_ENTRIES}")
        names = [item.filename for item in infos]
        matches = [item for item in infos if item.filename.rsplit("/", 1)[-1].lower() == MANIFEST.lower()]
        report["checks"]["zip_open"] = "PASS"
        report["checks"]["entry_count_limit"] = "PASS"
        bad_member = archive.testzip()
        report["checks"]["zip_crc_integrity"] = "PASS" if bad_member is None else "FAIL"
        if bad_member is not None:
            report["observed"]["first_corrupt_member"] = bad_member
        if len(matches) != 1:
            report["checks"]["build_manifest_unique"] = "FAIL"
            report["checks"]["target_identity"] = "NOT_VALIDATED"
            report["observed"]["manifest_matches"] = len(matches)
            report["checks"]["apple_authenticity"] = "NOT_VALIDATED"
            report["status"] = "FAIL"
            return report
        info = matches[0]
        if info.file_size > MAX_MANIFEST_BYTES:
            raise ValueError("BuildManifest.plist exceeds safety size limit")
        manifest = plistlib.loads(archive.read(info))
        if not isinstance(manifest, dict):
            raise ValueError("BuildManifest.plist root is not a dictionary")
        identities = manifest.get("BuildIdentities", [])
        device_classes = sorted({
            identity.get("Info", {}).get("DeviceClass")
            for identity in identities
            if isinstance(identity, dict)
            and isinstance(identity.get("Info"), dict)
            and isinstance(identity.get("Info", {}).get("DeviceClass"), str)
        }) if isinstance(identities, list) else []
        report["observed"] = {
            **report["observed"],
            "product_type": manifest.get("ProductType"),
            "product_version": manifest.get("ProductVersion"),
            "product_build_version": manifest.get("ProductBuildVersion"),
            "device_classes": device_classes,
            "build_identity_count": len(identities) if isinstance(identities, list) else None,
            "manifest_path": info.filename,
        }
        report["checks"]["build_manifest_unique"] = "PASS"
        expected = report["expected"]
        observed = report["observed"]
        checks = {
            "product_type": observed.get("product_type") == expected["product_type"],
            "product_version": observed.get("product_version") == expected["product_version"],
            "product_build_version": observed.get("product_build_version") == expected["product_build_version"],
            "device_class": expected["device_class"] in device_classes,
        }
        report["checks"].update({key: "PASS" if value else "FAIL" for key, value in checks.items()})
        report["checks"]["target_identity"] = (
            "PASS" if all(checks.values()) else "FAIL"
        )
        report["checks"]["apple_authenticity"] = "NOT_VALIDATED"
        report["status"] = (
            "PASS" if report["checks"]["zip_crc_integrity"] == "PASS"
            and report["checks"]["target_identity"] == "PASS" else "FAIL"
        )
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ipsw", type=Path, help="path to an already downloaded IPSW")
    parser.add_argument("--out", type=Path, help="optional JSON report path")
    parser.add_argument("--model", default=TARGET_MODEL)
    parser.add_argument("--board", default=TARGET_BOARD)
    parser.add_argument("--ios-version", default=TARGET_VERSION)
    parser.add_argument("--build", default=TARGET_BUILD)
    args = parser.parse_args(argv)
    try:
        report = verify_ipsw(args.ipsw, args.model, args.board, args.ios_version, args.build)
        rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.out:
            args.out.expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
            args.out.expanduser().resolve().write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0 if report["status"] == "PASS" else 1
    except (OSError, ValueError, zipfile.BadZipFile, plistlib.InvalidFileException,
            RuntimeError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
