#!/usr/bin/env python3
"""Read-only audit of a local jprx/darwin-vm checkout for PhoneBridge integration.

This tool does not clone repositories, execute scripts, boot QEMU, patch firmware,
or contact a connected iPhone. It reports repository evidence only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from pathlib import Path

REQUIRED = (
    "README.md",
    "get_files.sh",
    "run.sh",
    "build_tc.py",
    "dt_fixup.py",
    "qemu-sptm",
)
TARGET_MODEL = "iPhone17,3"
TARGET_VERSION = "27.0.1"
TARGET_BUILD = "24A446"


def audit_tree(root: Path) -> dict:
    root = root.expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError("darwin-vm path must be a directory")

    missing = [name for name in REQUIRED if not (root / name).exists()]
    readme_path = root / "README.md"
    readme = readme_path.read_text(encoding="utf-8", errors="replace") if readme_path.is_file() else ""
    submodules = (root / ".gitmodules").read_text(encoding="utf-8", errors="replace") if (root / ".gitmodules").is_file() else ""
    scripts = {}
    for name in ("get_files.sh", "run.sh", "build_tc.py", "dt_fixup.py", "fix_perms.sh"):
        path = root / name
        if path.is_file():
            data = path.read_bytes()
            scripts[name] = {"exists": True, "size_bytes": len(data), "sha256": __import__("hashlib").sha256(data).hexdigest()}
        else:
            scripts[name] = {"exists": False}

    exact_build_mentioned = TARGET_BUILD in readme or TARGET_BUILD in submodules
    target_model = TARGET_MODEL in readme
    target_version = bool(re.search(r"iOS\s+27\.0(?:\s|\(|$)", readme, re.IGNORECASE))
    qemu_submodule = (root / "qemu-sptm").is_dir() and any((root / "qemu-sptm").iterdir()) if (root / "qemu-sptm").is_dir() else False
    mac_required = bool(re.search(r"requires? a Mac|must run this on a Mac|requires? macOS", readme, re.IGNORECASE))

    checks = {
        "required_layout": "PASS" if not missing else "PARTIAL",
        "target_model_mentioned": "PASS" if target_model else "NOT_VALIDATED",
        "ios_27_family_mentioned": "PASS" if target_version else "NOT_VALIDATED",
        "exact_build_24A446_mentioned_in_text": "PASS" if exact_build_mentioned else "NOT_VALIDATED",
        "exact_build_24A446_boot_verified": "NOT_VALIDATED",
        "qemu_sptm_submodule_populated": "PASS" if qemu_submodule else "PARTIAL",
        "mac_host_requirement_documented": "PASS" if mac_required else "NOT_VALIDATED",
        "physical_iphone_validation": "NOT_VALIDATED",
        "jailbreak_compatibility": "NOT_VALIDATED",
    }
    status = "PASS" if all(value == "PASS" for value in checks.values()) else "PARTIAL"
    return {
        "tool": "PhoneBridge Darwin VM Audit",
        "schema_version": 1,
        "created_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "root": str(root),
        "target": {"model": TARGET_MODEL, "ios_version": TARGET_VERSION, "build": TARGET_BUILD},
        "status": status,
        "checks": checks,
        "missing_required_paths": missing,
        "scripts": scripts,
        "limits": [
            "This is a static checkout audit; no shell script or binary was executed.",
            "Text mentioning build 24A446 is not boot evidence; exact-build boot remains NOT_VALIDATED.",
            "A QEMU root shell is a guest-VM capability, not physical-device root or a jailbreak.",
            "Darwin VM setup and ramdisk preparation documented upstream require a Mac host.",
        ],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("darwin_vm", type=Path, help="path to an existing darwin-vm checkout")
    parser.add_argument("--out", type=Path, help="optional JSON report destination")
    args = parser.parse_args(argv)
    try:
        report = audit_tree(args.darwin_vm)
        rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return 0 if report["status"] == "PASS" else 1
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "FAIL", "error": f"{type(exc).__name__}: {exc}"}), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
