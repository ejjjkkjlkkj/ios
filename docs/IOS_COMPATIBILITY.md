# Compatibility matrix — iOS 27.0.1

## Target requested

- **Primary target:** iOS 27.0.1.
- **SDK/build target:** latest stable Xcode and iOS SDK that officially support iOS 27.0.1.
- **Minimum deployment target in the current Swift package:** iOS 17. This is a source-compatibility floor, not proof that the app has been built or tested on every iOS release.
- **Current validation status for iOS 27.0.1:** NOT VALIDATED. The repository currently has no complete Xcode app project or device-test evidence.

Apple's developer release listing records iOS 27.0.1 (build 24A446), released September 28, 2026. Check Apple's release page and the Xcode release notes before pinning CI to a particular SDK version:
- https://developer.apple.com/news/releases/
- https://developer.apple.com/documentation/xcode-release-notes/

## Compatibility requirements

1. Compile and link the iOS app using an Xcode version whose SDK supports iOS 27.
2. Keep the package deployment target at iOS 17 unless a feature genuinely requires a higher minimum; gate newer APIs with availability checks.
3. Test installation, launch, permissions, background/foreground behavior, file import, and VoiceOver on an actual iOS 27.0.1 device.
4. Test IPA signing/provisioning and device eligibility separately from file parsing. An IPA that parses successfully is not necessarily installable.
5. Do not claim support for iOS 27.0.1 until the Xcode build, automated tests, and physical-device checks pass.

## IPA installation constraints

Apple's documented workflow for installing an exported IPA on registered devices requires the appropriate signing/provisioning setup and may require Developer Mode. The product must detect and explain these prerequisites; it must not promise to bypass signature validation, provisioning, trust, or platform restrictions.

Reference: https://developer.apple.com/documentation/xcode/distributing-your-app-to-registered-devices

## DEB compatibility constraints

iOS 27.0.1 does not turn Debian packages into ordinary iOS apps. The app should refuse DEB installation on stock iOS. Support for DEB must be isolated to a compatible jailbroken environment and package manager, with explicit warnings and physical-device validation. That path is currently NOT IMPLEMENTED.
