# PhoneBridge Firmware Audit

Read-only preflight for Apple IPSW firmware archives. The tool inventories
`BuildManifest.plist`, build/version metadata, supported product identifiers,
kernelcache paths, sizes, SHA-256 hashes, and ZIP CRC integrity.

## Requirements

- Python 3.10 or newer
- Standard library only; no pip packages and no cloud connection

## Usage

From the repository root:

```sh
python Tools/firmware-audit/firmware_audit.py /path/to/firmware.ipsw
python Tools/firmware-audit/firmware_audit.py /path/to/firmware.ipsw --no-hash
python Tools/firmware-audit/firmware_audit.py /path/to/firmware.ipsw --output firmware-audit.json
```

A full hash pass reads every kernelcache referenced by the manifest and may take
time for large firmware archives. The report records evidence and limitations
explicitly. `INVENTORIED` means metadata was parsed, not that firmware is
compatible with a device, decryptable, bootable, or vulnerable.

## Unit tests

```sh
python -m unittest discover -s Tools/firmware-audit -p 'test_*.py' -v
```

## Deeper static analysis

For disassembly and kernel-specific reports, optionally use the independently
maintained open-source `ipsw` toolkit: https://github.com/blacktop/ipsw .
This repository's audit tool does not download tools, invoke third-party
binaries, decrypt firmware, patch kernels, or attempt exploitation.

## Safety and validation labels

- `PASS`: ZIP CRC test passed.
- `INVENTORIED`: manifest and listed metadata were parsed.
- `PARTIAL`: the archive could be opened but required metadata or checks were missing.
- `FAIL`: invalid archive or parse/read failure.
- `NOT_VALIDATED`: the report never claims physical-device compatibility or exploitability.

Never treat QEMU/simulation, archive parsing, or a hash as proof of behavior on a physical iPhone.
