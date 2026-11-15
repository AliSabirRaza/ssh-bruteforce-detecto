# CONCEPT 1: reading a file line by line, then strip() and split()
#
# Expected output with sample.log:
#   Month: Oct, Last word: ssh2   (one line per log line)

with open("sample.log") as f:
    for line in f:
        clean = line.strip()          # remove the newline at the end
        words = clean.split()         # split on spaces into a list
        print(f"Month: {words[0]}, Last word: {words[-1]}")
