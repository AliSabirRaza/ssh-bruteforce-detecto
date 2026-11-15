# FINAL PROGRAM: detect brute-force SSH logins and possible compromises
#
# Install once:  py -m pip install pandas matplotlib
#
# Run it like this:
#   py Python12.py generated.log
#   py Python12.py generated.log --threshold 3 --window 10
#   py Python12.py sample.log
#
# Creates:
#   results.csv      - one row per IP (overwritten each run)
#   burst_chart.png  - bar chart of each IP's largest burst

import argparse
import re
from datetime import datetime, timedelta

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser(description="Detect brute-force SSH logins")
parser.add_argument("logfile")
parser.add_argument("--threshold", type=int, default=5)
parser.add_argument("--window", type=int, default=10)
args = parser.parse_args()

# matches "Failed password for ... from <ip>" and "Accepted password for ... from <ip>"
LINE_PATTERN = re.compile(
    r"(Failed|Accepted) password for (?:invalid user )?(\w+) from (\d+\.\d+\.\d+\.\d+)"
)


def parse_log(path):
    """Read the log and return a table with one row per login result."""
    records = []
    with open(path) as f:
        for line in f:
            match = LINE_PATTERN.search(line)
            if not match:
                continue                      # skip lines that are not login results
            timestamp = datetime.strptime("2026 " + line[:15], "%Y %b %d %H:%M:%S")
            records.append({
                "timestamp": timestamp,
                "result": match.group(1),
                "user": match.group(2),
                "ip": match.group(3),
            })
    return pd.DataFrame(records, columns=["timestamp", "result", "user", "ip"])


def max_in_window(times, window_minutes):
    """Largest number of failure times that fit inside any span of window_minutes."""
    times = sorted(times)
    limit = timedelta(minutes=window_minutes)
    best = 0
    start = 0
    for end in range(len(times)):
        while times[end] - times[start] > limit:
            start += 1
        best = max(best, end - start + 1)
    return best


def analyze(df, threshold, window):
    """Return one row per IP: failures, burst, status, and compromise flag."""
    failures = df[df["result"] == "Failed"]
    successes = df[df["result"] == "Accepted"]

    rows = []
    for ip, group in failures.groupby("ip"):
        times = group["timestamp"].tolist()
        burst = max_in_window(times, window)
        flagged = burst >= threshold
        last_failure = max(times)

        # a success for this IP after its last failure = possible compromise
        later_success = successes[(successes["ip"] == ip) &
                                  (successes["timestamp"] > last_failure)]

        rows.append({
            "ip": ip,
            "total_failures": len(times),
            "burst": burst,
            "status": "FLAGGED" if flagged else "OK",
            "compromise": "YES" if flagged and not later_success.empty else "NO",
        })

    return pd.DataFrame(rows, columns=["ip", "total_failures", "burst", "status", "compromise"])


def make_chart(report, threshold, window):
    colors = ["red" if s == "FLAGGED" else "gray" for s in report["status"]]
    plt.figure(figsize=(8, 4))
    plt.bar(report["ip"], report["burst"], color=colors)
    plt.axhline(threshold, color="black", linestyle="--", label=f"threshold = {threshold}")
    plt.title("Largest failure burst per IP")
    plt.ylabel(f"failures within {window} min")
    plt.xticks(rotation=30, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig("burst_chart.png")
    plt.close()
    print("chart saved to burst_chart.png")


# ---- main ----
df = parse_log(args.logfile)
report = analyze(df, args.threshold, args.window)
report.to_csv("results.csv", index=False)

print("file:", args.logfile)
print("threshold:", args.threshold)
print("window:", args.window)
print()

if report.empty:
    print("No failed logins found.")
else:
    print(report.to_string(index=False))
    make_chart(report, args.threshold, args.window)
