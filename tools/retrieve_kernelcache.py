#!/usr/bin/env python3
"""Download iPhone 16 iOS 27.0.1 IPSW and extract a kernelcache candidate."""
from __future__ import annotations
import argparse, hashlib, json, shutil, sys, urllib.request, zipfile
from pathlib import Path, PurePosixPath

MODEL = "iPhone17,3"
VERSION = "27.0.1"
BUILD = "24A446"
METADATA_URL = f"https://api.ipsw.me/v4/device/{MODEL}?type=ipsw"
USER_AGENT = "PhoneBridge-KernelRetriever/0.1"

def hash_file(path: Path, algorithm: str = "sha1") -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def fetch_metadata(timeout: int = 30) -> dict:
    request = urllib.request.Request(METADATA_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.load(response)
    if not isinstance(payload, dict) or payload.get("identifier") != MODEL:
        raise ValueError("Metadata response does not match iPhone 16 identifier iPhone17,3")
    firmwares = payload.get("firmwares")
    if not isinstance(firmwares, list):
        raise ValueError("Metadata response has no firmware list")
    matches = [item for item in firmwares if isinstance(item, dict)
               and item.get("version") == VERSION and item.get("buildid") == BUILD
               ]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one {MODEL} {VERSION} ({BUILD}) record; found {len(matches)}")
    item = matches[0]
    url, checksum = item.get("url"), item.get("sha1sum")
    if not isinstance(url, str) or not url.startswith("https://"):
        raise ValueError("Firmware URL is missing or not HTTPS")
    if not isinstance(checksum, str) or len(checksum) != 40:
        raise ValueError("Firmware SHA-1 checksum is missing or malformed")
    return {"device": "iPhone 16", "identifier": MODEL, "version": VERSION, "build": BUILD,
            "signed_status_reported_by_metadata": item.get("signed"),
            "size_bytes": item.get("filesize"), "sha1": checksum.lower(), "url": url}

def download_verified(url: str, expected_sha1: str, destination: Path, timeout: int = 90) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    partial = destination.with_suffix(destination.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response, partial.open("wb") as output:
            if not response.geturl().startswith("https://"):
                raise ValueError("Download redirected away from HTTPS")
            shutil.copyfileobj(response, output, length=1024 * 1024)
        actual = hash_file(partial, "sha1")
        if actual.lower() != expected_sha1.lower():
            raise ValueError(f"SHA-1 mismatch: expected {expected_sha1}, got {actual}")
        partial.replace(destination)
    except Exception:
        partial.unlink(missing_ok=True)
        raise

def safe_member(name: str) -> bool:
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    first = path.parts[0] if path.parts else ""
    return (not path.is_absolute() and ".." not in path.parts
            and not (len(first) >= 2 and first[1] == ":")
            and not normalized.startswith("//"))

def extract_kernelcache(ipsw: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ipsw) as archive:
        candidates = [info for info in archive.infolist()
                      if "kernelcache" in info.filename.lower() and not info.is_dir()
                      and safe_member(info.filename)]
        if not candidates:
            raise ValueError("No safe kernelcache candidate found in IPSW")
        candidates.sort(key=lambda info: (MODEL not in info.filename,
                                         "t8140" not in info.filename.lower(),
                                         "/" in info.filename, -info.file_size))
        selected = candidates[0]
        basename = Path(selected.filename.replace("\\", "/")).name
        if not basename or basename in {".", ".."}:
            raise ValueError("Unsafe kernelcache output name")
        destination = output_dir / basename
        with archive.open(selected, "r") as source, destination.open("wb") as output:
            shutil.copyfileobj(source, output, length=1024 * 1024)
    return {"status": "PASS", "device": "iPhone 16", "model_identifier": MODEL,
            "ios_version": VERSION, "build": BUILD, "archive_member": selected.filename,
            "kernelcache_file": str(destination), "size_bytes": destination.stat().st_size,
            "sha256": hash_file(destination, "sha256"), "decoded": False,
            "physical_device_compatibility": "NOT_VALIDATED",
            "note": "Container extracted only; no firmware execution, restore, exploit, or device modification."}

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Retrieve iPhone 16 iOS 27.0.1 IPSW and extract kernelcache.")
    parser.add_argument("--out", type=Path, default=Path("artifacts/iphone16-ios-27.0.1"))
    parser.add_argument("--metadata-only", action="store_true", help="do not download the approximately 12 GB IPSW")
    parser.add_argument("--keep-ipsw", action="store_true", help="retain the full IPSW after extraction")
    args = parser.parse_args(argv)
    try:
        metadata = fetch_metadata()
        print(json.dumps({k: v for k, v in metadata.items() if k != "url"}, indent=2))
        if args.metadata_only:
            return 0
        args.out.mkdir(parents=True, exist_ok=True)
        ipsw = args.out / f"{MODEL}_{VERSION}_{BUILD}_Restore.ipsw"
        if not ipsw.exists():
            print("Downloading full IPSW (about 12 GB).", file=sys.stderr)
            download_verified(metadata["url"], metadata["sha1"], ipsw)
        elif hash_file(ipsw, "sha1").lower() != metadata["sha1"].lower():
            raise ValueError("Existing IPSW checksum mismatch; refusing to use it")
        result = extract_kernelcache(ipsw, args.out / "kernelcache")
        report = {"firmware_metadata": {k: v for k, v in metadata.items() if k != "url"},
                  "kernelcache": result}
        report_path = args.out / "retrieval-report.json"
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        print(f"Report: {report_path}")
        if not args.keep_ipsw:
            ipsw.unlink(missing_ok=True)
            print("Full IPSW removed after extraction; use --keep-ipsw to retain it.")
        return 0
    except (OSError, ValueError, RuntimeError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
