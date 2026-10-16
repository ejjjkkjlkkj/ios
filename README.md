# iOS Companion — IPA management and iPhone diagnostics

A clean-room Swift project aiming to make iPhone app management and diagnostics simpler than AltStore/SideStore, without requiring iTunes or iCloud.

## Current status

**Prototype / NOT production-ready.** IPA/DEB filename recognition and conservative installation planning exist in the core model. Archive inspection, signing validation, USB transfer, installation, and physical-device diagnostics have not been validated.

## Product goals

- A SwiftUI iPhone app for guided, accessible diagnostics.
- A desktop companion without mandatory iTunes or iCloud dependencies.
- Import and inspect IPA files; transfer/install them only through supported, authorized signing and distribution paths.
- Recognize and inspect DEB packages for compatible jailbroken environments, with safeguards.
- Reports using PASS / FAIL / PARTIAL / BLOCKED / NOT_VALIDATED and evidence.
- Keyboard, VoiceOver, Dynamic Type, and high-contrast-friendly UI.
- Read-only diagnostics by default; explicit confirmation for device-changing operations.

## IPA and DEB support

- **IPA:** the core recognizes the file type and describes required signing/provisioning checks. It does not yet parse or install the archive.
- **DEB:** the core recognizes the file type. Stock iOS is blocked by default because DEB is a Debian package format, not a normal iOS app bundle. A compatible jailbroken environment and package manager would be required; no such installation has been implemented or validated.
- **Transfer:** no USB transfer or app installation is implemented yet. A successful copy must never be reported as a successful installation.

See docs/IPA_DEB_WORKFLOWS.md for the detailed workflow and safety requirements.

## Platform constraint

An ordinary iOS app cannot freely install/sign other apps or access all low-level iPhone diagnostics. App installation outside the App Store still depends on a supported signing/distribution path and varies by region, account, iOS version, and distribution method. A desktop companion may assist with supported workflows, but it cannot legitimately remove Apple's signing and trust requirements.

## Planned architecture

- Sources/PhoneBridgeCore: platform-independent diagnostic and package models.
- Tests/PhoneBridgeCoreTests: automated unit tests.
- App/: SwiftUI iOS user interface (requires Xcode/iOS SDK to build).
- docs/: architecture, roadmap, and package workflows.

## Build core package

Requires Swift 6 toolchain:

```sh
swift test
```

Package tests validate code behavior only; they do not prove iPhone hardware access, app installation, signing, or device-level diagnostics.

## Verification labels

- **PASS** — directly tested with reproducible evidence.
- **FAIL** — test executed and failed.
- **PARTIAL** — only a subset is implemented or validated.
- **BLOCKED** — cannot be validated in the current environment.
- **NOT VALIDATED** — no test evidence yet.

## Security

Never upload device logs, identifiers, pairing records, diagnostic reports, or package contents without explicit user consent. Do not store Apple Account passwords, 2FA codes, or private signing keys in this repository.


## iOS 27.0.1 compatibility
The primary target is **iOS 27.0.1**. The Swift package currently declares iOS 17 as its minimum deployment target; that is not proof of compatibility with iOS 27.0.1. A complete Xcode app project, a build using an SDK that supports iOS 27, and physical-device validation are still required. Status: **NOT VALIDATED**. See `docs/IOS_COMPATIBILITY.md`.
