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

## Target IPSW verification tool — 2026-10-16

Added `tools/verify_target_firmware.py` and synthetic tests in `tests/test_verify_target_firmware.py`.

Run against an already-downloaded IPSW:

```sh
python tools/verify_target_firmware.py path/to/iPhone17,3_27.0.1_24A446_Restore.ipsw --out target-firmware-report.json
```

The verifier calculates SHA-256, checks ZIP CRC integrity, parses the unique `BuildManifest.plist`, and compares ProductType, ProductVersion, ProductBuildVersion, and BuildIdentities device classes with the requested target. A mismatch fails closed. The default target is iPhone17,3 / D47AP / iOS 27.0.1 / 24A446.

The tool does **not** download firmware, verify Apple's cryptographic signature, decrypt IMG4/AEA payloads, exploit the device, flash firmware, or prove a physical jailbreak. Its success means only that the local archive is structurally readable and its manifest metadata matches the requested target. Apple authenticity remains `NOT_VALIDATED`.

The CI workflow now syntax-checks this tool and its tests and runs the full unittest discovery suite. CI results remain unverified until a matching GitHub Actions run is observed.

## Official Calif release statement — 2026-10-16 update

Calif's own public post says: “Everything will be released in due time.” It lists four demonstrations (Signal one-click, iMessage, an additional iPhone capability demo, and “Apple Persistent Threat”), but provides no exploit identifiers, source code, package, device-support matrix, or release date. This is a statement of future intent, not a public release or a promise that iPhone 16 / T8140 is supported. Source: https://blog.calif.io/p/iphone

New coverage on 2026-10-16 independently describes the stage demonstration as an iPhone 18 Pro / iPhone19,2 / T8160 running 24A446. The device was unlocked with its normal passcode before root SSH was shown; this does not demonstrate lock-screen bypass. No report reviewed establishes compatibility with iPhone17,3 / T8140. Source: https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot

### CI finding

The KernelScope workflow passed on the target-firmware-verifier change. A separate “Swift and Firmware Audit CI” run failed in the pre-existing `Tools/firmware-audit` suite: `test_missing_manifest_is_partial` expected `PARTIAL` but received `NOT_VALIDATED`. This is a real unresolved CI failure, unrelated to the new `tools/verify_target_firmware.py` tests. The corresponding files are not present on this branch, so no speculative patch was made. Track and repair that failure in the branch that owns `Tools/firmware-audit` before declaring the overall PR green.

### Current evidence verdict

- Calif demo on iPhone 18 Pro / iOS 27.0.1: **REPORTED**, with official announcement of demonstrations; technical exploit details remain undisclosed.
- Public downloadable jailbreak: **NOT_FOUND** in sources checked on 2026-10-16.
- iPhone 16 / iPhone17,3 / T8140 / build 24A446 compatibility: **NOT_VALIDATED**.
- Physical root / SSH on the user's iPhone 16: **NOT_VALIDATED**.
- Firmware verifier synthetic unit tests: committed; do not claim passed until the new matching CI run completes successfully.


## Apple advisory cross-check and latest CI — 2026-10-16

Apple's official security-release index currently states that iOS 27.0.1 has **no published CVE entries**: https://support.apple.com/fr-fr/100100. Interpret this narrowly: no CVE entries are published for that update; it does **not** prove the OS has no vulnerabilities, and it does not identify or explain Calif's demonstrated chain. The same build number across iPhone models is not evidence of a shared exploit path.

A current third-party firmware index lists build 24A446 as signed for iPhone17,3 and iPhone19,2, but that listing is not Apple's cryptographic signature verification and does not establish jailbreak compatibility: https://ipsw.dev/build/24A446.

### Latest observed CI run for this branch

Run 38966917928 (**KernelScope**) completed successfully. Run 38966917986 (**Swift and Firmware Audit CI**) failed again at `Tools/firmware-audit/test_firmware_audit.py::test_missing_manifest_is_partial`: expected `PARTIAL`, got `NOT_VALIDATED`. Swift package validation and tests passed; the failure is specifically in the firmware-audit unit suite. The audit files are not present in this feature branch's tree, so this branch cannot safely repair the owning implementation without locating its authoritative branch first.

- KernelScope run: https://github.com/ejjjkkjlkkj/ios/actions/runs/38966917928
- Firmware Audit CI run: https://github.com/ejjjkkjlkkj/ios/actions/runs/38966917986
- Official Apple security-release index: https://support.apple.com/fr-fr/100100
- Build catalog (third-party): https://ipsw.dev/build/24A446

**Updated verdict:** overall CI is **FAIL** due to the separate firmware-audit test. The exact physical-device jailbreak objective remains **NOT_VALIDATED**.

## Security-advisory distinction — 2026-10-16 follow-up

