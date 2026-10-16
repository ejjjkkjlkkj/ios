import os
import plistlib
import tempfile
import unittest
import zipfile

from firmware_audit import audit_ipsw, _safe_member_name


class FirmwareAuditTests(unittest.TestCase):
    def make_ipsw(self, manifest, extras=None):
        temporary = tempfile.NamedTemporaryFile(suffix=".ipsw", delete=False)
        temporary.close()
        with zipfile.ZipFile(temporary.name, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("BuildManifest.plist", plistlib.dumps(manifest))
            for name, data in (extras or {}).items():
                archive.writestr(name, data)
        self.addCleanup(lambda: os.path.exists(temporary.name) and os.unlink(temporary.name))
        return temporary.name

    def test_inventories_and_hashes_kernelcache(self):
        manifest = {
            "ProductVersion": "27.0.1",
            "ProductBuildVersion": "TEST123",
            "SupportedProductTypes": ["iPhone17,3"],
            "BuildIdentities": [{
                "Info": {"Variant": "Customer Erase Install", "DeviceClass": "D73"},
                "Manifest": {"KernelCache": {"Path": "kernelcache.release.iphone"}},
            }],
        }
        path = self.make_ipsw(manifest, {"kernelcache.release.iphone": b"kernel-fixture"})
        report = audit_ipsw(path)
        self.assertEqual(report["status"], "INVENTORIED")
        self.assertEqual(report["product_version"], "27.0.1")
        self.assertEqual(report["build_identities"][0]["kernelcache_status"], "FOUND_HASHED")
        self.assertEqual(len(report["build_identities"][0]["kernelcache_sha256"]), 64)
        self.assertEqual(report["archive_integrity"], "PASS")

    def test_missing_manifest_is_partial(self):
        temporary = tempfile.NamedTemporaryFile(suffix=".ipsw", delete=False)
        temporary.close()
        self.addCleanup(lambda: os.path.exists(temporary.name) and os.unlink(temporary.name))
        with zipfile.ZipFile(temporary.name, "w") as archive:
            archive.writestr("other.txt", "fixture")
        report = audit_ipsw(temporary.name)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertIn("BuildManifest.plist is missing.", report["errors"])

    def test_missing_kernelcache_is_reported_not_fabricated(self):
        manifest = {"BuildIdentities": [{
            "Info": {"DeviceClass": "D73"},
            "Manifest": {"KernelCache": {"Path": "absent.kernel"}},
        }]}
        report = audit_ipsw(self.make_ipsw(manifest))
        self.assertEqual(report["build_identities"][0]["kernelcache_status"], "NOT_IN_ARCHIVE")

    def test_path_traversal_rejected(self):
        self.assertFalse(_safe_member_name("../kernelcache"))
        self.assertFalse(_safe_member_name("/absolute/path"))
        self.assertFalse(_safe_member_name("folder\\kernelcache"))
        self.assertTrue(_safe_member_name("Firmware/kernelcache"))

    def test_corrupt_input_fails_cleanly(self):
        temporary = tempfile.NamedTemporaryFile(suffix=".ipsw", delete=False)
        temporary.write(b"not a zip")
        temporary.close()
        self.addCleanup(lambda: os.path.exists(temporary.name) and os.unlink(temporary.name))
        report = audit_ipsw(temporary.name)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(report["errors"])


if __name__ == "__main__":
    unittest.main()
