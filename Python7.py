# FINAL PROGRAM: detect IPs with bursts of failed SSH logins
#
# Run it like this:
#   py Python7.py sample.log
#   py Python7.py sample.log --threshold 3
#   py Python7.py sample.log --threshold 3 --window 10
#
# Output: prints one line per IP and writes results.csv (overwritten each run).

import argparse
import re
import csv
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(description="Detect failed SSH logins")
parser.add_argument("logfile")
parser.add_argument("--threshold", type=int, default=5)
parser.add_argument("--window", type=int, default=10)
args = parser.parse_args()


def max_in_window(times, window_minutes):
    times = sorted(times)
    limit = timedelta(minutes=window_minutes)
    best = 0
    start = 0
    for end in range(len(times)):
        while times[end] - times[start] > limit:
            start += 1
        best = max(best, end - start + 1)
    return best


print("file:", args.logfile)
print("threshold:", args.threshold)
print("window:", args.window)
print()

times_by_ip = {}

with open(args.logfile) as f:
    for line in f:
        if "Failed" not in line:
            continue

        timestamp = datetime.strptime("2026 " + line[:15], "%Y %b %d %H:%M:%S")
        ip_match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)

        if ip_match:
            ip = ip_match.group(1)
            times_by_ip.setdefault(ip, []).append(timestamp)

with open("results.csv", "w", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["ip", "burst", "status"])
    for ip, times in times_by_ip.items():
        burst = max_in_window(times, args.window)
        status = "FLAGGED" if burst >= args.threshold else "OK"
        writer.writerow([ip, burst, status])
        print(ip, status + ":", burst)
