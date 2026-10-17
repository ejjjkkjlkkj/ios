# Jailbreak research status — iPhone 16 / iOS 27.0.1

**Target:** iPhone 16 `iPhone17,3`, board `D47AP`, platform `t8140`, iOS `27.0.1 (24A446)`.

**Last reviewed:** 2026-10-17. This document is an evidence ledger, not a claim that a jailbreak exists.

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


## Broad research matrix — 2026-10-17

This section records distinct investigation paths so that “search all ways” does not collapse unrelated evidence into a compatibility claim.

### Search paths and current disposition

| Path | What to check | Current disposition for iPhone17,3 / T8140 / 24A446 |
|---|---|---|
| Official vendor security advisories | Apple security releases, CVEs, affected/fixed versions, component names | No published CVE entry specifically attached to iOS 27.0.1 was found in the reviewed Apple release index. This is not proof of absence of vulnerabilities. |
| Public jailbreak projects | Upstream repositories, release assets, supported-device tables, reproducible instructions | Liter8 documents iPhone 11 / n104ap only; no iPhone 16 support claim. |
| Conference demonstrations | Primary announcement, footage, device model, build, post-reboot behavior | Calif demo is reported for iPhone18,2/18 Pro family context and T8160 in coverage; exploit chain and public tool remain unavailable in reviewed sources. No T8140 compatibility evidence. |
| Firmware provenance | Exact IPSW, ZIP integrity, BuildManifest identity, local SHA-256, signing status | Not completed in this session: no local IPSW artifact or hash was available to verify. |
| Static firmware analysis | Archive inventory, kernelcache/DeviceTree/boot components, tool versions, parser coverage, errors | BLOCKED pending the exact verified IPSW. Encrypted payloads must remain BLOCKED until validly decoded. |
| Differential firmware analysis | Compare target build with a prior build for the same product type and component | BLOCKED pending both exact, hashed artifacts. iPhone19,2 diffs are not substitutes for iPhone17,3 inputs. |
| Kernel and mitigation research | XNU source/version, patch diffs, PAC/PPL/SPTM/TXM and platform-specific boundaries | No target-specific exploit path validated. Kernel version strings alone are insufficient evidence. |
| Darwin VM / emulator | Exact input hashes, pinned upstream revisions, complete boot log and guest build evidence | Any VM result would be simulation only; it cannot prove physical-device root or jailbreak. Exact target build boot is NOT_VALIDATED. |
| USB / DFU / restore workflows | Upstream support, host prerequisites, signed ticket/restore behavior, recovery plan | No device operation performed. Do not restore, erase, or enter destructive workflows as part of this read-only audit. |
| Physical device | Read-only model/build collection; only a public compatible method or authorized controlled research; root/SSH/reboot checks separately | NOT_VALIDATED: no physical proof supplied or generated. |
| Scam / unofficial downloads | Claims of one-click jailbreaks, profiles, paid certificates, survey gates | Treat as untrusted unless corroborated by a reputable upstream project and independently reviewable source. Do not install profiles or run unknown binaries. |

### New upstream evidence checked

The public Liter8 README was rechecked. It states that its custom iOS 27 boot path is tethered, requires a Mac and pwned DFU at each boot, and is claimed for iPhone 11 (`n104ap`) only. Its documented restore step erases the phone. Its table lists build `24A446` for iPhone 11; that does not make it an iPhone 16 method.

Source: https://github.com/Xplo8E/Liter8

Recent independent reporting dated 2026-10-16 describes Calif's iPhone 18 Pro demonstration as returning to root SSH after a reboot and normal passcode unlock. It does not publish the exploit chain or establish iPhone 16 / T8140 support.

Sources:
- https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot
- https://gbhackers.com/ios-27-0-1-untethered-jailbreak/

### Decision gates — do not skip

1. **Firmware identity PASS** only when a local IPSW's SHA-256, ZIP CRC, unique BuildManifest and product/build identifiers have been recorded.
2. **Static analysis PASS** only for artifacts actually extracted and parsed; record unsupported/encrypted components as BLOCKED.
3. **VM boot PASS** means only the exact VM configuration booted, not that a physical iPhone is jailbroken.
4. **Exploit compatibility PASS** requires public, reproducible evidence matching the target model/board and build, not just the iOS version.
5. **Physical root/SSH PASS** requires evidence from the actual iPhone 16, separately verifying root, SSH reachability, reboot behavior and recovery.
6. **Overall completion PASS** is forbidden while any mandatory gate is BLOCKED or NOT_VALIDATED.

### CI state

The Swift CI run for this report update, commit `048fdd23067de73b96f4592e9533fce0a997f0b2`, completed successfully:
https://github.com/ejjjkkjlkkj/ios/actions/runs/38973803013

This is the Swift CI workflow only. It is not proof that every workflow or the complete PhoneBridge pull request is green. PR #2's firmware-audit correction CI separately passed but remains unmerged:
https://github.com/ejjjkkjlkkj/ios/pull/2

### Current verdict

- Repository documentation / Swift CI for commit `048fdd2`: **PASS**.
- Firmware-audit fix CI: **PASS**, PR **OPEN / NOT MERGED**.
- Exact target IPSW acquired and verified in this session: **NOT DONE**.
- Target-specific static kernel analysis: **BLOCKED** pending IPSW.
- Public jailbreak chain for iPhone16,3 / `iPhone17,3` / `D47AP` / `T8140` / `24A446`: **NOT_FOUND** in the sources reviewed.
- Physical root SSH and untethered persistence on the target iPhone: **NOT_VALIDATED**.


## CI and source recheck — 2026-10-17 (latest head)

### Exact commit checks
For feature commit `57560db9974f39688a165064c272a5f8a23ee3c1`:
- KernelScope run `38974006158`: **PASS**.
- Swift and Firmware Audit CI run `38974006117`: **IN_PROGRESS** at the time of this check; do not mark the complete PR green.
- The commit check-runs endpoint reports three checks: two **PASS**, one **IN_PROGRESS**.
- PR #1 remains **OPEN / NOT MERGED**, base `main`.
- PR #2 remains **OPEN / NOT MERGED**; its earlier targeted firmware-audit correction run `38973637302` passed, but that does not merge the fix into `main`.

Exact run links:
- https://github.com/ejjjkkjlkkj/ios/actions/runs/38974006158
- https://github.com/ejjjkkjlkkj/ios/actions/runs/38974006117
- https://github.com/ejjjkkjlkkj/ios/pull/1
- https://github.com/ejjjkkjlkkj/ios/pull/2

### Fresh research recheck
A new search on 2026-10-17 found no public, reproducible iPhone 16 / `iPhone17,3` / `D47AP` / `T8140` / iOS 27.0.1 jailbreak release. Recent reporting published 2026-10-16 describes Calif's demonstration on iPhone 18 Pro, with no public exploit/tool or published device support matrix. The described post-reboot sequence included normal passcode unlock before root SSH; it does not prove passcode bypass or T8140 compatibility.

Sources:
- https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot
- https://pasqualepillitteri.it/fr/news/24541/jailbreak-iphone-18-pro-ios-27-calif
- https://github.com/Xplo8E/Liter8 (upstream still documents iPhone 11 / `n104ap` only)

