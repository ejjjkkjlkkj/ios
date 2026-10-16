import hashlib
import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "tools" / "retrieve_kernelcache.py"
SPEC = importlib.util.spec_from_file_location("retrieve_kernelcache", MODULE_PATH)
retriever = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(retriever)

class KernelRetrieverTests(unittest.TestCase):
    def test_exact_target_constants(self):
        self.assertEqual(retriever.MODEL, "iPhone17,3")
        self.assertEqual(retriever.VERSION, "27.0.1")
        self.assertEqual(retriever.BUILD, "24A446")

    def test_safe_member_rejects_traversal_and_windows_drive(self):
        self.assertTrue(retriever.safe_member("Firmware/kernelcache"))
        self.assertFalse(retriever.safe_member("../outside"))
        self.assertFalse(retriever.safe_member("/absolute/path"))
        self.assertFalse(retriever.safe_member(r"C:\outside\kernelcache"))

    def test_extract_kernelcache_from_synthetic_archive(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive_path = root / "synthetic.ipsw"
            payload = b"synthetic not a real kernel"
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("kernelcache.t8140", payload)
                archive.writestr("../kernelcache.bad", b"must not extract")
            result = retriever.extract_kernelcache(archive_path, root / "out")
            extracted = Path(result["kernelcache_file"])
            self.assertEqual(extracted.read_bytes(), payload)
            self.assertEqual(result["sha256"], hashlib.sha256(payload).hexdigest())
            self.assertEqual(result["physical_device_compatibility"], "NOT_VALIDATED")

if __name__ == "__main__":
    unittest.main()
