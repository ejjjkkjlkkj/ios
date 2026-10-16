# IPA and DEB workflows

## Goal

PhoneBridge is intended to accept local IPA and DEB files, inspect them, explain compatibility, and—when a supported and authorized path exists—coordinate transfer/installation through a desktop companion. The current implementation only recognizes filenames and creates a conservative installation plan. It does not inspect archive bytes, transfer files, sign packages, or install anything yet.

## IPA (ordinary iOS app package)

Planned flow:
1. Import an IPA from Files or the desktop companion.
2. Validate the archive structure and read Payload/<App>.app/Info.plist.
3. Inspect code-signing metadata, entitlements, embedded provisioning profiles, minimum iOS version, architecture, and bundle identifier.
4. Explain whether the signing/provisioning arrangement is compatible with the target device.
5. Pair with the device through an authorized desktop workflow.
6. Transfer and request installation using a supported Apple/developer interface.
7. Verify the result from device-side evidence and report any error without claiming success based only on a successful transfer.

An IPA extension alone does not establish validity, trust, or installability. Signing and provisioning requirements remain in force. No bypass is promised.

## DEB (Debian package)

A DEB is not an ordinary iOS application bundle. Installing it on iPhone generally belongs to a compatible jailbroken environment with a suitable package manager. It is blocked by default for stock iOS.

Planned guarded flow for a user-confirmed compatible environment:
1. Inspect the ar archive and Debian control metadata.
2. Read package name, version, architecture, dependencies, conflicts, and maintainer scripts.
3. Check device/jailbreak/package-manager compatibility where reliably detectable.
4. Show all changes and scripts before installation; require explicit confirmation.
5. Use the environment's compatible package manager rather than blindly extracting files into the system.
6. Capture exit status and post-install evidence; support cancellation and recovery guidance.

DEB packages can run maintainer scripts and alter system files. Never treat a filename or metadata parse as a safety guarantee. No rootless/rootful compatibility is assumed until explicitly detected and tested.

## Transfer protocol requirements

The future desktop bridge must use a versioned, authenticated local protocol; validate paths and file sizes; stream files in bounded chunks; calculate and verify a cryptographic digest on both ends; reject traversal and unexpected file types; never log secrets; and require explicit user approval before any device-changing action. Discovery and diagnostics should be read-only by default.

## Current status

- File-extension recognition for IPA/DEB: implemented in the core model.
- Conservative install planning and stock-iOS DEB block: implemented in the core model.
- Archive parsing, signature validation, USB transfer, device installation, DEB script review/execution, and physical-device validation: not implemented / not validated.
