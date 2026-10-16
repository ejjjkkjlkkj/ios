# iPhone 16 iOS 27.0.1 IPSW validation plan

Date: 2026-10-17

## Scope

Target tuple (all fields must match before any device-specific conclusion):

- Product: iPhone 16
- Product identifier: `iPhone17,3`
- Board: `D47AP`
- Platform / CPID family: `t8140` / `0x8140`
- Firmware: iOS 27.0.1
- Build: `24A446`
- Expected archive name from catalog: `iPhone17,3_27.0.1_24A446_Restore.ipsw`

The firmware catalog lists this build as signed and approximately 12 GiB. This is third-party metadata, not local artifact verification and not a guarantee that signing remains available when a restore is attempted.

## Evidence gates

1. **Acquisition** — obtain the exact IPSW from Apple's CDN or a source that resolves to Apple's CDN. Record final URL, UTC time, byte count, and HTTP result. Do not treat a partial download as an artifact.
2. **Archive integrity** — confirm ZIP/IPS​W central directory and test archive readability. Record exact byte count and SHA-256. A successful hash proves identity for that file, not Apple's authenticity by itself.
3. **Manifest identity** — parse `BuildManifest.plist` without executing payloads. Confirm ProductVersion `27.0.1`, ProductBuildVersion `24A446`, and a build identity matching `iPhone17,3` / `D47AP` / `t8140`. If fields are missing or contradictory, stop and mark **FAIL** or **PARTIAL**, never infer compatibility from the filename.
4. **Inventory** — enumerate kernelcache, device tree, iBoot/iBSS/iBEC, restore ramdisk, and relevant trust-cache artifacts by archive path, size, and SHA-256. Do not patch or repack them during initial inventory.
5. **Static review** — identify format and architecture using read-only tooling; retain tool versions, commands, stdout/stderr, and hashes. Findings must cite the exact file hash and offset/symbol where applicable.
6. **Exploit evidence** — distinguish a public source/reproducer from a conference demo or a claim. Require the exact target device identifier and build in compatibility evidence. Shared iOS build numbers across different products do not prove portability.
7. **Device validation** — only with explicit owner consent and a separately approved test plan. Back up first; do not restore, enter DFU, alter passcode, or install a payload as part of a read-only firmware audit. Physical root SSH and reboot persistence require direct evidence from the exact target device.

## Windows read-only checks

Run from PowerShell in a dedicated work directory. Replace the path with the actual completed download.

```powershell
$ipsw = 'D:\Firmware\iPhone17,3_27.0.1_24A446_Restore.ipsw'
if (-not (Test-Path -LiteralPath $ipsw -PathType Leaf)) {
    Write-Output 'BLOCKED: IPSW file not found'
} else {
    $item = Get-Item -LiteralPath $ipsw
    [pscustomobject]@{
        Path = $item.FullName
        Bytes = $item.Length
        SHA256 = (Get-FileHash -LiteralPath $ipsw -Algorithm SHA256).Hash
    } | Format-List
    & tar.exe -tf $ipsw
    $archiveExit = $LASTEXITCODE
    if ($archiveExit -eq 0) {
        Write-Output 'ARCHIVE_LISTING=PASS'
    } else {
        Write-Output "ARCHIVE_LISTING=FAIL (exit $archiveExit)"
    }
}
```

This is only a first-pass file/hash/listing check. It does not validate the manifest identity, Apple signature, exploitability, or physical-device compatibility. Do not extract or execute binaries during this gate.

## Result labels

- **PASS** — only for the specific gate that was actually run and whose output was retained.
- **FAIL** — contradictory metadata, archive failure, or failed assertion.
- **PARTIAL** — some evidence obtained but one or more required fields/artifacts are missing.
- **BLOCKED** — required artifact/tool/access is unavailable.
- **NOT_VALIDATED** — no qualifying test has been performed.

## Current status at authoring time

- Exact target tuple: catalog metadata cross-checked, not locally verified.
- IPSW downloaded: **NOT DONE**.
- SHA-256 of target IPSW: **NOT DONE**.
- Manifest identity: **NOT DONE**.
- Component inventory: **NOT DONE**.
- iPhone 16 jailbreak/root SSH/reboot persistence: **NOT VALIDATED**.
- Public Calif tool for this exact target: **NOT FOUND** in reviewed public sources.
- Liter8 does not establish iPhone 16 compatibility; its README claims validated support for iPhone 11 `n104ap` only.

## Sources reviewed

- Calif announcement: https://blog.calif.io/p/iphone
- Independent coverage of the iPhone 18 Pro demo: https://decrypt.co/381177/hackers-jailbreak-iphone-18-pro-survives-reboot
- Liter8 upstream and its explicit device/build table: https://github.com/Xplo8E/Liter8
- iPhone 16 (`iPhone17,3`) IPSW catalog: https://ipsw.me/iPhone17%2C3/
- iOS 27.0.1 IPSW catalog: https://ipsw.me/iOS/27.0.1/

These sources are navigation and secondary metadata; the primary IPSW bytes and their parsed manifest must be retained before marking firmware analysis complete.