### Work status
- Exact target IPSW downloaded and hashed: **NOT DONE**.
- BuildManifest/product identity checked against a local artifact: **NOT VALIDATED**.
- Target-specific static analysis: **BLOCKED** until the exact IPSW is acquired and its identity verified.
- Physical root/SSH or reboot persistence on the user's iPhone 16: **NOT VALIDATED**.
- Overall completion: **NOT PASS**. CI is not yet fully green for the exact feature commit at this observation.


## CI result update — 2026-10-17 (after completion)

The previously in-progress run for commit `57560db9974f39688a165064c272a5f8a23ee3c1` has completed:
- KernelScope `38974006158`: **PASS**.
- Swift CI `38974001418`: **PASS**.
- Swift and Firmware Audit CI `38974006117`: **FAIL**; failed step is **Test firmware audit tool**.
- The failure means the full feature-branch CI is **NOT GREEN**. PR #1 remains open and unmerged.
- PR #2's standalone correction CI had passed earlier, but its correction has not yet been merged into `main` or incorporated into PR #1's head. The separate passing PR does not override the failure observed on this feature head.

A documentation-only follow-up commit `8d5544c43b431bb0f2d51aec148639ba812fbf56` was pushed after recording the then-current in-progress state. Its Swift CI run `38974105579` was **QUEUED** at the time of this update; this queued run is not evidence that the firmware-audit failure is fixed.

Run links:
- https://github.com/ejjjkkjlkkj/ios/actions/runs/38974006117
- https://github.com/ejjjkkjlkkj/ios/actions/runs/38974006158
- https://github.com/ejjjkkjlkkj/ios/actions/runs/38974001418
- https://github.com/ejjjkkjlkkj/ios/actions/runs/38974105579

Required next code action: rebase/port the already CI-tested missing-manifest status correction into the PhoneBridge branch through a reviewed change, then rerun the complete workflow on the resulting exact head. Do not mark overall CI PASS until that matching run succeeds.


## Follow-up research and CI log verification — 2026-10-17

### CI failure confirmed from the job log
The latest feature-head documentation commit `b60ad51d865c168fcf62d694872ff1aefbdbde0f` has:
- KernelScope run `38974133899`: **PASS**.
- Swift CI run `38974128069`: **PASS**.
- Swift and Firmware Audit CI run `38974133879`: **FAIL**.
- The failing assertion is confirmed from the job log: `test_missing_manifest_is_partial` expected `PARTIAL` but received `NOT_VALIDATED`. Four other firmware-audit tests passed.
- PR #2 contains the one-line fix for that exact return path and its own CI run passed, but PR #2 is still open. Do not claim the feature PR is green or the correction is on `main`.

Evidence:
- Failed job: https://github.com/ejjjkkjlkkj/ios/actions/runs/38974133879
- KernelScope: https://github.com/ejjjkkjlkkj/ios/actions/runs/38974133899
- Swift CI: https://github.com/ejjjkkjlkkj/ios/actions/runs/38974128069
- Fix PR: https://github.com/ejjjkkjlkkj/ios/pull/2

### Primary-source check: Calif announcement
Calif's own post dated 2026-10-16 lists four iPhone demonstrations and says “Everything will be released in due time.” It does not provide a release date, exploit identifiers, source code, a downloadable jailbreak, or a device compatibility matrix. This is evidence of a stated future intention, not a public release and not evidence of iPhone 16 support.

Primary source: https://blog.calif.io/p/iphone

Independent reporting describes the demonstrated device as iPhone 18 Pro / `iPhone19,2` / `T8160` on build `24A446`. The phone was unlocked using its normal passcode after reboot before root SSH was shown. This does not establish passcode bypass, nor does the shared build number establish compatibility with iPhone 16 / `iPhone17,3` / `T8140`.

Coverage: https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot

### Target IPSW metadata cross-check
A current third-party firmware catalog lists iOS 27.0.1 build `24A446` for iPhone 16 `iPhone17,3`, board `D47AP`, platform `t8140`, as signed. This is catalog metadata only; it is not a local artifact, a verified Apple signing response, or a cryptographic authenticity result.

Catalog: https://ipsw.me/iOS/27.0.1/

No IPSW was downloaded in this follow-up. The exact artifact is roughly 12 GB according to catalogs, so archive integrity, local SHA-256, BuildManifest identity, and component inventory remain **NOT DONE** until an artifact is actually obtained and checked.

### Current decision
- Latest observed full feature CI: **FAIL** (firmware-audit regression test).
- KernelScope and Swift checks on the same commit: **PASS**.
- Exact target firmware static analysis: **BLOCKED** pending local IPSW acquisition and identity verification.
- Public reproducible jailbreak for iPhone 16 / `T8140` / iOS 27.0.1: **NOT_FOUND** in reviewed sources.
- Physical root SSH / reboot persistence on the target iPhone: **NOT_VALIDATED**.
- No PR was merged; no device restore or modification was performed.

## Exact-head CI recheck — 2026-10-17 (commit 9c979c7eb1b226be5c6c4263338c383d5f9ec38b)

The three check-runs attached to this exact report/feature head have now completed:
- Firmware audit test job 38974356968 / job 117220087219: **FAIL**.
- Other two check-runs 38974356964 and 38974352904: **PASS**.
- The failed job log confirms the defect: Tools/firmware-audit/test_firmware_audit.py:46, test test_missing_manifest_is_partial, expected report status PARTIAL, got NOT_VALIDATED. The other firmware-audit tests in that run passed.
- This is a real failing CI check on the current feature head, not a pending result. Do not label the full PR CI as green.
- The focused correction remains available in open PR #2: https://github.com/ejjjkkjlkkj/ios/pull/2 . It has not been merged, and this report does not claim its fix is present on this branch.

Exact failed run: https://github.com/ejjjkkjlkkj/ios/actions/runs/38974356968

### Research delta
A fresh source review found no published Calif jailbreak tool or compatibility statement for iPhone 16 / iPhone17,3 / D47AP / T8140. The documented Liter8 upstream explicitly limits its validated target to iPhone 11 (n104ap); its own table marks other models as unverified/experimental, so it is not a valid basis to claim iPhone 16 support: https://github.com/Xplo8E/Liter8

The iPhone 16 firmware catalog still identifies build 24A446 for iPhone17,3, but this remains third-party metadata. The IPSW has **not** been downloaded, hashed, or parsed locally. No target-device test has been performed.

### Current gates
- Exact feature-head full CI: **FAIL**.
- Other two checks on that head: **PASS**.
- Firmware audit missing-manifest behavior: **FAIL**, correction awaiting integration.
- Calif public tool/source release for target: **NOT FOUND** in reviewed sources.
- iPhone 16 target IPSW local inspection: **NOT DONE**.
- Physical jailbreak/root/reboot-persistence proof: **NOT VALIDATED**.
## Further research and PR review audit — 2026-10-17

### Primary and official source check
- Calif's official post dated 2026-10-16 says the demos will be released in due time, but provides no tool download, exploit identifiers, or device compatibility matrix: https://blog.calif.io/p/iphone
- Decrypt's report describes the demonstrated target as iPhone 18 Pro (`iPhone19,2`, T8160), build `24A446`; it says no public tool or bug details are available. The device was unlocked with the regular passcode before root SSH was shown. This is not evidence for iPhone 16 (`iPhone17,3`, T8140), nor passcode bypass: https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot
- Apple's security-release index lists iOS 27.0.1 (24A446) on 2026-09-28 and says no CVE entries are published for that update. This does not establish that the Calif demo uses the two unrelated crash bugs attributed to Calif in earlier iOS 27 notes: https://support.apple.com/en-us/100100
- The IPSW catalog lists iPhone 16 `iPhone17,3_27.0.1_24A446_Restore.ipsw` at approximately 12 GiB and marks it signed. This is catalog status, not a locally verified Apple signature or artifact: https://ipsw.me/iOS/27.0.1/

