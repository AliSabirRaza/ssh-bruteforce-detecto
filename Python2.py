# CONCEPT 2: regular expressions and capture groups
#
# Expected output:
#   User: root
#   IP: 192.168.1.5

import re

line = "Oct 31 10:01:02 server sshd[1201]: Failed password for root from 192.168.1.5 port 22 ssh2"

user = re.search(r"for (\w+)", line)                       # (\w+) captures the username
ip = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)         # captures the IP address

if user and ip:
    print("User:", user.group(1))   # group(1) = text inside the first ( )
    print("IP:", ip.group(1))
