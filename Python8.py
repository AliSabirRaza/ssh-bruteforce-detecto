# CONCEPT 8: deciding whether a login was a compromise
#
# Rule: an IP is a potential compromise if it was FLAGGED (checked separately)
# AND it logged in successfully AFTER its last failed attempt.
#
# Expected output:
#   last failure: 2026-10-31 11:02:00
#   success: 2026-10-31 11:12:00
#   compromise: YES
#   compromise: NO   (second case: the success came before the failures)

from datetime import datetime

failures = [
    datetime(2026, 10, 31, 11, 0, 0),
    datetime(2026, 10, 31, 11, 1, 30),
    datetime(2026, 10, 31, 11, 2, 0),
]
success = datetime(2026, 10, 31, 11, 12, 0)

last_failure = max(failures)                  # the most recent failure
print("last failure:", last_failure)
print("success:", success)
print("compromise:", "YES" if success > last_failure else "NO")

# second case: a success BEFORE the failures is not a compromise
early_success = datetime(2026, 10, 31, 10, 55, 0)
print("compromise:", "YES" if early_success > last_failure else "NO")
