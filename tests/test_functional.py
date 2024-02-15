import os
import json
import unittest

from pathlib import Path

SCAN_OUTPUT_PATH = Path("tests") / "scan_output.json"
DETECT_OUTPUT_PATH = Path("tests") / "detect_output.json"
LOGFILE_PATH = Path("logfile.log")


class FunctionalTest(unittest.TestCase):
    def test_help_returns_zero_exit_status(self):
        exit_status = os.system("python src/main.py -h")
        self.assertEqual(exit_status, 0)

    def test_scan_detect_run_in_sequence_correctly(self):
        try:
            os.system("python src/main.py scan . .. -rp tests")
            self.assertTrue(SCAN_OUTPUT_PATH.exists())
            with open(SCAN_OUTPUT_PATH, "r") as f:
                json.load(f)

            os.system("python src/main.py detect tests -rp tests")
            self.assertTrue(DETECT_OUTPUT_PATH.exists())
            with open(DETECT_OUTPUT_PATH, "r") as f:
                json.load(f)
        finally:
            if SCAN_OUTPUT_PATH.exists():
                os.remove(SCAN_OUTPUT_PATH)
            if DETECT_OUTPUT_PATH.exists():
                os.remove(DETECT_OUTPUT_PATH)

    def test_logs_can_be_redirected_to_logfile(self):
        try:
            os.system(
                "python src/main.py scan . .. -rp tests --log-output logfile --log-verbosity debug"
            )
            self.assertTrue(LOGFILE_PATH.exists)

            os.system(
                "python src/main.py detect tests -rp tests --log-output logfile --log-verbosity debug"
            )
            self.assertTrue(LOGFILE_PATH.exists)
        finally:
            if SCAN_OUTPUT_PATH.exists():
                os.remove(SCAN_OUTPUT_PATH)
            if DETECT_OUTPUT_PATH.exists():
                os.remove(DETECT_OUTPUT_PATH)
            if LOGFILE_PATH.exists():
                os.remove(LOGFILE_PATH)


if __name__ == "__main__":
    unittest.main()
