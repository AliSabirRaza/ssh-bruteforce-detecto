# CONCEPT 5: counting with a dictionary
#
# Expected output:
#   {'192.168.1.5': 2, '10.0.0.7': 1}
#   {'192.168.1.5': [...times...], '10.0.0.7': [...times...]}  (second part)

ips = ["192.168.1.5", "10.0.0.7", "192.168.1.5"]

# Part A: count how many times each IP appears
counts = {}
for ip in ips:
    counts[ip] = counts.get(ip, 0) + 1     # .get returns 0 for a new IP
print(counts)

# Part B: store a LIST of values per IP (we need the times later)
times_by_ip = {}
times = ["10:01:02", "10:01:05", "10:01:09"]
for ip, t in zip(ips, times):
    times_by_ip.setdefault(ip, []).append(t)   # creates the list the first time
print(times_by_ip)

