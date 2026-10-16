import XCTest
@testable import PhoneBridgeCore

final class LocalDiagnosticEngineTests: XCTestCase {
    func testPlatformRestrictedCapabilitiesAreBlockedNotPassed() {
        let report = LocalDiagnosticEngine().run(productVersion: "test", now: Date(timeIntervalSince1970: 0))
        let install = report.checks.first { $0.id == "app.installation" }
        XCTAssertEqual(install?.status, .blocked)
    }

    func testReportIncludesEvidenceAndLimitations() {
        let report = LocalDiagnosticEngine().run(productVersion: "test")
        XCTAssertFalse(report.checks.isEmpty)
        XCTAssertTrue(report.checks.allSatisfy { !$0.evidenceSource.isEmpty })
        XCTAssertTrue(report.checks.allSatisfy { $0.limitation != nil })
    }

    func testUnknownCapabilityIsNotValidated() {
        let capability = DeviceCapability(
            id: "test.unknown", title: "Unknown", availability: .notValidated,
            explanation: "No proof", evidenceSource: "Test fixture"
        )
        let report = LocalDiagnosticEngine().run(productVersion: "test", capabilities: [capability])
        XCTAssertEqual(report.checks.first?.status, .notValidated)
    }
}
