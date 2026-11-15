# CONCEPT 3: turning a syslog timestamp into a datetime object
#
# syslog lines have no year, so we add "2026 " in front and parse with %Y.
#
# Expected output:
#   2026-10-31 10:01:02

from datetime import datetime

line = "2026 Oct 31 10:01:02 server sshd[1201]: Failed password for root from 192.168.1.5 port 22 ssh2"

timestamp = datetime.strptime("2026 " + line[:15], "%Y %b %d %H:%M:%S")
print(timestamp)