### Pull-request and CI state
- PR #1 is still open and draft; its head includes the new IPSW validation plan. It has not been merged: https://github.com/ejjjkkjlkkj/ios/pull/1
- PR #2 remains open and unmerged. Its focused CI passed, but the PR review bot reported a failed review status and then reported that its review usage limit had been reached. This is not equivalent to a successful code review; resolve review coverage before treating the change as approved: https://github.com/ejjjkkjlkkj/ios/pull/2
- The PhoneBridge feature head's latest observed firmware audit run still fails because `test_missing_manifest_is_partial` receives `NOT_VALIDATED` instead of `PARTIAL`. The other two checks on that head passed. The new documentation commit has no check runs yet; no full-green result is claimed.

### New evidence boundaries
- Public Calif release for iPhone 16 / T8140 / iOS 27.0.1: **NOT FOUND** in reviewed sources.
- Exact IPSW downloaded, hashed, archive-tested, and manifest parsed locally: **NOT DONE**.
- Exploit chain, kernel offsets, PAC bypass, SEP/passcode bypass, or physical root SSH for target: **NOT VALIDATED**.
- Safe next work: close the test-status defect with a reviewed code change, obtain the exact IPSW from a verified Apple CDN route, and run archive/manifest identity checks before deeper analysis. Do not infer device compatibility from the shared build number.

## Integration gate recheck — 2026-10-17

- PR #1 remains open and draft; GitHub currently reports `mergeable: false`. Resolve the branch/base conflict state and rerun CI before considering it ready for review or merge. No merge performed.
- Latest research-report commit `6385ecedc5235a766a5a696846e1125afc387e3b` has no check-runs returned yet. Its CI state is **NOT VALIDATED**, not PASS.
- PR #2's focused workflow passed, but its review-bot status was failed and the bot reported a usage limit; treat review approval as **NOT VALIDATED** until an actual code review is completed.

## Follow-up from user-provided IPSW Downloads page — 2026-10-17

The user supplied the visible page for iOS 27.0.1 (24A446), iPhone 16. It states the firmware is signed, names `iPhone17,3_27.0.1_24A446_Restore.ipsw`, and says downloads redirect to Apple servers rather than being mirrored by IPSW Downloads. This supports the catalog/source-routing description only. The message contains no completed-download path, byte count, final Apple CDN URL, SHA-256, or local manifest output.

### Latest feature-head checks

Commit `c095907e82805ad53c2c0f3a61df53913d83cd5d` has three completed checks:
- Swift tests: **PASS**.
- KernelScope test workflow: **PASS**.
- Firmware-audit workflow: **FAIL** — `test_missing_manifest_is_partial` expected `PARTIAL`, got `NOT_VALIDATED`. The workflow log confirms four other firmware-audit tests passed and this one failed.
- Latest PR #1 metadata reports `mergeable: true`; PR remains open and unmerged. This does not mean CI is green.
- PR #2 contains the one-line correction and its focused CI passed, but its automated code review failed/was rate-limited. Do not treat that as approved review or assume the correction is on PR #1.

Failure log: https://github.com/ejjjkkjlkkj/ios/actions/runs/38974772898/job/117221448056
PR #1: https://github.com/ejjjkkjlkkj/ios/pull/1
PR #2: https://github.com/ejjjkkjlkkj/ios/pull/2

### Evidence status after the supplied page

- Firmware marked signed by third-party catalog: **PASS (catalog claim only)**.
- Exact IPSW present locally and complete: **NOT VALIDATED**.
- Local SHA-256 / archive integrity / BuildManifest product identity: **NOT DONE**.
- iPhone 16 / `iPhone17,3` / `D47AP` / `t8140` jailbreak, root SSH, or reboot persistence: **NOT VALIDATED**.
- Calif's public iPhone 18 Pro demo does not establish iPhone 16 compatibility; no public reproducible target-specific jailbreak was found in reviewed sources.

Next safe gate: once the download finishes, record the exact path, byte size and SHA-256, then test archive readability and parse `BuildManifest.plist` read-only. Do not restore the phone or run payloads as part of this audit.

## GitHub research follow-up — Liter8 and exact-head CI — 2026-10-17

### Relevant public repository examined

- Upstream: https://github.com/Xplo8E/Liter8
- Current README says the project patches and boots iOS 27 on **iPhone 11 only** (`n104ap`), using a tethered workflow that requires a Mac and pwn DFU for boot.
- Its build table marks iOS 27.0.1 build `24A446` as `run` for iPhone 11. The 11 Pro and 11 Pro Max entries are explicitly `experimental`; the README says no one has confirmed them on those phones.
- This is useful evidence that build `24A446` is not itself sufficient to establish hardware compatibility. It provides **no iPhone 16 / `iPhone17,3` / `D47AP` / `t8140` profile** and is not proof of compatibility with that target.
- Liter8 is not an out-of-the-box answer to the target requirement: its documented workflow is Mac-based and tethered, while the target port has not been validated. Do not run its restore workflow on the target device as part of this read-only research.

### Exact latest commit and CI

- Documentation commit: `986faa6c994d7f3b5099b3c7ab3926ebc5231bb2`.
- Swift CI for that exact commit: **PASS** (run 38975304917): https://github.com/ejjjkkjlkkj/ios/actions/runs/38975304917
- PR #1 remains open and unmerged; GitHub currently reports `mergeable: true`. This only means GitHub does not currently report a merge conflict; it does not establish full CI health or reviewer approval.
- The previously observed firmware-audit failure remains a real failure on the earlier commit `c095907e82805ad53c2c0f3a61df53913d83cd5d`. The latest documentation-only commit's Swift CI success must not be presented as a fix for that test failure. The missing-manifest correction in PR #2 remains separate and unmerged.

### Updated conclusion

- Public code search found no validated Liter8 support profile for the target iPhone 16.
- Exact IPSW download, archive hash and manifest inspection: **NOT VALIDATED**.
- Target-specific exploit, root SSH, and post-reboot persistence: **NOT VALIDATED**.
- No merge, restore, or device modification performed.


## GitHub research update — 2026-10-17 (Airlift and vphone-cli)

### Newly identified public projects

