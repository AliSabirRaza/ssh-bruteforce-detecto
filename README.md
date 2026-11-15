# Brute-Force SSH Login Detector

This tool reads a Linux authentication log, counts failed SSH password attempts per IP address within a time window, flags IPs at or above a threshold, and marks IPs that logged in successfully after their failures as possible compromises.

It analyzes sample or owned logs only. It does not block addresses or access live systems.

## Requirements

- Python 3
- pandas and matplotlib

Install the two libraries once:

    py -m pip install pandas matplotlib

## Files

- `Python12.py`: the complete program
- `Python1.py` to `Python11.py`: one concept per file, for learning and the presentation
- `Python7.py`: an earlier version without pandas or compromise detection. Use Python12.py instead.
- `sample.log`: handwritten sample with one burst of failures
- `nofail.log`: successful logins only
- `Python11.py` creates `generated.log` and `ground_truth.txt` for testing

## Usage

    py Python12.py <logfile> [--threshold N] [--window MINUTES]

- `logfile`: the log file to check (required)
- `--threshold`: failures needed in one window to flag an IP (default: 5)
- `--window`: window length in minutes (default: 10)

Steps:

    py Python11.py
    py Python12.py generated.log

## Output

- The terminal prints the settings and a table with one row per IP.
- `results.csv` holds the same table. It is overwritten on each run.
- `burst_chart.png` shows each IP's largest burst against the threshold line.

Columns:

- `total_failures`: all failed logins from the IP
- `burst`: the most failures inside any one window
- `status`: `FLAGGED` if burst is at or above the threshold, otherwise `OK`
- `compromise`: `YES` if the IP was flagged and later logged in successfully after its last failure

## Example

With `generated.log` and the default threshold, `203.0.113.99` is flagged with a compromise, because it logged in after six quick failures. See `ground_truth.txt` for the full expected result.
