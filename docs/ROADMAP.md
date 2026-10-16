# Roadmap — maximize useful functionality

## Phase 1 — Core
- [x] Evidence-labelled diagnostic model and deterministic JSON report.
- [x] Baseline capability matrix and local diagnostic engine.
- [x] Initial SwiftUI dashboard source and unit tests.
- [x] macOS Swift CI workflow.
- [x] Recognize IPA and DEB filenames and create conservative installation plans.

## Phase 2 — Build and validate
- [ ] Run CI and fix actual compiler/test failures.
- [ ] Add an Xcode project/workspace and app target.
- [ ] Build for iOS Simulator with a pinned Xcode/SDK.
- [ ] Validate VoiceOver, Dynamic Type, and contrast manually.
- [ ] Add dependency and secret scanning.

## Phase 3 — On-device diagnostics
- [ ] Add public-API checks for OS/app versions and app-visible state.
- [ ] Add battery state only through APIs actually exposed to the app.
- [ ] Add storage/network checks with documented API limitations.
- [ ] Export redacted reports and require consent before sharing.

## Phase 4 — Desktop bridge, no mandatory iTunes/iCloud
- [ ] Define a versioned device protocol with safe file streaming and digest verification.
- [ ] Investigate libimobiledevice/usbmuxd support and licensing per desktop OS.
- [ ] Implement read-only device discovery and pairing state first.
- [ ] Test with real iPhones across supported iOS versions.
- [ ] Add authorized IPA transfer/installation only where supported.

## Phase 5 — IPA inspection and installation
- [ ] Parse IPA ZIP structure and Payload/*.app/Info.plist.
- [ ] Validate signatures, entitlements, provisioning profiles, expiration, and device eligibility.
- [ ] Use user-owned signing assets and protect keys in OS keychain.
- [ ] Use documented signing and distribution methods only.
- [ ] Verify installation with device-side evidence; transfer is not proof of installation.

## Phase 6 — DEB inspection and guarded installation
- [ ] Parse Debian ar archive and control metadata without executing maintainer scripts.
- [ ] Detect architecture, dependencies, conflicts, scripts, and package-manager requirements.
- [ ] Block installation on stock iOS; require an explicitly detected compatible jailbroken environment.
- [ ] Review system-changing actions and scripts before confirmation.
- [ ] Integrate only with a compatible package manager; do not blindly extract packages as root.
- [ ] Test supported rootless/rootful environments and provide recovery guidance.

## Phase 7 — Optional specialized coding AI
- [ ] Create a separate optional Swift code assistant module.
- [ ] Prefer local models through a pluggable provider interface where hardware permits.
- [ ] AI suggestions never count as test evidence.
- [ ] Require explicit approval before AI-generated changes or device actions.
- [ ] Do not send IPA files, logs, UDIDs, pairing records, or signing secrets to cloud models by default.

## Release gate
A release is not ready until CI passes, the iOS app builds with Xcode, security review is complete, and device-specific features are validated on physical devices. Simulator/QEMU results are not physical-device proof.


## iOS 27.0.1 compatibility gate
- [ ] Build with an Xcode/iOS SDK that supports iOS 27.
- [ ] Validate install, launch, file import, permissions, and VoiceOver on a physical iOS 27.0.1 device.
- [ ] Keep iOS 17 as the package minimum unless a specific feature requires a higher version; use availability checks.
- [ ] Do not label iOS 27.0.1 as supported until build, CI, and physical-device evidence are recorded.
