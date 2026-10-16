import XCTest
@testable import PhoneBridgeCore

final class AppArtifactTests: XCTestCase {
    func testIPAIsRecognizedButRequiresSigningAndProvisioning() {
        let artifact = AppArtifact(filename: "Example.ipa", byteCount: 1024)
        XCTAssertEqual(artifact.kind, .ipa)
        XCTAssertEqual(artifact.inspectionStatus, .recognized)

        let plan = ArtifactInstallPlanner().plan(for: artifact)
        XCTAssertEqual(plan.status, .requiresSigningAndProvisioning)
        XCTAssertTrue(plan.prerequisites.contains { $0.localizedCaseInsensitiveContains("signature") })
        XCTAssertTrue(plan.evidence.contains("have not been validated"))
    }

    func testDEBIsBlockedByDefaultOnStockIOS() {
        let artifact = AppArtifact(filename: "tweak.deb")
        let plan = ArtifactInstallPlanner().plan(for: artifact)
        XCTAssertEqual(artifact.kind, .deb)
        XCTAssertEqual(plan.status, .blockedOnStockIOS)
    }

    func testDEBOnExplicitJailbreakStillRequiresValidationAndPackageManager() {
        let artifact = AppArtifact(filename: "tweak.deb")
        let plan = ArtifactInstallPlanner().plan(for: artifact, deviceIsJailbroken: true)
        XCTAssertEqual(plan.status, .requiresJailbrokenDeviceAndPackageManager)
        XCTAssertTrue(plan.prerequisites.contains { $0.localizedCaseInsensitiveContains("maintainer scripts") })
    }

    func testUnsupportedAndPathTraversalNamesAreNotAccepted() {
        XCTAssertEqual(AppArtifact(filename: "notes.txt").kind, .unsupported)
        XCTAssertEqual(AppArtifact(filename: "../payload.deb").inspectionStatus, .invalidFilename)
    }

    func testExtensionMatchingIsCaseInsensitive() {
        XCTAssertEqual(AppArtifact(filename: "APP.IPA").kind, .ipa)
        XCTAssertEqual(AppArtifact(filename: "TWEAK.DEB").kind, .deb)
    }
}
