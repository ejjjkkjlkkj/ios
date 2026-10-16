# Jailbreak research status — iPhone 16 / iOS 27.0.1

**Target:** iPhone 16 `iPhone17,3`, board `D47AP`, platform `t8140`, iOS `27.0.1 (24A446)`.

**Last reviewed:** 2026-10-16. This document is an evidence ledger, not a claim that a jailbreak exists.

## Evidence ledger

| Claim | Status | Evidence / limitation |
|---|---|---|
| iOS 27.0.1 build 24A446 is listed for iPhone16,3 model identifier iPhone17,3 | `REPORTED` | Third-party firmware catalog; independently verify the downloaded IPSW manifest and hash. |
| Calif demonstrated an untethered jailbreak on iPhone 18 Pro, iOS 27.0.1 | `REPORTED` | Public demonstration reported on 2026-10-16. |
| Calif published a reproducible tool or exploit details | `NOT_AVAILABLE` | Its public post says material will be released later; no reproduction recipe/tool found in sources reviewed. |
| Calif's chain works on T8140 / iPhone17,3 | `NOT_VALIDATED` | Demonstrated model is iPhone19,2 / T8160; matching OS build alone does not establish hardware compatibility. |
| darwin-vm boots iPhone 16 on iOS 27.0 beta 7 / 24A437 | `UPSTREAM_REPORTED` | Upstream support matrix; not a test run by this repository. |
| darwin-vm boots exact build 24A446 | `NOT_VALIDATED` | No verified boot log and matching input hashes attached. |
| Physical iPhone 16 has root / SSH root / persistence | `NOT_VALIDATED` | No physical-device evidence. |

Sources reviewed:
- Calif announcement: https://blog.calif.io/p/iphone
- darwin-vm upstream: https://github.com/Passw/jprx-darwin-vm
- iPhone 16 firmware listing: https://www.applefirmwares.com/firmware/iPhone17%2C3/27.0.1
- ipsw tooling: https://blacktop.github.io/ipsw/docs/cli/ipsw/extract/

## Work plan and completion criteria

### A. Firmware provenance
- [ ] Download the exact `iPhone17,3_27.0.1_24A446_Restore.ipsw` from a trusted source.
- [ ] Record URL, download timestamp, byte size and local SHA-256.
- [ ] Validate ZIP integrity and parse `BuildManifest.plist`; assert product type, product version and build.
- [ ] Preserve the full manifest and a sorted file inventory as artifacts.
- [ ] Never treat a third-party checksum as proof of Apple's signature.

### B. KernelScope extraction and analysis
- [ ] Inventory all archive members before extraction.
- [ ] Record every component's path, size, hash, container type, extraction result and tool version.
- [ ] Extract kernelcache, DeviceTree, SPTM, TXM, boot components and dyld caches where present.
- [ ] Mark decoding, decryption, filesystem extraction and semantic analysis as separate stages.
- [ ] Keep unsupported encrypted AEA/IMG4 payloads explicitly `BLOCKED`; do not infer their contents.
- [ ] Run structural parsers only on verified extracted files; retain parser errors and coverage.
- [ ] Compare against a documented reference build only when both input artifacts are available and hashed.

### C. Darwin VM
- [ ] Pin the upstream source commit and QEMU submodule commit.
- [ ] Review scripts and their downloaded dependencies before executing them.
- [ ] Use a disposable isolated environment; never expose guest debug/SSH services to public interfaces.
- [ ] Record host OS, toolchain, exact IPSW hash, generated artifact hashes and complete boot log.
- [ ] Confirm the actual booted OS build from guest evidence; README mentions alone are not boot proof.
- [ ] If the host prerequisites (upstream currently documents a Mac requirement for file preparation) are unavailable, report `BLOCKED`, not success.
- [ ] Treat guest root as VM-only; never label it physical-device root.

### D. Public vulnerability research
- [ ] Maintain source, disclosure date, affected component, fixed build, affected hardware, public PoC availability and confidence for each candidate.
- [ ] Prefer vendor advisories, source-level patch diffs, reproducible public research and exact build metadata.
- [ ] Reject candidates whose fixed-version range includes the target, unless evidence explains why the target remains affected.
- [ ] Do not attribute Calif's chain to any CVE without a source explicitly establishing that connection.
- [ ] Reassess compatibility independently for T8140 and T8160.

