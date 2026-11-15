# CONCEPT 6: the sliding window (largest burst inside a time span)
#
# Question: what is the most failures that fit inside any span of N minutes?
#
# Expected output:
#   window 10 minutes -> 3
#   window 1 minute   -> 2

from datetime import datetime, timedelta


def max_in_window(times, window_minutes):
    times = sorted(times)
    limit = timedelta(minutes=window_minutes)
    best = 0
    start = 0
    for end in range(len(times)):
        # move the left edge forward while the span is too long
        while times[end] - times[start] > limit:
            start += 1
        best = max(best, end - start + 1)   # count inside the window
    return best


failures = [
    datetime(2026, 10, 31, 10, 1, 2),
    datetime(2026, 10, 31, 10, 1, 9),
    datetime(2026, 10, 31, 10, 4, 30),
    datetime(2026, 10, 31, 10, 40, 0),
    datetime(2026, 10, 31, 10, 40, 3),
]

print("window 10 minutes ->", max_in_window(failures, 10))
print("window 1 minute ->", max_in_window(failures, 1))