Apple's official security-release index labels iOS 27.0.1 as having “no published CVE entries” (release dated 28 September 2026): https://support.apple.com/en-us/100100. This is a statement about published CVE entries, not a claim that the build has no vulnerabilities.

Decrypt's 16 October coverage reports that Apple's separate iOS 27 security notes credit Calif.io, in collaboration with Claude and Anthropic Research, for two bugs that could cause denial of service or a system crash. The report explicitly says neither is tied to the demonstrated jailbreak: https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot. Do not associate those crash bugs with a kernel privilege escalation or persistence chain without primary evidence.

The public video reportedly shows the iPhone 18 Pro being unlocked with its normal passcode after reboot before a root SSH session is displayed. This is evidence for the demonstrated post-unlock state, not for bypassing the passcode screen.

### Research conclusion after this cross-check

- iOS 27.0.1: Apple currently lists no published CVE entries for this update.
- Calif-associated crash/denial-of-service bugs: reported separately; relationship to jailbreak **NOT_ESTABLISHED**.
- iPhone 16 / T8140 compatibility: **NOT_VALIDATED**.
- Public, reproducible jailbreak package for the exact target: **NOT_FOUND** in the sources reviewed.
- Physical root/SSH/persistence on the user's device: **NOT_VALIDATED**.


## Follow-up research and verifier test hardening — 2026-10-17

### Fresh source cross-check
- Apple's official security-release index still lists iOS 27.0.1 as having no published CVE entries. This means no CVE IDs are published for that release; it does not establish that the release has no vulnerabilities: https://support.apple.com/fr-fr/100100
- Decrypt's 16 October coverage explicitly distinguishes the two Calif-associated crash/denial-of-service bugs from the demonstrated jailbreak; no source reviewed ties those bugs to the jailbreak chain: https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot
- The report describes a normal passcode unlock after reboot before root SSH is shown. This does not establish a passcode bypass.
- No new public reproducible package or T8140/iPhone17,3 compatibility evidence was found in this follow-up review.

### Repository changes
Extended `tests/test_verify_target_firmware.py` with:
- duplicate root/nested manifest detection, which must fail closed and leave target identity unvalidated;
- malformed plist handling;
- stronger assertions for the missing-manifest case, including explicit `NOT_VALIDATED` for target identity and Apple authenticity.

Commit: `5b225874b0c6b8e764a53e56336cbf607f8a466e`.

### Validation state
The new test commit has been pushed to `feature/phonebridge-kernelscope-audit`, but no matching Actions result was returned when queried. Therefore these added tests are **NOT_VALIDATED by CI** until a run for this commit is observed. The latest observed separate Firmware Audit CI failure remains unresolved; do not declare overall CI green.


## Additional public candidate checked — Liter8 / usbliter8 — 2026-10-17

### Evidence found
- Public repository: https://github.com/Xplo8E/Liter8
- The project README claims a working, tethered custom-iOS-27 boot path with root SSH and package management on **iPhone 11 (n104ap) only**. The author explicitly says no other A13 model is claimed.
- Its compatibility table lists iOS 27.0.1 build 24A446 as tested on iPhone 11, but marks iPhone 11 Pro / Pro Max experimental and does not list iPhone 16 / iPhone17,3 / T8140.
- The workflow is tethered: the README says every boot requires a Mac and pwned DFU. It also warns that the custom-firmware restore step erases the phone.
- The project states several functions remain incomplete (including SEP, passcode, cellular data, and Apple services).

### Target verdict
| Claim | Status | Reason |
|---|---|---|
| Public iOS 27.0.1-related project exists | REPORTED | Public Liter8 repository and README |
| Root SSH on iPhone 11 | UPSTREAM_REPORTED | Project author's device-specific claim; not independently reproduced here |
| Liter8 supports iPhone 16 / T8140 | NOT_SUPPORTED_AS_PUBLISHED | The README limits its claim to iPhone 11 / n104ap; target model absent |
| Calif's iPhone 18 Pro chain is the same method as Liter8 | NOT_VALIDATED | No source establishes a relationship |
| Physical jailbreak on this repository owner's iPhone 16 | NOT_VALIDATED | No target-device evidence |

This is a meaningful new public lead for iOS 27 research, but **not a solution for the iPhone 16 target**. Do not port its device-specific patch profiles or infer compatibility from the shared build number. Before any future physical experiment, review the full code and recovery path; its documented restore step is destructive. This repository's audit workflow remains read-only and must not execute Liter8 or restore firmware.

Source checked: https://github.com/Xplo8E/Liter8 (README and device/build matrix, reviewed 2026-10-17).


## CI follow-up — 2026-10-17

