import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "phonebridge_device_probe.py"
SPEC = importlib.util.spec_from_file_location("phonebridge_device_probe", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class DeviceProbeReportTests(unittest.TestCase):
    def test_exact_target_is_pass_but_limited_to_observed_metadata(self):
        report = MODULE.build_report({
            "ProductType": "iPhone17,3",
            "ProductVersion": "27.0.1",
            "BuildVersion": "24A446",
            "UniqueDeviceID": "MUST_NOT_LEAK",
            "SerialNumber": "MUST_NOT_LEAK",
        }, connected=True)
        self.assertEqual(report["status"], "PASS")
        self.assertTrue(report["target_match"])
        self.assertNotIn("UniqueDeviceID", report["observed"])
        self.assertNotIn("SerialNumber", report["observed"])
        self.assertIn("does not provide kernel memory", " ".join(report["limitations"]))

    def test_other_build_is_partial_not_pass(self):
        report = MODULE.build_report({
            "ProductType": "iPhone17,3",
            "ProductVersion": "27.0.1",
            "BuildVersion": "OTHER",
        }, connected=True)
        self.assertEqual(report["status"], "PARTIAL")
        self.assertFalse(report["target_match"])

    def test_no_device_is_blocked(self):
        report = MODULE.build_report({}, connected=False, error="not connected")
        self.assertEqual(report["status"], "BLOCKED")
        self.assertIsNone(report["target_match"])
        self.assertEqual(report["evidence_type"], "no_device_observation")


if __name__ == "__main__":
    unittest.main()
