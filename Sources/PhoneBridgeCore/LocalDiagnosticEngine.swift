import Foundation

public struct LocalDiagnosticEngine: Sendable {
    public init() {}

    public func run(productVersion: String, capabilities: [DeviceCapability] = .baseline,
                    now: Date = Date()) -> DiagnosticReport {
        let checks = capabilities.map { capability in
            let status: DiagnosticStatus
            switch capability.availability {
            case .available:
                status = .partial
            case .unavailable:
                status = .fail
            case .requiresDesktopCompanion, .requiresUserConsent, .restrictedByPlatform:
                status = .blocked
            case .notValidated:
                status = .notValidated
            }
            return DiagnosticCheck(
                id: capability.id,
                title: capability.title,
                status: status,
                summary: capability.explanation,
                evidenceSource: capability.evidenceSource,
                checkedAt: now,
                limitation: "État de capacité théorique : ce résultat ne prouve pas un test sur iPhone physique."
            )
        }
        return DiagnosticReport(generatedAt: now, productVersion: productVersion, checks: checks)
    }
}
