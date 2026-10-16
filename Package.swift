// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "PhoneBridge",
    platforms: [
        .iOS(.v17),
        .macOS(.v14)
    ],
    products: [
        .library(name: "PhoneBridgeCore", targets: ["PhoneBridgeCore"])
    ],
    targets: [
        .target(name: "PhoneBridgeCore"),
        .testTarget(name: "PhoneBridgeCoreTests", dependencies: ["PhoneBridgeCore"])
    ]
)
