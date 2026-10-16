import Foundation
import XCTest
@testable import PhoneBridgeCore

final class DiagnosticReportTests: XCTestCase {
    func testAllStatusesHaveStableWireValues() {
        XCTAssertEqual(DiagnosticStatus.pass.rawValue, "PASS")
        XCTAssertEqual(DiagnosticStatus.fail.rawValue, "FAIL")
        XCTAssertEqual(DiagnosticStatus.partial.rawValue, "PARTIAL")
        XCTAssertEqual(DiagnosticStatus.blocked.rawValue, "BLOCKED")
        XCTAssertEqual(DiagnosticStatus.notValidated.rawValue, "NOT_VALIDATED")
    }

    func testReportRoundTripsThroughJSON() throws {
        let date = Date(timeIntervalSince1970: 1_750_000_000)
        let check = DiagnosticCheck(
            id: "app.runtime",
            title: "Runtime",
            status: .pass,
            summary: "Core diagnostic model initialized.",
            evidenceSource: "PhoneBridgeCore unit test",
            checkedAt: date
        )
        let report = DiagnosticReport(
            generatedAt: date,
            productVersion: "0.1.0",
            checks: [check]
        )

        let data = try report.encodedJSON()
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        let decoded = try decoder.decode(DiagnosticReport.self, from: data)

        XCTAssertEqual(decoded, report)
    }

    func testLimitationsCanBeRepresented() {
        let check = DiagnosticCheck(
            id: "device.usb",
            title: "USB device connection",
            status: .blocked,
            summary: "No connected-device evidence is available.",
            evidenceSource: "No device session",
            limitation: "Requires a supported desktop companion and a real iPhone."
        )

        XCTAssertEqual(check.status, .blocked)
        XCTAssertNotNil(check.limitation)
    }
}
