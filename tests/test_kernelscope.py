import importlib.util
import plistlib
import tempfile
import unittest
import zipfile
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "tools" / "kernelscope.py"
SPEC = importlib.util.spec_from_file_location("kernelscope", MODULE_PATH)
kernelscope = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kernelscope)


class KernelScopeTests(unittest.TestCase):
    def test_archive_path_safety(self):
        self.assertTrue(kernelscope.safe_archive_path("Firmware/kernelcache"))
        self.assertFalse(kernelscope.safe_archive_path("../outside"))
        self.assertFalse(kernelscope.safe_archive_path("/absolute/path"))

    def test_build_metadata(self):
        raw = plistlib.dumps({
            "ProductVersion": "27.0.1",
            "ProductBuildVersion": "24A446",
            "BuildIdentities": [{"Info": {"DeviceClass": "iPhone17,3"}}],
        })
        metadata = kernelscope.build_metadata({"BuildManifest.plist": raw})
        self.assertEqual(metadata["product_version"], "27.0.1")
        self.assertEqual(metadata["product_build_version"], "24A446")
        self.assertEqual(metadata["device_classes"], ["iPhone17,3"])

    def test_inspect_synthetic_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "synthetic.ipsw"
            manifest = plistlib.dumps({
                "ProductVersion": "27.0.1",
                "ProductBuildVersion": "24A446",
                "BuildIdentities": [{"Info": {"DeviceClass": "iPhone17,3"}}],
            })
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("BuildManifest.plist", manifest)
                archive.writestr("kernelcache.test", b"not a real kernel")
            report = kernelscope.inspect_archive(archive_path, "iPhone17,3", "27.0.1")
            self.assertEqual(report["checks"]["zip_open"], "PASS")
            self.assertEqual(report["checks"]["build_manifest"], "PASS")
            self.assertEqual(report["checks"]["kernel_candidates"], "PASS")
            self.assertEqual(report["checks"]["target_compatibility"], "NOT_VALIDATED")


if __name__ == "__main__":
    unittest.main()
