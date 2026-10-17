import plistlib
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from verify_target_firmware import verify_ipsw


def make_fixture(path: Path, *, model="iPhone17,3", board="D47AP",
                 version="27.0.1", build="24A446"):
    manifest = {
        "ProductType": model,
        "ProductVersion": version,
        "ProductBuildVersion": build,
        "BuildIdentities": [
            {"Info": {"DeviceClass": board}},
            {"Info": {"DeviceClass": "OTHER_BOARD"}},
        ],
    }
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("BuildManifest.plist", plistlib.dumps(manifest))


class TargetFirmwareVerifierTests(unittest.TestCase):
    def test_matching_target_passes_but_authenticity_is_not_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.ipsw"
            make_fixture(path)
            report = verify_ipsw(path)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["checks"]["target_identity"], "PASS")
            self.assertEqual(report["checks"]["apple_authenticity"], "NOT_VALIDATED")
            self.assertEqual(len(report["input"]["sha256"]), 64)

    def test_wrong_model_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.ipsw"
            make_fixture(path, model="iPhone19,2")
            report = verify_ipsw(path)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["checks"]["product_type"], "FAIL")

    def test_wrong_build_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.ipsw"
            make_fixture(path, build="24A437")
            report = verify_ipsw(path)
            self.assertEqual(report["checks"]["product_build_version"], "FAIL")
            self.assertEqual(report["status"], "FAIL")

    def test_missing_manifest_is_not_validated_and_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.ipsw"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("payload.bin", b"fixture")
            report = verify_ipsw(path)
            self.assertEqual(report["checks"]["build_manifest_unique"], "FAIL")
            self.assertEqual(report["checks"]["target_identity"], "NOT_VALIDATED")
            self.assertEqual(report["checks"]["apple_authenticity"], "NOT_VALIDATED")
            self.assertEqual(report["status"], "FAIL")

    def test_duplicate_manifests_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.ipsw"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("BuildManifest.plist", plistlib.dumps({"ProductType": "iPhone17,3"}))
                archive.writestr("nested/BuildManifest.plist", plistlib.dumps({"ProductType": "iPhone17,3"}))
            report = verify_ipsw(path)
            self.assertEqual(report["checks"]["build_manifest_unique"], "FAIL")
            self.assertEqual(report["observed"]["manifest_matches"], 2)
            self.assertEqual(report["checks"]["target_identity"], "NOT_VALIDATED")
            self.assertEqual(report["status"], "FAIL")

    def test_malformed_manifest_raises_clear_parse_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixture.ipsw"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("BuildManifest.plist", b"not a plist")
            with self.assertRaises((plistlib.InvalidFileException, ValueError)):
                verify_ipsw(path)


if __name__ == "__main__":
    unittest.main()