| Project / evidence | Status | Relevance to the physical iPhone 16 target |
|---|---|---|
| `0xjohnnydev/airlift`: AirTraffic path-validation sandbox escape | `PUBLIC_POC` | Upstream README says tested on iOS 27.0 RC (24A435); it describes reading/writing files outside AirTraffic's intended directory scope, with confirmed writes in selected `/var/mobile` paths. This is not a root exploit, kernel exploit, root SSH, or full jailbreak. |
| `YiHoooong/AirliftSilence`: Windows wrapper using Airlift | `TARGET_BUILD_REPORTED` | Its README reports end-to-end file read/replace/restore on iOS 27.0.1 (24A446), over USB with a paired/unlocked device and Apple's Windows device components. This is a project author's report, not independent validation by PhoneBridge. Its demonstrated task modifies call-announcement audio files; it does not demonstrate root or arbitrary system-partition writes. |
| Airlift's iOS 27.0.1 Grappa-session workaround | `PUBLIC_RESEARCH` | AirliftSilence documents that 24A446 rejects sessions without Grappa HostInfo and says it reuses client tokens documented by AirCard-iOS. This may explain why a file-operation PoC was adapted to the target build, but it does not establish privilege escalation. |
| `Lakr233/vphone-cli` compatibility guide and issue #596 / PR #599 | `VM_ONLY_VALIDATION` | Upstream reports iPhone17,3 + iOS 27.0.1 (24A446) boots in its virtualized research guest with cloudOS 26.4 after a TXM pre-check patch. This is a VM/custom-firmware result, not a physical-device jailbreak. Its kernel shared-region patch for iPhone18,x is likewise VM-specific. |
| `Xplo8E/Liter8` compatibility table | `NOT_VALIDATED_FOR_TARGET` | It lists 24A446 as experimental on some devices, but no confirmed iPhone17,3/T8140 profile was found in the reviewed material. Do not infer support from the build number alone. |

### Source links

- Airlift upstream: https://github.com/0xjohnnydev/airlift
- AirliftSilence Windows project: https://github.com/YiHoooong/AirliftSilence
- AirCard-iOS token/reference project: https://github.com/Mak5er/AirCard-iOS
- vphone-cli compatibility guide: https://github.com/Lakr233/vphone-cli/blob/main/Documents/Guides/compatibility.md
- vphone-cli issue #596: https://github.com/Lakr233/vphone-cli/issues/596
- vphone-cli fix PR #599: https://github.com/Lakr233/vphone-cli/pull/599
- Liter8: https://github.com/Xplo8E/Liter8

### Updated assessment

Airlift is the most directly relevant new lead for limited file operations on the exact 24A446 build. It does **not** close the jailbreak objective: the published scope is an AirTraffic sandbox escape with selected mobile-data file access, not kernel privilege escalation or root. No reviewed source demonstrates root SSH, installation of arbitrary DEBs as root, persistence after reboot on a physical iPhone17,3, or a reproducible complete jailbreak for this target.

Next evidence needed:
1. Verify the exact iPhone17,3/24A446 IPSW locally and preserve SHA-256 plus BuildManifest metadata.
2. For Airlift, record the upstream commit/release and exact supported device/build claims; treat any live test as a separate authorized, reversible file-access test.
3. Keep privilege level, accessible path scope, write/read verification, reboot persistence, and physical-device root as separate test results.
4. Do not label VM boot success or a `/var/mobile` file write as physical root or a complete jailbreak.


## GitHub follow-up — Airlift caveats and iOS app port — 2026-10-17

Additional source review found an important qualification:

