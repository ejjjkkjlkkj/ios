# iOS Companion — sideloading research and iPhone diagnostics

A clean-room Swift project aiming to make iPhone app management and diagnostics simpler than AltStore/SideStore, without requiring iTunes or iCloud.

## Current status

**Prototype / NOT production-ready.** This repository starts from an empty GitHub repository. No iPhone pairing, app installation, signing, or physical-device diagnostics have been validated yet.

## Product goals

- A SwiftUI iPhone app for guided, accessible diagnostics.
- A companion workflow that does not depend on iTunes or iCloud.
- Clear reports with PASS / FAIL / PARTIAL / BLOCKED and evidence.
- Explain app-signing, provisioning, trust, and Apple platform restrictions honestly.
- Keyboard, VoiceOver, Dynamic Type, and high-contrast-friendly UI.
- No destructive device actions; diagnostics are read-only by default.

## Important platform constraint

An ordinary iOS app cannot freely install/sign other apps or access all low-level iPhone diagnostics. App installation outside the App Store still depends on an Apple-supported distribution/signing path and varies by region, account, iOS version, and distribution method. A desktop companion may help with supported workflows, but it cannot legitimately remove Apple's signing and trust requirements. The project must not claim otherwise.

## Planned architecture

- `Sources/PhoneBridgeCore`: platform-independent diagnostic models and report serialization.
- `Tests/PhoneBridgeCoreTests`: automated unit tests.
- `App/`: SwiftUI iOS user interface (requires Xcode/iOS SDK to build).
- `docs/ARCHITECTURE.md`: security boundaries, implementation roadmap, and verification labels.

## Build core package

Requires Swift 6 toolchain:

```sh
swift test
```

The Swift package tests do not prove iPhone hardware access, app installation, signing, or device-level diagnostics.

## Verification labels

- **PASS** — directly tested with reproducible evidence.
- **FAIL** — test executed and failed.
- **PARTIAL** — only a subset is implemented or validated.
- **BLOCKED** — cannot be validated in the current environment.
- **NOT VALIDATED** — no test evidence yet.

## Security

Never upload device logs, identifiers, pairing records, or diagnostic reports without explicit user consent. Do not store Apple Account passwords, 2FA codes, or private signing keys in this repository.
