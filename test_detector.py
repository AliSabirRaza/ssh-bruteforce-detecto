# Automated tests for Python12.py
#
# Put this file in the same folder as Python12.py, then run:
#   py test_detector.py
#
# Each test runs Python12.py as a separate program, then checks results.csv
# and the printed output against the expected values.
# Note: running the tests overwrites results.csv and burst_chart.png.

import csv
import subprocess
import sys
import traceback


def run_tool(*args):
    """Run Python12.py with the given arguments. Returns (exit code, printed text)."""
    result = subprocess.run(
        [sys.executable, "Python12.py", *args],
        capture_output=True, text=True,
    )
    return result.returncode, result.stdout + result.stderr


def read_results():
    """Read results.csv into a dictionary: ip -> row. Values are text."""
    with open("results.csv", newline="") as f:
        return {row["ip"]: row for row in csv.DictReader(f)}


def test_default_threshold():
    code, _ = run_tool("generated.log")
    assert code == 0, "program should exit cleanly"
    rows = read_results()
    assert rows["203.0.113.50"]["status"] == "FLAGGED"
    assert rows["203.0.113.50"]["burst"] == "8"
    assert rows["203.0.113.50"]["compromise"] == "NO"
    assert rows["203.0.113.99"]["status"] == "FLAGGED"
    assert rows["203.0.113.99"]["burst"] == "6"
    assert rows["203.0.113.99"]["compromise"] == "YES"
    assert rows["198.51.100.7"]["total_failures"] == "4"
    assert rows["198.51.100.7"]["status"] == "OK"
    assert rows["10.0.0.7"]["status"] == "OK"


def test_threshold_3():
    run_tool("generated.log", "--threshold", "3")
    rows = read_results()
    assert rows["203.0.113.50"]["status"] == "FLAGGED"
    assert rows["203.0.113.99"]["status"] == "FLAGGED"
    assert rows["198.51.100.7"]["status"] == "OK"
    assert rows["10.0.0.7"]["status"] == "OK"


def test_threshold_above_all_bursts():
    # the largest burst is 8, so a threshold of 9 flags nobody
    run_tool("generated.log", "--threshold", "9")
    rows = read_results()
    assert rows["203.0.113.50"]["status"] == "OK"
    assert rows["203.0.113.99"]["status"] == "OK"
    assert rows["203.0.113.99"]["compromise"] == "NO", "compromise needs a flag first"


def test_window_matters():
    # with a 1-minute window, the 6-failure attacker only bursts to 3
    run_tool("generated.log", "--window", "1", "--threshold", "4")
    rows = read_results()
    assert rows["203.0.113.50"]["burst"] == "4"
    assert rows["203.0.113.50"]["status"] == "FLAGGED"
    assert rows["203.0.113.99"]["burst"] == "3"
    assert rows["203.0.113.99"]["status"] == "OK"
    assert rows["203.0.113.99"]["compromise"] == "NO"


def test_no_failures():
    code, text = run_tool("nofail.log")
    assert code == 0
    assert "No failed logins found." in text
    assert read_results() == {}, "CSV should contain only the header"


def test_missing_file():
    code, text = run_tool("nofile.log")
    assert code != 0, "a missing file should stop the program"
    assert "FileNotFoundError" in text


TESTS = [
    test_default_threshold,
    test_threshold_3,
    test_threshold_above_all_bursts,
    test_window_matters,
    test_no_failures,
    test_missing_file,
]

if __name__ == "__main__":
    # regenerate the test log first, so the tests always start from known data
    subprocess.run([sys.executable, "Python11.py"], check=True, capture_output=True)

    passed = 0
    for test in TESTS:
        try:
            test()
            print("PASS", test.__name__)
            passed += 1
        except AssertionError:
            print("FAIL", test.__name__)
            traceback.print_exc()

    print(f"\n{passed} of {len(TESTS)} tests passed")
