import Foundation

/// Recognized package file types. Recognition does not imply that a package is safe or installable.
public enum AppArtifactKind: String, Codable, Sendable {
    case ipa
    case deb
    case unsupported
}

public enum ArtifactInspectionStatus: String, Codable, Sendable {
    case recognized
    case unsupported
    case invalidFilename
    case notInspected
}

public struct AppArtifact: Codable, Equatable, Sendable, Identifiable {
    public let id: String
    public let filename: String
    public let kind: AppArtifactKind
    public let byteCount: Int64?
    public let inspectionStatus: ArtifactInspectionStatus

    public init(filename: String, byteCount: Int64? = nil) {
        self.id = filename
        self.filename = filename
        self.byteCount = byteCount
        let trimmed = filename.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty, URL(fileURLWithPath: trimmed).lastPathComponent == trimmed else {
            self.kind = .unsupported
            self.inspectionStatus = .invalidFilename
            return
        }
        switch URL(fileURLWithPath: trimmed).pathExtension.lowercased() {
        case "ipa":
            self.kind = .ipa
            self.inspectionStatus = .recognized
        case "deb":
            self.kind = .deb
            self.inspectionStatus = .recognized
        default:
            self.kind = .unsupported
            self.inspectionStatus = .unsupported
        }
    }
}

/// A policy decision only; this type does not extract, sign, transfer, or install files.
public enum ArtifactInstallStatus: String, Codable, Sendable {
    case requiresSigningAndProvisioning
    case requiresJailbrokenDeviceAndPackageManager
    case blockedOnStockIOS
    case unsupportedArtifact
    case notValidated
}

public struct ArtifactInstallPlan: Codable, Equatable, Sendable {
    public let artifact: AppArtifact
    public let status: ArtifactInstallStatus
    public let prerequisites: [String]
    public let evidence: String

    public init(artifact: AppArtifact, status: ArtifactInstallStatus,
                prerequisites: [String], evidence: String) {
        self.artifact = artifact
        self.status = status
        self.prerequisites = prerequisites
        self.evidence = evidence
    }
}

public struct ArtifactInstallPlanner: Sendable {
    public init() {}

    /// Produces a conservative plan without claiming the package was inspected or installed.
    public func plan(for artifact: AppArtifact, deviceIsJailbroken: Bool = false) -> ArtifactInstallPlan {
        switch artifact.kind {
        case .ipa:
            return ArtifactInstallPlan(
                artifact: artifact,
                status: .requiresSigningAndProvisioning,
                prerequisites: [
                    "Inspect the IPA archive and its Info.plist.",
                    "Validate the code signature, entitlements, and provisioning profile.",
                    "Use an Apple-supported installation/distribution path and an authorized paired device.",
                    "Confirm device eligibility and any Developer Mode or trust requirements."
                ],
                evidence: "Extension recognized only; archive contents, signature, transfer, and installation have not been validated."
            )
        case .deb:
            if deviceIsJailbroken {
                return ArtifactInstallPlan(
                    artifact: artifact,
                    status: .requiresJailbrokenDeviceAndPackageManager,
                    prerequisites: [
                        "Confirm the exact iOS version and jailbreak compatibility.",
                        "Inspect package control metadata and maintainer scripts before installation.",
                        "Use the device's compatible package manager with explicit user confirmation.",
                        "Create a recovery/backup plan; package scripts may modify the system."
                    ],
                    evidence: "Extension recognized only; package contents, compatibility, and installation have not been validated."
                )
            }
            return ArtifactInstallPlan(
                artifact: artifact,
                status: .blockedOnStockIOS,
                prerequisites: [
                    "A .deb is a Debian package, not a normal iOS app bundle.",
                    "Stock iOS does not provide a supported general-purpose .deb installation workflow.",
                    "Do not attempt installation unless a compatible jailbroken environment and package manager are deliberately in use."
                ],
                evidence: "No device state was queried. The planner defaults to stock iOS and does not execute package contents."
            )
        case .unsupported:
            return ArtifactInstallPlan(
                artifact: artifact,
                status: .unsupportedArtifact,
                prerequisites: ["Choose an IPA for supported iOS app-distribution workflows or a DEB for a compatible jailbroken environment."],
                evidence: "The filename extension is not a supported package type."
            )
        }
    }
}
