import Foundation

public enum CapabilityAvailability: String, Codable, Sendable {
    case available
    case unavailable
    case requiresDesktopCompanion
    case requiresUserConsent
    case restrictedByPlatform
    case notValidated
}

public struct DeviceCapability: Codable, Equatable, Sendable, Identifiable {
    public let id: String
    public let title: String
    public let availability: CapabilityAvailability
    public let explanation: String
    public let evidenceSource: String

    public init(id: String, title: String, availability: CapabilityAvailability,
                explanation: String, evidenceSource: String) {
        self.id = id
        self.title = title
        self.availability = availability
        self.explanation = explanation
        self.evidenceSource = evidenceSource
    }

    public static let baseline: [DeviceCapability] = [
        .init(id: "ios.public-apis", title: "Informations exposées par iOS",
              availability: .available,
              explanation: "Uniquement les informations accessibles via les API publiques autorisées.",
              evidenceSource: "Inventaire des API publiques à confirmer par implémentation"),
        .init(id: "usb.pairing", title: "Connexion USB et jumelage",
              availability: .requiresDesktopCompanion,
              explanation: "Nécessite un compagnon compatible, un appareil déverrouillé et l'autorisation de confiance.",
              evidenceSource: "Aucune session appareil réelle dans ce package"),
        .init(id: "app.installation", title: "Installation d'applications tierces",
              availability: .restrictedByPlatform,
              explanation: "Dépend d'une méthode de distribution prise en charge, de la signature et des profils applicables.",
              evidenceSource: "Documentation officielle Apple sur la distribution"),
        .init(id: "private.diagnostics", title: "Diagnostics internes non exposés",
              availability: .restrictedByPlatform,
              explanation: "Ne sont pas accessibles à une application ordinaire sans interface système autorisée.",
              evidenceSource: "Limites de la plateforme iOS")
    ]
}