The complete CI failure is **not explained solely by a stale PR merge base**. The failing PR run `38973232945` reports `test_missing_manifest_is_partial`: the checked-out implementation returns `NOT_VALIDATED` where the test expects `PARTIAL`. The fix exists on the separate branch `feature/fix-firmware-audit-missing-manifest-status` and that branch's run `38973187844` completed successfully, but the fix is **not present in the PhoneBridge feature branch or current `main` source**. The current `main` head `b7372deff1dfc598e32405bab71404a30605f614` contains a separate baseline capability fix; it must not be described as containing the firmware-audit correction.

- Current `main` head: https://github.com/ejjjkkjlkkj/ios/commit/b7372deff1dfc598e32405bab71404a30605f614
- Corrective branch CI: https://github.com/ejjjkkjlkkj/ios/actions/runs/38973187844
- Failing PhoneBridge PR CI: https://github.com/ejjjkkjlkkj/ios/actions/runs/38973232945

**Required validation:** incorporate the tested correction through an explicitly reviewed change and obtain a fresh CI run for the resulting PR head. KernelScope success alone does not establish that the complete workflow passes. No PR merge was performed.


## Follow-up work — 2026-10-17

### Firmware audit correction re-proposed against current main

Created branch `fix/firmware-audit-main-missing-manifest-status` from current `main`, applied the one-line status correction, and opened PR #2:
- PR: https://github.com/ejjjkkjlkkj/ios/pull/2
- Commit: https://github.com/ejjjkkjlkkj/ios/commit/4a30bf2b94461c440678ab8a5c9928f979d6101d
- CI run: https://github.com/ejjjkkjlkkj/ios/actions/runs/38973637302

At the time of this update, PR #2 is open and the CI run is queued. The patch has not been merged; final validation is pending.

### Fresh public-source check for the target device

The latest reporting on Calif's Hexacon demonstration still describes an iPhone 18 Pro on iOS 27.0.1 with root SSH returning after reboot, but says the exploit details and tool have not been released. No public source found in this check establishes that this chain supports iPhone 16 / `iPhone17,3` / `T8140`. The iPhone 11-only Liter8 lead remains device-specific and is not evidence for T8140.

- Reporting, 2026-10-16: https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot
- Liter8 upstream: https://github.com/Xplo8E/Liter8

Target-device jailbreak and physical root SSH remain `NOT_VALIDATED`. No IPSW was downloaded or analyzed in this work session, and no physical device test was performed.


## Follow-up — CI resolution and target evidence — 2026-10-17

### Firmware-audit correction validated

The PR #2 CI run has now completed successfully:
- Run: https://github.com/ejjjkkjlkkj/ios/actions/runs/38973637302
- Result: `success`
- The job passed Swift package validation/tests, firmware-audit compilation and firmware-audit tests, including the missing-manifest regression test, plus whitespace checks.
- PR #2 remains **OPEN / NOT MERGED**. This validates the proposed fix against its PR baseline; it does not mean the correction is already on `main`.

PR: https://github.com/ejjjkkjlkkj/ios/pull/2  
Fix commit: `4a30bf2b94461c440678ab8a5c9928f979d6101d`

### Latest public target check

A current third-party firmware listing identifies the target as iPhone 16 `iPhone17,3`, board `D47AP`, platform `t8140`, and lists build `24A446` as signed. The same listing says no public jailbreak is known for this exact target/build. This is a catalog report, **not** independent verification of Apple's signing service or the authenticity of a local IPSW.

The Calif demonstration remains specific to iPhone 18 Pro / `iPhone19,2` / `T8160`; the matching build number `24A446` does not establish cross-device exploit compatibility. Liter8's upstream README still explicitly claims iPhone 11 / `n104ap` support, not iPhone 16.

Sources:
- Target firmware listing: https://www.applefirmwares.com/firmware/iPhone17%2C3/27.0.1
- Calif demo coverage, 2026-10-16: https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot
- Liter8 upstream support matrix: https://github.com/Xplo8E/Liter8

### Current status after this update

- PR #2 firmware-audit correction CI: **PASS**.
- PR #2 merged into `main`: **NO**.
- Exact target IPSW downloaded, SHA-256 recorded, and BuildManifest checked in this session: **NOT DONE**.
- IPSW cryptographic authenticity verified: **NOT_VALIDATED**.
- Public reproducible jailbreak for iPhone 16 / `T8140` / iOS 27.0.1: **NOT_FOUND** in sources reviewed.
- Physical root SSH / reboot persistence on the target iPhone 16: **NOT_VALIDATED**.
- Overall PhoneBridge feature-branch CI: **NOT_DECLARED_GREEN** until a matching complete run is observed after the firmware-audit fix is integrated and the relevant workflows pass.

Next concrete task: obtain the exact target IPSW in a controlled environment, record its local SHA-256 and byte size, then run the repository's read-only target-firmware verifier. Do not restore or modify the device as part of this audit.
