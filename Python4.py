# CONCEPT 4: command-line arguments with argparse
#
# Run it like this:
#   py Python4.py sample.log
#   py Python4.py sample.log --threshold 3 --window 30
#
# Expected output for "py Python4.py sample.log":
#   file: sample.log
#   threshold: 5
#   window: 10

import argparse

parser = argparse.ArgumentParser(description="Demo: command-line arguments")
parser.add_argument("logfile")                            # required, no dashes
parser.add_argument("--threshold", type=int, default=5)   # optional, default 5
parser.add_argument("--window", type=int, default=10)     # optional, default 10
args = parser.parse_args()

print("file:", args.logfile)
print("threshold:", args.threshold)
print("window:", args.window)
