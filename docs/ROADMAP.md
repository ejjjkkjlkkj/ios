# Roadmap — maximize useful functionality

## Phase 1 — Core (in repository)
- [x] Evidence-labelled diagnostic data model.
- [x] Deterministic JSON export model.
- [x] Baseline capability matrix with explicit restrictions.
- [x] Local diagnostic engine that does not claim hardware proof.
- [x] Initial SwiftUI dashboard source.
- [x] Unit tests for status semantics.
- [x] macOS Swift CI workflow.

## Phase 2 — Build and validate
- [ ] Run CI and fix actual compiler/test failures.
- [ ] Add an Xcode project/workspace and app target.
- [ ] Build for iOS Simulator with a pinned Xcode/SDK.
- [ ] Validate VoiceOver, Dynamic Type, and contrast manually.
- [ ] Add dependency and secret scanning.

## Phase 3 — On-device diagnostics
- [ ] Add public-API checks for OS/app versions and app-visible state.
- [ ] Add battery state only through APIs actually exposed to the app; do not promise battery health if unavailable.
- [ ] Add storage/network checks with documented API limitations.
- [ ] Export redacted reports and require consent before sharing.

## Phase 4 — Desktop bridge, no mandatory iTunes/iCloud
- [ ] Define a protocol boundary between UI and device adapter.
- [ ] Investigate libimobiledevice/usbmuxd support and licensing per Windows/macOS/Linux.
- [ ] Implement read-only device discovery and pairing state first.
- [ ] Test with real iPhones across supported iOS versions.
- [ ] Add installation/log retrieval only where supported and authorized.
- [ ] Keep destructive operations disabled by default.

## Phase 5 — Signing and installation
- [ ] Inspect IPA structure and metadata locally.
- [ ] Validate signatures/provisioning profiles and explain failures.
- [ ] Use user-owned signing assets; protect keys in OS keychain.
- [ ] Support documented installation/distribution methods only.
- [ ] Show expiration, device eligibility, entitlements, and capability restrictions.
- [ ] Do not promise a signing or trust bypass.

## Phase 6 — Optional specialized coding AI
- [ ] Create a separate, optional Swift code assistant module.
- [ ] Use local models through a pluggable provider interface where hardware permits.
- [ ] Keep static analysis deterministic; AI suggestions never count as test evidence.
- [ ] Require explicit approval before AI-generated changes or device actions.
- [ ] Do not send IPA files, logs, UDIDs, pairing records, or signing secrets to cloud models by default.

## Release gate
A release is not ready until CI passes, iOS app builds with Xcode, security review is complete, and device-specific features are validated on physical devices. Simulator/QEMU results are not physical-device proof.
