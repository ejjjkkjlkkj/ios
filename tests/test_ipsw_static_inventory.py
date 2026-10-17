"""Unit tests for tools/ipsw_static_inventory.py (stdlib unittest only)."""
import importlib.util
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
                archive.writestr("BuildManifest.plist", b"manifest")
                archive.writestr("kernelcache.release", b"not executable")
                archive.writestr("System/Library/dyld/dyld_shared_cache_arm64e", b"cache")

            report = MODULE.inspect_ipsw(archive_path)
            self.assertEqual(report["archive"]["zip_integrity_test"], "PASS")
            self.assertEqual(report["archive"]["entry_count"], 3)
            self.assertEqual(len(report["input"]["sha256"]), 64)
            by_name = {entry["path"]: entry for entry in report["entries"]}
            self.assertIn("kernelcache", by_name["kernelcache.release"]["interesting_tags"])
            self.assertIn("manifest", by_name["BuildManifest.plist"]["interesting_tags"])
            self.assertIn("dyld", by_name["System/Library/dyld/dyld_shared_cache_arm64e"]["interesting_tags"])

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


if __name__ == "__main__":
    unittest.main()
