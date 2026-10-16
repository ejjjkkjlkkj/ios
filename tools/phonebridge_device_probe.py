#!/usr/bin/env python3
"""Read-only USB iOS device probe for PhoneBridge.

This tool reports only explicitly allow-listed, non-unique Lockdown values.
It never installs apps, changes settings, starts a tunnel, reboots, or writes to
the device. A synthetic fixture is never accepted as physical-device evidence.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SAFE_KEYS = (
    "ProductType",
    "ProductVersion",
    "BuildVersion",
    "DeviceClass",
    "HardwareModel",
    "CPUArchitecture",
    "SupportedDeviceFamilies",
)
TARGET_PRODUCT = "iPhone17,3"
TARGET_VERSION = "27.0.1"
TARGET_BUILD = "24A446"


def build_report(values: dict[str, Any], *, connected: bool, error: str | None = None) -> dict[str, Any]:
    selected = {key: values[key] for key in SAFE_KEYS if key in values}
    identity_match = (
        selected.get("ProductType") == TARGET_PRODUCT
        and selected.get("ProductVersion") == TARGET_VERSION
        and selected.get("BuildVersion") == TARGET_BUILD
    )
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "probe": "phonebridge-usb-lockdown-readonly",
        "evidence_type": "physical_device_observation" if connected else "no_device_observation",
        "connected": connected,
        "target": {
            "product_type": TARGET_PRODUCT,
            "ios_version": TARGET_VERSION,
            "build": TARGET_BUILD,
        },
        "observed": selected,
        "target_match": identity_match if connected else None,
        "status": "PASS" if connected and identity_match else (
            "PARTIAL" if connected else "BLOCKED"
        ),
        "limitations": [
            "Only allow-listed Lockdown metadata is collected.",
            "This does not provide kernel memory, a root shell, or proof of kernelcache compatibility.",
            "A matching product/version/build is not proof of physical kernel analysis.",
        ],
        "error": error,
    }


async def collect() -> dict[str, Any]:
    try:
        from pymobiledevice3.lockdown import create_using_usbmux
    except ImportError:
        return build_report({}, connected=False,
                            error="pymobiledevice3 is not installed; install it separately to enable USB probing.")
    try:
        async with await create_using_usbmux() as lockdown:
            values = lockdown.all_values
            if not isinstance(values, dict):
                return build_report({}, connected=False, error="Lockdown returned unexpected metadata.")
            return build_report(values, connected=True)
    except Exception as exc:
        # Do not emit exception details that may contain UDIDs or connection metadata.
        return build_report({}, connected=False,
                            error=f"USB Lockdown connection failed ({type(exc).__name__}). Check cable, unlock state, and Trust prompt.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", type=Path, help="Optional report destination; written on the host only.")
    args = parser.parse_args(argv)
    report = asyncio.run(collect())
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0 if report["connected"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