- Upstream issue [0xjohnnydev/airlift#4](https://github.com/0xjohnnydev/airlift/issues/4) is titled “streaming_zip_conduit is entitlement-gated on iOS 27 — PoC cannot stage on 24A437”. This documents a staging/entitlement obstacle in the original PoC path. It should not be silently treated as resolved for every device/build.
- [AirliftSilence](https://github.com/YiHoooong/AirliftSilence) separately claims end-to-end file read, replacement and restoration on build 24A446, including surviving a reboot. The README does not identify the tested iPhone product type, board, or chip. Therefore it is **build-specific upstream-reported evidence, not proof for iPhone17,3 / D47AP / T8140**.
- [AirliftSilence-iOS](https://github.com/YiHoooong/AirliftSilence-iOS) is a separate on-device app port and documents an unsigned IPA build. This is a delivery/UI variant of the same limited file-operation research, not a new privilege-escalation primitive and not evidence of root.
- AirliftSilence explicitly changes the two call-recording announcement audio files under `/var/mobile/Library/CallServices/Greetings/default/`. Removing that announcement may violate call-recording consent laws. PhoneBridge should not make this modification by default; any research validation must use harmless test files and explicit authorization.

### Updated confidence labels

| Claim | Status |
|---|---|
| Airlift-family file-operation technique has public source code | `PUBLIC_POC` |
| A third-party Windows port reports 24A446 read/write/restore success | `UPSTREAM_REPORTED` |
| That test was performed on the exact iPhone 16 / D47AP / T8140 | `NOT_SPECIFIED` |
| The original PoC's iOS 27 staging/entitlement issue is universally solved | `NOT_VALIDATED` |
| Airlift grants kernel privileges, root SSH, or unrestricted system writes | `NOT_DEMONSTRATED` |
| Airlift supplies a complete jailbreak for this target | `NOT_DEMONSTRATED` |

Source review is not device execution. No Airlift binary was downloaded or run by this repository, and no physical device was modified.

## GitHub follow-up — vphone-cli merged patch and exact-head CI — 2026-10-17

### New source-level finding: vphone-cli PR #599

- Issue [#596](https://github.com/Lakr233/vphone-cli/issues/596) reported a first-boot kernel panic for iOS 27.0.1 (24A446) using vphone-cli 2.6.0.
- The issue was closed by merged [PR #599](https://github.com/Lakr233/vphone-cli/pull/599). Its patch is specifically about the **virtualized research guest**: the cloudOS 26.4 guest kernel's dyld shared region was too small for some iPhone 18 cache sizes; the PR widens that guest region and adds a preflight refusal when a cache cannot fit.
- The PR body explicitly notes that the iPhone17,3 cache size fits the existing guest region. That is a virtual-machine compatibility fact only. It does not establish that a physical iPhone 16 can be jailbroken, booted with custom firmware, or given root SSH.
- The merge is confirmed in GitHub metadata (merged: true); it must not be described as a physical-device exploit.

Sources:
- Issue #596: https://github.com/Lakr233/vphone-cli/issues/596
- Merged PR #599: https://github.com/Lakr233/vphone-cli/pull/599
- Compatibility guide: https://github.com/Lakr233/vphone-cli/blob/main/Documents/Guides/compatibility.md

### Search-quality note: repository named iOS27/Jailbreak

GitHub search surfaced [iOS27/Jailbreak](https://github.com/iOS27/Jailbreak). Its repository metadata reports size 0, one star, and an old push date (2025-05-30); its contents endpoint exposes only a README. No executable, source implementation, release artifact, or target-specific evidence was found there. It is not a usable jailbreak lead.

A direct GitHub API lookup for a guessed califio/iphone repository returned 404. This does not prove Calif has no repositories under any other account or name; the official Calif announcement remains the source reviewed for its stated future release, and no public tool or device matrix was found.

### Exact feature-head CI recheck

For feature branch commit 8985d91028f36aa310903922a579d081046fb94d, GitHub's commit check-runs endpoint now returns three completed checks:
- One check: **FAIL** — https://github.com/ejjjkkjlkkj/ios/actions/runs/38975719386/job/117224555668
- Two checks: **PASS** — https://github.com/ejjjkkjlkkj/ios/actions/runs/38975719218/job/117224554728 and https://github.com/ejjjkkjlkkj/ios/actions/runs/38975714128/job/117224539011

The feature branch is therefore **not green**. The failed check is a real result on this exact head; do not infer that the open PR #2 fix is incorporated merely because PR #2 exists or has its own passing focused run. PR #1 remains open, draft, and unmerged. GitHub reports mergeable: true, which only describes the current merge-conflict assessment.

### Updated assessment

| Claim | Status |
|---|---|
| vphone-cli PR #599 merged | PASS — MERGED |
| vphone-cli proves physical iPhone17,3 jailbreak | NOT_DEMONSTRATED — VM ONLY |
| Public Calif jailbreak tool for iPhone17,3/T8140 | NOT FOUND IN REVIEWED SOURCES |
| Exact feature-head CI | FAIL — 1 FAILED, 2 PASSED |
| Physical iPhone 16 root SSH / reboot persistence | NOT_VALIDATED |
| Exact target IPSW downloaded and locally inspected | NOT DONE |

No device was modified, no IPSW was downloaded in this research pass, and no pull request was merged.

## GitHub follow-up — Darwin VM for iPhone 16 and current CI — 2026-10-17

### New lead: Passw/jprx-darwin-vm

The public repository [Passw/jprx-darwin-vm](https://github.com/Passw/jprx-darwin-vm) describes booting iOS/macOS in QEMU and lists iPhone 16 (`iPhone17,3`, `t8140`) with iOS 27.0 beta 7 as a tested virtualized configuration. Its stated output is a barebones root shell for low-level Darwin research; it explicitly says it is not a full iPhone emulator and does not provide normal graphics, Wi-Fi, Bluetooth, or SpringBoard.

Evidence limits:
- The listed iPhone 16 configuration is iOS 27.0 beta 7 (`24A5424a`), **not** target build 27.0.1 (`24A446`).
- Repository metadata shows one commit dated 2026-08-27 and no published GitHub releases.
- A root shell inside QEMU is a virtual guest result; it is not root on the user's physical iPhone and is not a jailbreak installer.
- It may be useful as a controlled kernel/Darwin research environment, but compatibility with the exact target IPSW remains unverified.

Source: https://github.com/Passw/jprx-darwin-vm

### Feature branch CI after the latest documentation commit

Commit `8cd76e8b2080bcda0ea971a428a2f6d7ccad8626` has three reported checks: two completed **PASS** and one **IN_PROGRESS** at the time checked. This is not yet a fully green, completed CI result. The draft PR #1 remains open and unmerged.

Checks:
- In progress: https://github.com/ejjjkkjlkkj/ios/actions/runs/38975925434/job/117225238414
- Passed: https://github.com/ejjjkkjlkkj/ios/actions/runs/38975925454/job/117225238317
- Passed: https://github.com/ejjjkkjlkkj/ios/actions/runs/38975920852/job/117225223665

### Updated assessment

| Claim | Status |
|---|---|
| iPhone 16 / T8140 can boot a Darwin guest in QEMU on a listed iOS 27 beta build | UPSTREAM_REPORTED — VM ONLY |
| Darwin VM is validated on target build 24A446 | NOT VALIDATED |
| VM root shell proves physical iPhone root | NO — DIFFERENT ENVIRONMENT |
| Public complete physical jailbreak for iPhone17,3 / 24A446 | NOT FOUND IN REVIEWED SOURCES |
| Latest feature-branch CI | 2 PASS, 1 IN PROGRESS at check time |

No device was modified. No IPSW was downloaded or locally analyzed in this pass. No PR was merged.

## Additional GitHub research update — 2026-10-17

### New exact-build evidence (virtual guest only)

| Finding | Status | Interpretation for the physical iPhone 16 target |
|---|---|---|
| `Lakr233/vphone-cli` compatibility guide reports iPhone17,3 / iOS 27.0.1 (24A446) booting in its virtualized guest after a TXM selector-24 admission patch, with `vphoned device.info` responding; bundle 2.6.0 is the first release carrying the fix | `UPSTREAM_REPORTED_VM_PASS` | Useful exact-build Darwin research, but the guide describes a Mac-hosted VM/custom-firmware pipeline. It does not prove an exploit or root SSH on a physical iPhone. |
| `Lakr233/vphone-cli` latest release observed during this review is 2.9.5 (published 2026-10-16) | `RELEASE_FOUND` | Check its release notes and compatibility guide before pinning tools; do not assume release 2.9.5 alone is a physical jailbreak. |
| `Xplo8E/Liter8` README lists iOS 27.0.1 / 24A446 as `run` only for iPhone 11 (`n104ap`); other listed devices are iPhone 11 Pro/Pro Max and explicitly `experimental` | `NOT_COMPATIBLE_WITH_TARGET_AS_DOCUMENTED` | The project explicitly says iPhone 11 only. Do not port its device profile or assume T8140 support. It is tethered and requires a Mac/pwn DFU; its documented workflow erases the device during restore. |
| Calif's 2026-10-16 iPhone 18 Pro demonstration | `REPORTED_NO_PUBLIC_TOOL` | New coverage confirms a live demo and reboot-surviving root on iPhone18 Pro, but no exploit chain/tool or T8140 compatibility has been published in the reviewed evidence. |

### GitHub sources reviewed
- vphone-cli exact-build compatibility matrix: https://github.com/Lakr233/vphone-cli/blob/main/Documents/Guides/compatibility.md
- vphone-cli latest release: https://github.com/Lakr233/vphone-cli/releases/tag/2.9.5
- Liter8 README/device matrix: https://github.com/Xplo8E/Liter8
- Calif demonstration coverage (published 2026-10-16): https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot

### Updated conclusion
The strongest new exact-build result is a **virtual guest boot**, not a physical jailbreak. Liter8 is not a path for this target as documented. The physical iPhone 16 / T8140 / 24A446 still has no publicly reproducible, verified jailbreak chain in the sources reviewed. Keep root SSH, arbitrary DEB installation, and persistence as `NOT_VALIDATED`.

## GitHub follow-up — 2026-10-17 (exact-build VM details and source correction)

### New verification from upstream documentation

| Finding | Status | Evidence / limitation |
|---|---|---|
| `Lakr233/vphone-cli` compatibility guide explicitly reports `iPhone17,3 27.0.1 (24A446)` booting with `26.4-23E5207q` cloudOS and the `txm-boot-precheck_admission` patch; guest `vphoned device.info` responds | `UPSTREAM_REPORTED_VM_PASS` | This is the most exact build-specific VM evidence found. It remains a custom virtual guest, not a physical-device jailbreak. |
| Current `jprx/darwin-vm` README lists `iPhone17,3 / t8140` as booting iOS 27.0 `24A437` and iOS 26.6 | `UPSTREAM_REPORTED_VM_PASS` | The README does not list 27.0.1 `24A446` as a tested pairing. |
| `jprx/darwin-vm/get_files.sh` defaults to iPhone17,3 / 27.0 `24A437` and says preparation/ramdisk patching requires macOS | `HOST_PREREQUISITE_DOCUMENTED` | Do not claim this pipeline has been run on this repository's Windows host. |
| darwin-vm provides root shell and SSH/TCP tunnelling in its VM | `VM_ONLY` | The project explicitly says it is not a full iPhone emulator and does not provide normal SpringBoard, Wi-Fi, Bluetooth, graphics or GUI apps. VM root/SSH is not physical root/SSH. |

### Correction to earlier wording
The currently inspected upstream repository is `jprx/darwin-vm`. Its current README test row is iOS 27.0 `24A437` for `iPhone17,3/t8140`; it should not be described as a verified iOS 27.0 beta 7 `24A5424a` result based on the current matrix. Exact build `24A446` is instead explicitly documented by the separate `vphone-cli` VM compatibility guide.

### Sources reviewed
- https://github.com/jprx/darwin-vm
- https://github.com/jprx/darwin-vm/blob/main/get_files.sh
- https://github.com/Lakr233/vphone-cli/blob/main/Documents/Guides/compatibility.md
- https://github.com/Lakr233/vphone-cli/releases/tag/2.9.5

### Target conclusion unchanged
The exact `24A446` virtual-guest boot is a useful analysis lead, but it does not provide a public, reproducible jailbreak chain for a physical iPhone 16 `T8140`. Physical root, root SSH, arbitrary DEB installation and persistence remain `NOT_VALIDATED`.


## Additional GitHub research — 2026-10-17 (ABrake27 and live CI)

### New public repository reviewed

vvirei333/ABrake27 describes a Linux-native reverse-engineering workflow and a PoC related to the iOS Developer Mode / AMFI lockdown path. Its published comparison is explicitly for **iPhone14,5** (iPhone 13) and compares iOS 27.0.1 with 27.2; it is not a T8140 / iPhone17,3 target-specific analysis.

| Claim | Status | Assessment |
|---|---|---|
| A new public iOS 27 reverse-engineering repository exists | `REPOSITORY_FOUND` | Public source and research documents are available. |
| It provides a complete jailbreak | `NOT_ESTABLISHED` | The README describes Developer Mode activation through Apple's normal lockdown protocol, not a complete kernel privilege-escalation + persistence chain. |
| Its iPhone14,5 findings apply to iPhone17,3 / T8140 | `NOT_VALIDATED` | Different device family and firmware artifacts; no transfer of compatibility is justified. |
| Its ASTC/DDS overflow path is behaviorally confirmed | `NOT_CONFIRMED_BY_REPOSITORY_DESCRIPTION` | The README itself calls for behavioral confirmation of the proposed path. Treat it as a research hypothesis, not a demonstrated exploit. |
| It supplies physical root SSH / arbitrary DEB / untethered persistence for this target | `NOT_FOUND` | No target-specific reproducible chain established by the reviewed materials. |

Source: https://github.com/vvirei333/ABrake27

### Exact-build virtual guest details

The upstream vphone-cli compatibility guide and research index explicitly identify iPhone17,3 / 24A446 virtual-guest testing, including guest-side DeviceHub display research. These are useful for static/dynamic Darwin research on a virtualized custom guest, but remain **VM-only evidence**. They do not demonstrate that the same boot patch works on a physical iPhone or that the physical secure-boot/security boundary has been bypassed.

Sources:
- https://github.com/Lakr233/vphone-cli/blob/main/Documents/Guides/compatibility.md
- https://github.com/Lakr233/vphone-cli/blob/main/Research/Firmware/txm_selector24_cms_gate.md
- https://github.com/Lakr233/vphone-cli/blob/main/Research/Guest/devicehub_screen_viewing.md

### CI snapshot observed during this review

For feature-branch commit `583fd4eaa4f8f359285a00a2c1e46d79dc329eb0`, the latest connector query returned:
- KernelScope run **38976354221**: `SUCCESS`.
- Swift and Firmware Audit CI run **38976354161**: `IN_PROGRESS` at query time; no final conclusion available in that response.

This is a time-of-check snapshot, not proof that all CI has passed. Recheck the run before treating the branch as green.

### Updated verdict

- Exact build 24A446 boots in a custom virtual guest: `UPSTREAM_REPORTED_VM_PASS`.
- ABrake27 is a potentially relevant static-analysis lead, but not a verified jailbreak for the target: `PARTIAL`.
- Public reproducible physical jailbreak for iPhone17,3 / T8140 / 24A446: `NOT_FOUND_IN_REVIEWED_SOURCES`.
- Physical root SSH, arbitrary DEB installation, and reboot persistence: `NOT_VALIDATED`.
- No device was modified, no firmware was flashed, and no PR was merged in this research pass.


## Additional GitHub research — 2026-10-17 (ABrake27, W0lfSword, and VM evidence)

### ABrake27: useful firmware-diff lead, not a jailbreak

The current README for `vvirei333/ABrake27` describes a Linux-native toolkit for comparing iOS 27.0.1 with 27.2, inspecting AMFI dispatch behavior, and enabling Developer Mode through Apple's stock lockdown protocol. The README explicitly labels that flow **“no jailbreak, no unsigned code.”** Its ASTC/DDS/ImageIO path is described as structurally reachable, but behavioral confirmation of the MediaAnalysis delivery path remains open. The documented firmware diff is for iPhone14,5, not the target iPhone17,3.

| Claim | Status | Reason |
|---|---|---|
| ABrake27 offers public iOS 27 reverse-engineering material | `REPOSITORY_FOUND` | Public README and research documents |
| Developer Mode activation equals jailbreak/root | `FALSE` | The project explicitly says the flow is not a jailbreak and uses the stock lockdown protocol |
| ASTC/DDS candidate is a demonstrated exploitable vulnerability | `NOT_VALIDATED` | README says behavioral confirmation is still needed |
| ABrake27 demonstrates a physical iPhone17,3 / T8140 chain | `NOT_FOUND` | Its documented diff target is iPhone14,5; no target chain shown |

Source: https://github.com/vvirei333/ABrake27

### W0lfSword: version range does not reach the target

`kaffeindecaf/W0lfSword` documents support through iOS 26.0.1, not iOS 27.0.1. Its README also distinguishes the toolkit/tweak functionality from a full jailbreak. It is therefore not a candidate for the exact 24A446 target as published.

Source: https://github.com/kaffeindecaf/W0lfSword

### Additional exact-build VM findings

The current public `vphone-cli` research index includes iPhone17,3 / 24A446 guest-specific findings beyond initial boot, including DeviceHub display, host clock synchronization, and a Launchpad app-expansion stall report dated 2026-10-15. These show ongoing VM development and also show that the guest pipeline has operational edge cases. They remain custom-guest results; none is evidence of a physical jailbreak.

Sources:
- https://github.com/Lakr233/vphone-cli/blob/main/Research/Guest/devicehub_screen_viewing.md
- https://github.com/Lakr233/vphone-cli/blob/main/Research/Guest/host_clock_sync.md
- https://github.com/Lakr233/vphone-cli/blob/main/Research/Host/machine_templates.md

### Verdict after this search

- ABrake27: `PARTIAL_RESEARCH_LEAD`, not a jailbreak.
- W0lfSword: `OUT_OF_TARGET_VERSION_RANGE` for iOS 27.0.1.
- vphone-cli exact-build evidence: `UPSTREAM_REPORTED_VM_ONLY`.
- Public, reproducible physical jailbreak for iPhone17,3 / T8140 / 24A446: `NOT_FOUND_IN_REVIEWED_SOURCES`.
- Physical root SSH, arbitrary DEB installation, and persistence: `NOT_VALIDATED`.


## Additional GitHub research — 2026-10-17 (Liter8, vphone-cli 2.6.x, and Calif demo)

### Liter8: real-device evidence, but only for iPhone 11

The public `Xplo8E/Liter8` README reports a tethered iOS 27 jailbreak based on usbliter8 for **iPhone 11 / n104ap only**. It marks iOS 27.0.1 build `24A446` as “run” for that device and says the test involved erase/restore, normal boot, then reboot and boot again. It also lists important missing functionality: SEP, passcode, cellular, Apple services, and reliable tweak injection. The README marks iPhone 11 Pro/Pro Max profiles experimental.

| Claim | Status | Assessment |
|---|---|---|
| Public iOS 27.0.1 jailbreak project with reported physical-device testing exists | `REPORTED_DEVICE_PASS` | Liter8 README reports iPhone 11 / n104ap at 24A446 |
| Liter8 supports iPhone17,3 / T8140 | `OUT_OF_SCOPE` | Maintainer explicitly claims iPhone 11 only; no A18/T8140 port validated |
| Liter8 meets untethered/persistence requirement | `FAIL_FOR_REQUIREMENT` | It is explicitly tethered and requires Mac + pwn DFU for boot |
| Liter8 proves target physical root SSH / DEB install | `NOT_VALIDATED_FOR_TARGET` | Reported capabilities are for a different board and exploit path |

Source: https://github.com/Xplo8E/Liter8

### vphone-cli: exact build boots in a custom virtual guest

The current upstream compatibility guide records that iPhone17,3 / iOS 27.0.1 build 24A446 failed first boot with older bundles because the TXM selector-24 pre-check rejected binaries. Upstream says the `txm-boot-precheck_admission` patch fixes this in the custom guest; bundle 2.6.0 is identified as the first release carrying the patch. The related issue reports successful guest creation and a responding `vphoned` service with the specified pairing.

This is useful evidence for reproducing a **virtual guest boot issue**, not evidence that the patch provides a physical-device jailbreak, bypasses physical secure boot, or yields root SSH on an actual iPhone.

Sources:
- https://github.com/Lakr233/vphone-cli/blob/main/Documents/Guides/compatibility.md
- https://github.com/Lakr233/vphone-cli/issues/596
- https://github.com/Lakr233/vphone-cli

### Calif: significant demonstration, but no public reproducible tool found

Reporting dated 2026-10-16 says Calif demonstrated an untethered iOS 27.0.1 jailbreak on an iPhone 18 Pro at Hexacon, with root SSH returning after reboot. The exploit chain and vulnerabilities were not disclosed in the reviewed coverage, and no public tool was reported as released. The reported device is iPhone 18 Pro / T8160, not the target iPhone 16 / iPhone17,3 / T8140. This is a reported live demonstration, not a source-available implementation or proof of cross-device compatibility.

Sources:
- https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot
- https://pasqualepillitteri.it/en/news/24541/jailbreak-iphone-18-pro-ios-27-calif

### Updated target verdict

- Liter8 on iPhone 11 / 24A446: `UPSTREAM_REPORTED_DEVICE_TEST`; tethered, incomplete, and not transferable to T8140 without evidence.
- vphone-cli on iPhone17,3 / 24A446: `UPSTREAM_REPORTED_VM_PASS`; VM-only.
- Calif iOS 27.0.1 untethered demo: `REPORTED_DEMO_NO_PUBLIC_TOOL_FOUND`; different hardware and undisclosed chain.
- Public, reproducible physical jailbreak for iPhone 16 / iPhone17,3 / T8140 / 24A446: `NOT_FOUND_IN_REVIEWED_SOURCES`.
- Physical root SSH, arbitrary DEB installation, and untethered reboot persistence for the target: `NOT_VALIDATED`.
- No physical device was modified, no firmware was flashed, and no PR was merged in this research pass.


## Additional GitHub/web research — 2026-10-17 (usbliter8 fork scope and target-specific status)

### Cross-check: usbliter8-fun is a separate, narrowly scoped project

The public `34306/usbliter8-fun` repository describes its iOS 27 usbliter8 work as **iPhone 11 Pro only**. Its warning says that restoring the custom firmware can erase the device and break SEP, passcode, Wi-Fi, baseband, Bluetooth (partially), and Apple services. It says other devices require finding correct offsets. This is not a safe or validated route for the target iPhone 16.

Source: https://github.com/34306/usbliter8-fun

| Claim | Status | Assessment |
|---|---|---|
| A second public usbliter8-based iOS 27 project exists | `REPOSITORY_FOUND` | Public repository and source tree found |
| It supports iPhone17,3 / T8140 / 24A446 | `NOT_SUPPORTED_BY_REPO` | README says iPhone 11 Pro only; other hardware needs offsets |
| It preserves normal device functionality | `WARNED_UNSAFE` | README warns about loss of SEP/passcode/Wi-Fi/baseband and Apple services |
| It supplies an acceptable solution for this target | `NO` | Wrong hardware scope and destructive/limited custom-firmware path |

This reinforces the distinction between “a project reports an iOS 27 boot/jailbreak on one older device” and “a reliable jailbreak for this exact iPhone 16.” Do not restore its custom firmware to a primary device.

### Exact target and public status cross-check

The current firmware listing identifies the target as iPhone 16 `iPhone17,3`, board `D47AP`, platform `t8140`, with iOS 27.0.1 build `24A446`. A current compatibility/status page says no public jailbreak is known for iOS 27.0.1 on iPhone 16 Pro; that is a different model (`iPhone17,1`) and is corroborative context only, not direct evidence about `iPhone17,3`.

Sources:
- https://ipswfiles.com/iphone/iPhone17%2C3
- https://www.applefirmwares.com/firmware/iPhone17%2C1/27.0.1

### Research status after this cross-check

- Public usbliter8 work: `DEVICE_SPECIFIC_EXPERIMENTAL`; published scope is iPhone 11 / 11 Pro, with severe functionality warnings.
- ABrake27: `STATIC_RESEARCH_LEAD_ONLY`; its documented firmware comparison is iPhone14,5, and its Developer Mode flow is explicitly not a jailbreak.
- vphone-cli / darwin-vm: `VM_ONLY`; custom-guest root or boot success is not physical-device evidence.
- Calif demonstration: `REPORTED_DEMO_NO_PUBLIC_TOOL_FOUND`; different reported device, exploit details/tool not public in reviewed sources.
- Public, reproducible physical jailbreak for iPhone16 `iPhone17,3 / D47AP / T8140 / 24A446`: `NOT_FOUND_IN_REVIEWED_SOURCES`.
- Physical root SSH, arbitrary DEB installation, and reboot persistence on this target: `NOT_VALIDATED`.
- No device was modified, no firmware was restored, and no PR was merged in this pass.


## Additional research — 2026-10-17 (fresh status check and VM source clarification)

### Fresh public status cross-check

A recently crawled iOS 27.0.1 status page continues to report no stable/public jailbreak for iPhone 16 and newer, and identifies Liter8 as experimental iPhone 11-only work. This is a secondary source, so it is a status cross-check rather than primary exploit evidence.

Source: https://nathanlr.com/ios27-0-1-jailbreak/

A firmware listing for the exact target continues to identify `iPhone17,3`, board `D47AP`, platform `t8140`, build `24A446`, and states that no public jailbreak is known for iPhone 16 on this build. Firmware signing/download status is not evidence of jailbreak compatibility.

Source: https://www.applefirmwares.com/firmware/iPhone17%2C3/27.0.1

### Important source distinction: darwin-vm supports emulated A14–A19 CPUs

The public `Passw/jprx-darwin-vm` README reports that its QEMU-based Darwin environment can boot an iPhone17,3 / T8140 configuration to a root shell, and describes kernel/SPTM/TXM debugging. It explicitly says this is not a full iPhone emulator and does not provide the normal GUI, Wi-Fi, Bluetooth or SpringBoard. The tested matrix refers to iOS 27.0 beta 7 and iOS 26.6, not a demonstrated physical-device jailbreak on 27.0.1 (24A446).

Source: https://github.com/Passw/jprx-darwin-vm

| Claim | Status | Evidence boundary |
|---|---|---|
| QEMU Darwin guest can run a root shell for an emulated T8140 profile | `UPSTREAM_REPORTED_VM_CAPABILITY` | Project README; guest only |
| This validates root on a physical iPhone 16 | `FALSE_INFERENCE` | Emulated root shell does not cross the physical-device trust boundary |
| This proves exact 24A446 physical exploitability | `NOT_VALIDATED` | Documented tested versions differ; no physical chain provided |
| Stable public jailbreak for iPhone17,3 / 24A446 | `NOT_FOUND_IN_REVIEWED_SOURCES` | No reproducible target-specific public tool found in this pass |

### Updated conclusion

The new cross-check did not find a public, reproducible jailbreak chain for physical iPhone 16 / `iPhone17,3 / D47AP / T8140 / 24A446`. Liter8/usbliter8 remain older-device-specific and tethered/experimental; darwin-vm and vphone-cli remain virtual-guest research; Calif remains a reported demonstration without a reviewed public implementation for this target.

Target requirements still `NOT_VALIDATED`: physical root SSH, arbitrary DEB installation, and persistence across reboot. No device was modified, no IPSW was restored, and no PR was merged.


## Additional research — 2026-10-17 (Calif primary statement and exact firmware metadata)

### Calif primary statement checked

Calif's own public newsletter entry dated 2026-10-16 lists the iPhone demo among its Hexacon demonstrations and says the material will be released “in due time.” The entry does not provide exploit identifiers, source code, a downloadable jailbreak, or a supported-device matrix. This is primary evidence that the team announced the demonstration, but not a public implementation for this repository's target.

Source: https://blog.calif.io/p/iphone

Independent reporting describes the on-stage device as iPhone 18 Pro / `iPhone19,2` / T8160 on iOS 27.0.1 build `24A446`, with root SSH returning after reboot. The target in this project is iPhone 16 / `iPhone17,3` / D47AP / T8140. Shared OS build numbers do not establish hardware compatibility.

Sources:
- https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot
- https://cybersecuritynews.com/ios-27-0-1-jailbreak-demonstrated/

### Exact firmware metadata is available, but is not exploit evidence

Public firmware references identify `iPhone17,3_27.0.1_24A446_Restore.ipsw` and list component/key metadata for this build. Such catalogs can help inventory the firmware and plan a static-analysis workflow, but their existence does not prove that a local IPSW has been verified, that every component is decryptable in the user's environment, or that any exploitable vulnerability exists.

Sources:
- https://theapplewiki.com/wiki/Keys:Rave_24A446_%28iPhone17%2C3%29
- https://ipswfiles.com/iphone/iPhone17%2C3

### Research outcome

- Calif public announcement: `PRIMARY_DEMO_ANNOUNCEMENT`; no public implementation or target compatibility matrix in the announcement.
- Reported untethered iOS 27.0.1 demonstration: `REPORTED_ON_IPHONE18_PRO_T8160`; not independently reproduced by this project.
- Exact iPhone 16 / T8140 / 24A446 firmware metadata references: `REFERENCE_FOUND`; no local IPSW inspection claimed.
- Public, reproducible physical jailbreak for iPhone16 `iPhone17,3 / D47AP / T8140 / 24A446`: `NOT_FOUND_IN_REVIEWED_SOURCES`.
- Physical root SSH, arbitrary DEB installation, and reboot persistence for this target: `NOT_VALIDATED`.
- No device was modified, no firmware was restored, and no PR was merged.


## Research continuation — darwin-vm compatibility boundary and fresh GitHub search — 2026-10-17

### Newly cross-checked upstream evidence

- Upstream `jprx/darwin-vm` README lists iPhone 16 (`iPhone17,3`, `t8140`) as tested with **iOS 27.0 beta 8** and iOS 26.6. It describes a minimal virtualized Darwin environment with a root shell, not a full iPhone emulator.
- The same README explains that the guest lacks normal iPhone functionality such as the full GUI, Wi-Fi, Bluetooth, and graphics. VM root is therefore not evidence of physical-device root.
- The upstream table does **not** establish an exact boot of iOS 27.0.1 build `24A446` on the target. Exact-build VM boot remains `NOT_VALIDATED` unless a reproducible run log and hashes for the actual inputs are attached.
- Fresh GitHub searches for `iPhone17,3 T8140 root SSH jailbreak 24A446`, `iOS 27.0.1 exploit kernel privilege escalation T8140`, and a public Calif source release found no new target-specific public exploit or reproducible package. Search results are not exhaustive proof of nonexistence.

### Source

- `https://github.com/jprx/darwin-vm/blob/main/README.md`
- `https://github.com/jprx/qemu-sptm`

### Updated verdict

| Requirement | Status |
|---|---|
| iPhone 16 listed in darwin-vm's iOS 27 beta 8 matrix | `UPSTREAM_REPORTED` |
| Exact target build 24A446 booted in VM with retained logs/hashes | `NOT_VALIDATED` |
| Physical iPhone 16 / T8140 jailbreak tool publicly available | `NOT_FOUND_IN_REVIEWED_SOURCES` |
| Physical root SSH, arbitrary DEB installation, untethered persistence | `NOT_VALIDATED` |

No exploit was executed, no binary was run, no firmware was restored, and no physical device was modified. Continue with read-only firmware provenance and static-analysis work; do not promote VM support, sandbox file access, or matching OS build numbers into a jailbreak claim.


## Research continuation — Calif Hexacon demo and target compatibility — 2026-10-17

### Fresh primary and secondary sources

- Calif's own post, dated 2026-10-16, says it demonstrated four iPhone-related demos at Hexacon and that details will be released later: https://blog.calif.io/p/iphone
- Decrypt's report of 2026-10-16 says Calif demonstrated an untethered iOS 27.0.1 jailbreak on an iPhone 18 Pro, with root access returning after reboot, but no public tool or vulnerability details were available at publication: https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot
- The reported target is iPhone 18 Pro / `iPhone19,2` / `T8160`; PhoneBridge's target is iPhone 16 / `iPhone17,3` / `D47AP` / `T8140`. Same OS build does not prove cross-device exploit compatibility.

### New assessment

| Requirement or claim | Status |
|---|---|
| Calif publicly reported a live untethered jailbreak demo | `PRIMARY_ANNOUNCEMENT + SECONDARY_REPORT` |
| Calif published a reproducible public jailbreak package/source | `NOT_FOUND_AS_OF_2026-10-17_REVIEW` |
| Calif demo proves compatibility with iPhone 16 / T8140 | `NOT_DEMONSTRATED` |
| Vulnerability chain and persistence mechanism publicly documented | `NOT_DISCLOSED_IN_REVIEWED_SOURCES` |
| Physical iPhone 16 root SSH, DEB install, untethered persistence | `NOT_VALIDATED` |

### Work decision

Keep monitoring Calif's official post and linked technical releases. When a release appears, first verify its provenance, license, supported product identifiers/builds, published hashes, and prerequisites; then update the target compatibility matrix. Do not run an unverified payload or restore/modify the phone based only on a headline or same-build claim.

No exploit or payload was executed. No physical device was modified. This report update records public-source research only.
