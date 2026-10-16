# Darwin VM integration plan for PhoneBridge / KernelScope

## Purpose

Use [jprx/darwin-vm](https://github.com/jprx/darwin-vm) as an **optional, isolated research harness** for kernel and system-component analysis. It is not an iPhone emulator with a complete GUI, and its root shell belongs to the guest VM. It does not jailbreak the connected physical iPhone.

## Known upstream evidence (checked 2026-10-16)

The upstream README reports successful boots for iPhone 16 `iPhone17,3` / `t8140` on iOS 27.0 beta 7 build `24A437` and iOS 26.6. This is not the same as the target in this repository: iOS 27.0.1 build `24A446`. Therefore exact-target support remains `NOT_VALIDATED` until a run with the exact IPSW produces logs and hashes that can be reviewed.

Upstream setup says the file preparation and ramdisk permission steps require a Mac. The QEMU fork must be built from its submodule, with upstream notes about disabling PVG for macOS 27 build environments. Do not assume these instructions work unchanged on Windows.

## Integration boundaries

1. Keep the upstream project in a separate checkout; do not copy its scripts into PhoneBridge or run them implicitly.
2. Pin the upstream Git commit and QEMU submodule commit in every report. Do not track floating `main` as reproducible evidence.
3. Verify the IPSW device identifier, version and build against `iPhone17,3`, `27.0.1`, `24A446`; calculate SHA-256 locally. A third-party checksum is a comparison value, not Apple signature verification.
4. Inventory files first. Record each extraction step separately: archive extraction, container decoding, decryption, filesystem extraction and semantic analysis are distinct operations.
5. Hash kernelcache, SPTM, TXM, DeviceTree and ramdisk inputs and outputs. Preserve the exact command, tool version, exit status, logs and output hashes.
6. Treat VM changes as disposable and isolated. Never connect the VM's debug services to an untrusted network; SSH/tunnelling must be bound to loopback or an explicitly controlled interface.
7. Run only trusted, reviewed upstream scripts. Static-audit them before execution; never execute firmware payloads on the host.
8. Separate results into `PASS`, `PARTIAL`, `BLOCKED`, `FAIL`, and `NOT_VALIDATED`. A VM boot cannot produce a physical-device PASS.

## Automated static audit

From the repository root:

```sh
python tools/darwin_vm_audit.py /path/to/darwin-vm --out artifacts/darwin-vm-audit.json
```

Exit codes: 0 = all declared checks passed; 1 = partial/not fully validated; 2 = audit input error. The audit is read-only and does not run any upstream script or QEMU.

## Required evidence to close the gap

- [ ] Record upstream repository commit and `qemu-sptm` submodule commit.
- [ ] Verify exact IPSW metadata and archive SHA-256.
- [ ] Extract the expected kernelcache, SPTM, TXM, DeviceTree and ramdisk, recording missing members explicitly.
- [ ] Boot only after reviewing the scripts and documenting host prerequisites.
- [ ] Preserve complete boot log and identify the actual Darwin/XNU build string.
- [ ] Confirm the VM's build is exactly `24A446`; otherwise report `PARTIAL`.
- [ ] Run KernelScope against the extracted kernelcache and record decoding/analysis status separately.
- [ ] Keep physical iPhone probe results separate from VM results.
- [ ] Do not label root-in-VM, kernel patching in QEMU, or a VM shell as an iPhone jailbreak.

## Current status

`PARTIAL`: upstream darwin-vm has a relevant iPhone 16/T8140 path, but the evidence cited upstream does not establish a boot of this repository's exact iOS 27.0.1 build `24A446`. No VM was launched by this repository change, and no physical-device validation is claimed.
