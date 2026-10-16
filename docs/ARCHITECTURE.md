# Architecture and implementation roadmap

## Product split

### iOS app

SwiftUI interface for guided, on-device checks using public APIs. It can report app-visible facts such as OS version, app version, available storage information where permitted, network reachability, and battery state where exposed by supported APIs. Every diagnostic must state its source and limitations.

### Desktop companion (future)

A separate companion may use supported Apple pairing/developer interfaces or audited open-source tooling to gather permitted diagnostics and assist with app deployment. It must not require iTunes or iCloud as a product dependency. It must disclose any platform, driver, pairing, developer-account, or signing prerequisites before the user starts.

### Signing and distribution

The app must never represent certificate signing, provisioning, developer mode, trust prompts, or regional distribution restrictions as bypassed. Use documented, authorized distribution paths. No credential harvesting, certificate theft, or security-control evasion.

## Evidence contract

Every check returns:
- stable check identifier;
- status: PASS, FAIL, PARTIAL, BLOCKED, or NOT_VALIDATED;
- human-readable summary;
- evidence source;
- timestamp;
- limitation / next action when applicable.

A successful unit test validates code behavior only. It is not proof that an iPhone has been connected or diagnosed.

## Milestones

1. **Foundation** — diagnostic model, deterministic JSON report, tests, CI.
2. **iOS UI** — accessible SwiftUI dashboard and on-device checks.
3. **Device connection** — investigate supported USB/pairing APIs for each target desktop OS; no fabricated support claims.
4. **Diagnostics** — battery/thermal/storage/log data only where the platform exposes it through documented interfaces or user-authorized device reports.
5. **App deployment** — evaluate compliant signing/install methods and clearly expose prerequisites.
6. **Release** — signed builds, SBOM/dependency review, security review, real-device matrix, reproducible release notes.

## Non-goals

- Bypassing Apple's code-signing enforcement.
- Installing arbitrary apps from an ordinary iOS app without a supported signing/distribution mechanism.
- Claiming access to private iOS APIs or hardware data without evidence.
- Uploading device data without informed consent.
