#!/usr/bin/env python3
"""Read-only IPSW inventory for PhoneBridge. Never executes firmware or extracted files."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import plistlib
import sys
import zipfile
from pathlib import Path, PurePosixPath

VERSION = "0.1.0"
MAX_ENTRIES = 200_000
MAX_PLIST_BYTES = 128 * 1024 * 1024
KERNEL_HINTS = ("kernelcache", "kernelcollection", "kernel_collection")
MANIFEST_NAMES = {"buildmanifest.plist", "restore.plist", "updatemanifest.plist"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_archive_path(name: str) -> bool:
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    return not path.is_absolute() and ".." not in path.parts and not normalized.startswith("//")


def summarize_plist(value):
    """Convert plist values to bounded JSON-safe metadata; avoid dumping binary blobs."""
    if isinstance(value, dict):
        return {str(k): summarize_plist(v) for k, v in list(value.items())[:5000]}
    if isinstance(value, list):
        return [summarize_plist(v) for v in value[:5000]]
    if isinstance(value, bytes):
        return {"type": "bytes", "length": len(value)}
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)[:500]


def build_metadata(manifests: dict[str, bytes]) -> dict:
    result = {"product_version": None, "product_build_version": None,
              "build_identity_count": None, "device_classes": [], "parse_errors": []}
    for name, raw in manifests.items():
        if Path(name).name.lower() != "buildmanifest.plist":
            continue
        try:
            parsed = plistlib.loads(raw)
            result["product_version"] = parsed.get("ProductVersion")
            result["product_build_version"] = parsed.get("ProductBuildVersion")
            identities = parsed.get("BuildIdentities", [])
            result["build_identity_count"] = len(identities) if isinstance(identities, list) else None
            classes = set()
            if isinstance(identities, list):
                for identity in identities:
                    info = identity.get("Info", {}) if isinstance(identity, dict) else {}
                    device_class = info.get("DeviceClass") if isinstance(info, dict) else None
                    if isinstance(device_class, str):
                        classes.add(device_class)
            result["device_classes"] = sorted(classes)
        except (ValueError, plistlib.InvalidFileException, TypeError) as exc:
            result["parse_errors"].append(f"{name}: {type(exc).__name__}: {exc}")
    return result


def inspect_archive(source: Path, expected_model: str | None, expected_ios: str | None) -> dict:
    report = {
        "tool": "PhoneBridge KernelScope", "version": VERSION,
        "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "input": {"filename": source.name, "size_bytes": source.stat().st_size,
                  "sha256": sha256_file(source)},
        "requested_target": {"model": expected_model, "ios_version": expected_ios},
        "firmware_metadata": {}, "checks": {}, "entries": [], "warnings": []
    }
    manifests: dict[str, bytes] = {}
    with zipfile.ZipFile(source) as archive:
        infos = archive.infolist()
        report["checks"]["zip_open"] = "PASS"
        report["checks"]["entry_count"] = len(infos)
        if len(infos) > MAX_ENTRIES:
            raise ValueError(f"Archive has {len(infos)} entries; safety limit is {MAX_ENTRIES}")
        for info in infos:
            name = info.filename
            lower = name.lower()
            is_manifest = Path(name).name.lower() in MANIFEST_NAMES
            is_kernel = any(hint in lower for hint in KERNEL_HINTS)
            status = "PASS"
            if not safe_archive_path(name):
                status = "FAIL_UNSAFE_PATH"
                report["warnings"].append(f"Unsafe archive path: {name}")
            if info.file_size < 0 or info.compress_size < 0:
                status = "FAIL_INVALID_SIZE"
            elif info.file_size > 0 and info.compress_size == 0 and not info.is_dir():
                status = "WARN_SUSPICIOUS_SIZE"
            elif info.compress_size and info.file_size / info.compress_size > 10_000:
                status = "WARN_HIGH_COMPRESSION_RATIO"
            category = "manifest" if is_manifest else "kernel_candidate" if is_kernel else "other"
            report["entries"].append({
                "name": name, "size_bytes": info.file_size,
                "compressed_size_bytes": info.compress_size, "category": category, "status": status
            })
            if is_manifest and safe_archive_path(name) and info.file_size <= MAX_PLIST_BYTES:
                try:
                    manifests[name] = archive.read(info)
                except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
                    report["warnings"].append(f"Cannot read manifest {name}: {exc}")
    report["firmware_metadata"] = build_metadata(manifests)
    report["checks"]["build_manifest"] = (
        "PASS" if any(Path(n).name.lower() == "buildmanifest.plist" for n in manifests) else "PARTIAL"
    )
    report["checks"]["kernel_candidates"] = (
        "PASS" if any(e["category"] == "kernel_candidate" for e in report["entries"]) else "FAIL"
    )
    report["checks"]["target_compatibility"] = "NOT_VALIDATED"
    report["warnings"].append(
        "Filename and archive metadata do not prove the installed device/build or physical compatibility."
    )
    report["warnings"].append(
        "Container SHA-256 is an integrity identifier, not proof of Apple authenticity unless compared "
        "with a trusted official reference."
    )
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Read-only IPSW inventory; no exploit or device actions.")
    sub = parser.add_subparsers(dest="command", required=True)
    inspect = sub.add_parser("inspect", help="inventory an IPSW and identify kernel candidates")
    inspect.add_argument("ipsw", type=Path)
    inspect.add_argument("--out", type=Path, default=Path("kernelscope-report"))
    inspect.add_argument("--model", default="iPhone17,3", help="expected model; informational only")
    inspect.add_argument("--ios-version", default="27.0.1", help="expected version; informational only")
    args = parser.parse_args(argv)
    try:
        source = args.ipsw.expanduser().resolve(strict=True)
        if not source.is_file():
            raise ValueError("Input must be a regular file")
        report = inspect_archive(source, args.model, args.ios_version)
        args.out.mkdir(parents=True, exist_ok=True)
        json_path = args.out / "report.json"
        json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"JSON report: {json_path}")
        print(f"IPSW SHA-256: {report['input']['sha256']}")
        print(f"Firmware: {report['firmware_metadata']['product_version']} "
              f"(build {report['firmware_metadata']['product_build_version']})")
        print(f"Kernel candidates: {sum(e['category'] == 'kernel_candidate' for e in report['entries'])}")
        print("Target compatibility: NOT_VALIDATED")
        return 0
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError) as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
