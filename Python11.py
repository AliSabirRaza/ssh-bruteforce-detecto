# CONCEPT 11: generating a test log where we already know the answers
#
# Run:  py Python11.py
#
# Creates:
#   generated.log     - the test input, sorted by time like a real log
#   ground_truth.txt  - what the analyzer SHOULD report

LOG_LINES = []
pid = 3000


def login(time_str, result, user, ip):
    global pid
    pid += 1
    LOG_LINES.append(
        f"Oct 31 {time_str} server sshd[{pid}]: {result} password for {user} from {ip} port 22 ssh2\n"
    )


def other(time_str, text):
    LOG_LINES.append(f"Oct 31 {time_str} server {text}\n")


# 1. brute-force attacker: 8 failures in about 2 minutes
for t, user in [("11:00:00", "root"), ("11:00:08", "admin"), ("11:00:15", "test"),
                ("11:00:40", "root"), ("11:01:10", "ubuntu"), ("11:01:30", "root"),
                ("11:02:05", "admin"), ("11:02:20", "root")]:
    login(t, "Failed", user, "203.0.113.50")

# 2. slow scanner: 4 failures spread over hours, never a burst
for t in ["09:00:00", "10:30:00", "12:00:00", "13:30:00"]:
    login(t, "Failed", "root", "198.51.100.7")

# 3. compromise: 6 quick failures, then a successful login
for t, user in [("11:10:00", "root"), ("11:11:00", "root"), ("11:11:30", "admin"),
                ("11:12:00", "root"), ("11:12:20", "test"), ("11:13:00", "root")]:
    login(t, "Failed", user, "203.0.113.99")
login("11:25:00", "Accepted", "root", "203.0.113.99")

# 4. normal user who mistyped once, then logged in
login("08:55:00", "Failed", "alice", "10.0.0.7")
login("08:55:20", "Accepted", "alice", "10.0.0.7")

# 5. noise the analyzer must ignore
other("11:05:00", "systemd[1]: Started Session 4 of user alice.")
other("11:06:00", "sshd[3100]: Disconnected from user alice 10.0.0.7 port 51022")

LOG_LINES.sort(key=lambda line: line[:15])   # sort by timestamp, like a real log

with open("generated.log", "w") as f:
    f.writelines(LOG_LINES)

GROUND_TRUTH = """Expected results, default threshold 5, window 10:
ip,total_failures,burst,status,compromise
10.0.0.7,1,1,OK,NO
198.51.100.7,4,1,OK,NO
203.0.113.50,8,8,FLAGGED,NO
203.0.113.99,6,6,FLAGGED,YES

Expected results with --threshold 3:
203.0.113.50 FLAGGED (burst 8)
203.0.113.99 FLAGGED (burst 6, compromise YES)
10.0.0.7 and 198.51.100.7 OK
"""

with open("ground_truth.txt", "w") as f:
    f.write(GROUND_TRUTH)

print("created generated.log and ground_truth.txt")
