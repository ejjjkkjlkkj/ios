# iOS Companion — IPA management and iPhone diagnostics

A clean-room Swift project aiming to make iPhone app management and diagnostics simpler than AltStore/SideStore, without requiring iTunes or iCloud.

## Current status

**Prototype / NOT production-ready.** IPA/DEB filename recognition and conservative installation planning exist in the core model. The no-jailbreak scope excludes DEB installation. SSH client/service, archive inspection, signing validation, USB transfer, IPA installation, and physical-device diagnostics have not been validated.

## Product goals

- A SwiftUI iPhone app for guided, accessible diagnostics.
- A desktop companion without mandatory iTunes or iCloud dependencies.
- Import and inspect IPA files; transfer/install them only through supported, authorized signing and distribution paths.
- No DEB installation in the no-jailbreak product scope.
- Provide an authenticated SSH-based connection where the target explicitly runs an SSH server; on stock iOS, use only a limited in-app service, not a system shell.
- Reports using PASS / FAIL / PARTIAL / BLOCKED / NOT_VALIDATED and evidence.
- Keyboard, VoiceOver, Dynamic Type, and high-contrast-friendly UI.
- Read-only diagnostics by default; explicit confirmation for device-changing operations.

## IPA and SSH support without jailbreak

- **IPA:** the core recognizes the file type and describes signing/provisioning prerequisites. It does not yet parse, sign, transfer, or install the archive.
- **DEB:** installation is explicitly out of scope for stock iOS. SSH does not bypass Apple's code-signing, sandbox, or system privilege restrictions.
- **SSH:** planned for authenticated connections to a server the user has explicitly enabled. A normal iPhone does not expose a general-purpose system SSH server; a stock-iOS implementation must be a limited service inside the app, constrained by iOS sandbox and app lifecycle rules. It must not be described as root/system SSH.
- **Transfer:** SSH transfer is not implemented yet. Copying a file must never be reported as successful installation.

See `docs/IPA_DEB_WORKFLOWS.md`, `docs/SSH_STOCK_IOS.md`, and `docs/IOS_COMPATIBILITY.md` for scope and constraints.

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
