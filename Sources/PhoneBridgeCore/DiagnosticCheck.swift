import Foundation

public enum DiagnosticStatus: String, Codable, CaseIterable, Sendable {
    case pass = "PASS"
    case fail = "FAIL"
    case partial = "PARTIAL"
    case blocked = "BLOCKED"
    case notValidated = "NOT_VALIDATED"
}

public struct DiagnosticCheck: Codable, Equatable, Sendable, Identifiable {
    public let id: String
    public let title: String
    public let status: DiagnosticStatus
    public let summary: String
    public let evidenceSource: String
    public let checkedAt: Date
    public let limitation: String?

    public init(
        id: String,
        title: String,
        status: DiagnosticStatus,
        summary: String,
        evidenceSource: String,
        checkedAt: Date = Date(),
        limitation: String? = nil
    ) {
        self.id = id
        self.title = title
        self.status = status
        self.summary = summary
        self.evidenceSource = evidenceSource
        self.checkedAt = checkedAt
        self.limitation = limitation
    }
}
