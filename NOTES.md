# Technical Notes

## Method

1. Read the log line by line. Keep only lines matching `Failed password` or `Accepted password` and capture the result, user, and IP with one regular expression.
2. Extract the timestamp from the first 15 characters and add the year.
3. Load the results into a pandas DataFrame with one row per login result.
4. For each IP with failures, sort its failure times and slide a window of the given length across them. The largest number of failures inside any one window is the IP's burst.
5. Flag the IP if its burst is at or above the threshold.
6. Mark the IP as a possible compromise if it was flagged and it has a successful login later than its last failure.
7. Write the table to `results.csv` and draw a bar chart with matplotlib, saved as `burst_chart.png`.

## Definitions

- **Burst**: the largest number of failures within any span of `--window` minutes.
- **Flagged**: burst is at or above `--threshold`.
- **Possible compromise**: flagged, and a successful login from the same IP happened after its last failure. This is a rule for review, not proof of an attack.

## Assumptions

- Syslog timestamps have no year, so the year is fixed to 2026.
- Timestamps use the format `Oct 31 10:01:02`, with the first 15 characters being the timestamp.
- Only SSH password lines are analyzed. Key-based logins, other services, and other failure types are ignored.

## Limitations

- Reads one log file per run.
- Does not block IPs or take any action beyond reporting.
- Compromise detection is a simple time rule. A success after failures can also be a legitimate user who mistyped, so results need human review.
- The window check uses a strict limit, so a gap of exactly the window length still fits.
- Overwrites `results.csv` and `burst_chart.png` on every run.
- Stops with an error if the log file doesn't exist.

## Testing

Run `py Python11.py` first to create `generated.log`, whose correct results are in `ground_truth.txt`.

| Input | Command | Expected result |
|------|---------|-----------------|
| `generated.log` | `py Python12.py generated.log` | 203.0.113.50 FLAGGED (8), 203.0.113.99 FLAGGED (6) with compromise YES, 10.0.0.7 and 198.51.100.7 OK |
| `generated.log` | `py Python12.py generated.log --threshold 3` | Same two IPs FLAGGED, the other two OK |
| `sample.log` | `py Python12.py sample.log` | 192.168.1.5: 5 failures, burst 3, OK, compromise NO |
| `sample.log` | `py Python12.py sample.log --threshold 3` | 192.168.1.5 FLAGGED, compromise NO |
| `nofail.log` | `py Python12.py nofail.log` | "No failed logins found." CSV has the header only |
| `nofile.log` (does not exist) | `py Python12.py nofile.log` | `FileNotFoundError: [Errno 2] No such file or directory` |
