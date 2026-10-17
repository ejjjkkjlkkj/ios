"""Unit tests for tools/ipsw_static_inventory.py (stdlib unittest only)."""
import importlib.util
import plistlib
import tempfile
import unittest
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "tools" / "ipsw_static_inventory.py"
SPEC = importlib.util.spec_from_file_location("ipsw_static_inventory", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class IpswStaticInventoryTests(unittest.TestCase):
    def test_inventory_reports_hash_and_interesting_members(self):
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "sample.ipsw"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("BuildManifest.plist", plistlib.dumps({
                    "ProductVersion": "27.0.1",
                    "ProductBuildVersion": "24A446",
                    "SupportedProductTypes": ["iPhone17,3"],
                    "BuildIdentities": [{
                        "Info": {
                            "DeviceClass": "D47AP",
                            "BoardConfig": "d47ap",
                            "Variant": "Customer Erase Install (IPSW)",
                            "RestoreBehavior": "Erase",
                        },
                        "Manifest": {
                            "KernelCache": {"Info": {"Path": "kernelcache.release"}},
                            "DeviceTree": {"Info": {"Path": "Firmware/all_flash/DeviceTree.d47ap.im4p"}},
                            "StaticTrustCache": {"Info": {"Path": "Firmware/TrustCache/StaticTrustCache"}},
                        },
                    }],
                }))
                archive.writestr("kernelcache.release", b"not executable")
                archive.writestr("System/Library/dyld/dyld_shared_cache_arm64e", b"cache")

            report = MODULE.inspect_ipsw(archive_path)
            self.assertEqual(report["archive"]["zip_integrity_test"], "PASS")
            self.assertEqual(report["archive"]["entry_count"], 3)
            self.assertEqual(len(report["input"]["sha256"]), 64)
            manifest = report["build_manifest"]
            self.assertEqual(manifest["status"], "PARSED")
            self.assertEqual(manifest["product_build_version"], "24A446")
            self.assertEqual(manifest["supported_product_types"], ["iPhone17,3"])
            self.assertEqual(manifest["build_identities"][0]["device_class"], "D47AP")
            self.assertTrue(manifest["build_identities"][0]["has_kernelcache_path"])
            by_name = {entry["path"]: entry for entry in report["entries"]}
            self.assertIn("kernelcache", by_name["kernelcache.release"]["interesting_tags"])
            self.assertIn("dyld", by_name["System/Library/dyld/dyld_shared_cache_arm64e"]["interesting_tags"])

    def test_expected_hash_match_and_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.ipsw"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("test.txt", b"sample")
            digest = MODULE.sha256_file(path)
            self.assertEqual(MODULE.inspect_ipsw(path, digest)["input"]["expected_hash_check"]["status"], "PASS")
            self.assertEqual(MODULE.inspect_ipsw(path, "0" * 64)["input"]["expected_hash_check"]["status"], "FAIL")

    def test_rejects_non_zip_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "not-an-ipsw.ipsw"
            path.write_bytes(b"not a zip archive")
            with self.assertRaises(ValueError):
                MODULE.inspect_ipsw(path)

    def test_rejects_missing_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "missing.ipsw"
            with self.assertRaises(FileNotFoundError):
                MODULE.inspect_ipsw(path)

    def test_rejects_malformed_expected_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.ipsw"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("test.txt", b"sample")
            with self.assertRaises(ValueError):
                MODULE.inspect_ipsw(path, "not-a-sha256")


if __name__ == "__main__":
    unittest.main()
