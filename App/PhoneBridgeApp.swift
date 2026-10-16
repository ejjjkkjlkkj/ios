#if canImport(SwiftUI)
import SwiftUI
import PhoneBridgeCore

@main
struct PhoneBridgeApp: App {
    var body: some Scene {
        WindowGroup {
            DiagnosticsView()
        }
    }
}

struct DiagnosticsView: View {
    @State private var report = LocalDiagnosticEngine().run(productVersion: "0.1.0")

    var body: some View {
        NavigationStack {
            List {
                Section("État du projet") {
                    Label("Diagnostics locaux", systemImage: "checkmark.shield")
                    Text("Prototype : les capacités USB et d’installation ne sont pas encore validées sur appareil réel.")
                        .font(.body)
                        .fixedSize(horizontal: false, vertical: true)
                }
                Section("Capacités") {
                    ForEach(report.checks) { check in
                        VStack(alignment: .leading, spacing: 6) {
                            Text(check.title).font(.headline)
                            Text(check.status.rawValue).font(.subheadline).bold()
                            Text(check.summary).font(.body)
                            if let limitation = check.limitation {
                                Text(limitation).font(.footnote)
                            }
                        }
                        .accessibilityElement(children: .combine)
                        .padding(.vertical, 4)
                    }
                }
                Section("Rapport") {
                    ShareLink(item: reportText) {
                        Label("Exporter le rapport JSON", systemImage: "square.and.arrow.up")
                    }
                }
            }
            .navigationTitle("PhoneBridge")
            .toolbar {
                Button("Actualiser") {
                    report = LocalDiagnosticEngine().run(productVersion: "0.1.0")
                }
                .accessibilityHint("Régénère le rapport des capacités connues.")
            }
        }
    }

    private var reportText: String {
        guard let data = try? report.encodedJSON(),
              let text = String(data: data, encoding: .utf8) else {
            return "{\"error\":\"Échec de sérialisation\"}"
        }
        return text
    }
}
#endif
