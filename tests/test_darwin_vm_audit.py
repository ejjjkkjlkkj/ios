import tempfile
import unittest
from pathlib import Path

from darwin_vm_audit import audit_tree


class DarwinVmAuditTests(unittest.TestCase):
    def test_missing_checkout_paths_are_partial(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "iPhone 16 iPhone17,3 iOS 27.0 beta 7", encoding="utf-8"
            )
            report = audit_tree(root)
            self.assertEqual(report["status"], "PARTIAL")
            self.assertEqual(report["checks"]["exact_build_24A446_boot_verified"], "NOT_VALIDATED")
            self.assertIn("run.sh", report["missing_required_paths"])

    def test_exact_build_text_does_not_claim_physical_jailbreak(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "iPhone17,3 iOS 27.0.1 build 24A446; requires a Mac", encoding="utf-8"
            )
            for name in ("get_files.sh", "run.sh", "build_tc.py", "dt_fixup.py"):
                (root / name).write_text("# static fixture\n", encoding="utf-8")
            (root / "qemu-sptm").mkdir()
            (root / "qemu-sptm" / "README").write_text("fixture", encoding="utf-8")
            report = audit_tree(root)
            self.assertEqual(report["checks"]["physical_iphone_validation"], "NOT_VALIDATED")
            self.assertEqual(report["checks"]["jailbreak_compatibility"], "NOT_VALIDATED")
            self.assertEqual(report["checks"]["exact_build_24A446_mentioned_in_text"], "PASS")
            self.assertEqual(report["checks"]["exact_build_24A446_boot_verified"], "NOT_VALIDATED")
            self.assertEqual(report["status"], "PARTIAL")


if __name__ == "__main__":
    unittest.main()
