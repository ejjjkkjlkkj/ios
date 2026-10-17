# PhoneBridge USB physical-device probe (read-only)

## Purpose

`tools/phonebridge_device_probe.py` reads a small allow-list of ordinary
Lockdown metadata from a connected, paired iPhone using the public
`pymobiledevice3` Python API. It is an observation tool, not a phone emulator.

It does not install or remove apps, change device settings, reboot, enter
recovery/DFU, start developer tunnels, request root, or read kernel memory.
It intentionally omits UDID, serial number, Wi-Fi/Bluetooth addresses, and
other unique identifiers from its report.

## Prerequisites

- Python 3.11–3.14 is a practical choice for current Atheris/fuzzing workflows;
  the probe itself uses the standard library plus `pymobiledevice3`.
- Install the optional dependency in the host environment:
  `python -m pip install -U pymobiledevice3`
- Connect the iPhone over USB, unlock it, and explicitly approve **Trust This Computer**
  if iOS asks. Do not bypass pairing or trust prompts.

## Run

```powershell
python tools/phonebridge_device_probe.py
python tools/phonebridge_device_probe.py --json-out artifacts/device-probe.json
```

Exit code 0 means a device responded to Lockdown and its product type, iOS
version, and build match the project's declared target. Exit code 2 means no
device observation was obtained. A different connected build is reported as
`PARTIAL`, not as a successful target match.

## Evidence boundaries

- `PASS` means only that Lockdown returned the target's allow-listed metadata.
- `PARTIAL` means a device responded but the declared target did not match exactly.
- `BLOCKED` means no physical-device observation was obtained.
- A passing report does **not** prove kernelcache decoding, kernel-memory access,
  exploitability, jailbreak support, SSH/root access, or full iOS 27.0.1
  compatibility.
- Synthetic unit tests validate report logic only. They are not physical-device tests.
- The tool records a timestamp and observed metadata but does not cryptographically
  authenticate Apple firmware. Keep raw reports private if you later extend the
  schema with personally identifying fields.

## iOS 17 and later

Classic Lockdown metadata and developer/DVT services are separate access paths.
Developer services on modern iOS versions may require a trusted Remote Service
Discovery (RSD) tunnel. This probe deliberately does not create such a tunnel;
add that capability only as a separately consented, explicitly reported mode.