### E. Physical-device validation
- [ ] Capture non-sensitive device/build metadata via the read-only PhoneBridge probe.
- [ ] Use only a publicly released, documented jailbreak explicitly supporting the exact device/build, or a controlled, authorized research PoC.
- [ ] Validate root access, SSH exposure, reboot behavior and recovery independently; do not infer one from another.
- [ ] Record rollback/recovery and backup readiness before any test that can alter the device.
- [ ] Keep results `NOT_VALIDATED` until evidence from the physical target is recorded.

## Why this is not yet a complete jailbreak

A firmware archive, a decoded kernelcache, symbols, a VM shell and even a kernel vulnerability are not individually a jailbreak. A usable jailbreak requires a compatible, reproducible path through the relevant security boundaries and (if persistence is claimed) a separately demonstrated persistence mechanism. No public, reproducible chain for this exact iPhone 16 target was identified in the sources reviewed on the date above.

This repository can automate artifact collection, static analysis, differential analysis, test execution and evidence reporting. It cannot honestly mark the physical jailbreak objective complete until a compatible chain is available and verified on the target. Do not download or run purported “iOS 27 jailbreak” binaries that demand payment, configuration profiles, certificates, or survey-based verification.

## Additional research update — 2026-10-16

### New public evidence

| Finding | Status | Interpretation for this target |
|---|---|---|
| Calif demonstrated untethered root persistence after reboot on iPhone 18 Pro / T8160 / build 24A446 | `REPORTED` | The same OS build exists on multiple hardware families; this is not proof of T8140 compatibility. No public tool or exploit details were found in this review. |
| Public ipsw-diffs comparison exists for iPhone 18 Pro, 27.0 (24A437) vs 27.0.1 (24A446) | `REFERENCE_AVAILABLE` | It reports the same XNU version string on both inputs, 89 updated filesystem Mach-O items, WebKit changes, and an updated ISP firmware item. The inputs are iPhone19,2, not the target iPhone17,3; do not transfer conclusions across devices without target-specific artifacts. |
| CVE-2026-86950 is an out-of-bounds write in Apple's PDF/CoreGraphics processing path | `PUBLIC_ADVISORY` | Apple/NVD describe affected releases before iOS 27 and fixes in iOS 26.7.1 / related releases. This does not establish that the CVE affects iOS 27.0.1 or was used by Calif. |
| DarkSword public chain | `NOT_COMPATIBLE_AS_PUBLISHED` | Google GTIG describes the chain as targeting iOS 18.4–18.7, with component vulnerabilities patched in later releases. It is not evidence of a working chain for iOS 27.0.1. |
| Reddit claims that Calif will release a compatible jailbreak or that DarkSword needs only an SPTM bypass | `UNVERIFIED_COMMUNITY_CLAIMS` | Do not treat community comments as a PoC, a compatibility matrix, or evidence of an available bypass. |

### Sources for this update

- Calif demonstration coverage: https://cybersecuritynews.com/ios-27-0-1-jailbreak-demonstrated/
- Public iPhone 18 Pro build comparison: https://github.com/blacktop/ipsw-diffs/blob/main/iOS/27_0_24A437_vs_27_0_1_24A446/README.md
- NVD CVE-2026-86950: https://nvd.nist.gov/vuln/detail/CVE-2026-86950
- CERT-FR advisory: https://cert.cyber.gouv.fr/avis/CERTFR-2026-AVI-1236/
- Google Threat Intelligence Group, DarkSword: https://cloud.google.com/blog/topics/threat-intelligence/darksword-ios-exploit-chain

### Research priority

1. Obtain and verify the exact iPhone17,3 / 24A446 firmware artifact and preserve its SHA-256 and BuildManifest metadata.
2. Produce a target-device-specific inventory and comparison report; the public iPhone19,2 comparison is context only.
3. Track Calif's official publication and compare any disclosed supported-device/build matrix before considering physical-device testing.
4. Keep all exploit compatibility, kernel boot, and physical root claims `NOT_VALIDATED` until backed by reproducible evidence.

