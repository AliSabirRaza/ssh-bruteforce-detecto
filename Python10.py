# CONCEPT 10: matplotlib - a bar chart saved as a PNG
#
# Install once:  py -m pip install matplotlib
#
# Creates demo_chart.png in the current folder. Open it to see the result.

import matplotlib
matplotlib.use("Agg")               # draw straight to a file, no window needed
import matplotlib.pyplot as plt

ips = ["10.0.0.7", "192.168.1.5"]
bursts = [1, 3]

plt.bar(ips, bursts, color=["gray", "red"])                          # one bar per IP
plt.axhline(3, color="black", linestyle="--", label="threshold = 3") # the threshold line
plt.title("Largest burst per IP")
plt.ylabel("failures in window")
plt.legend()
plt.tight_layout()
plt.savefig("demo_chart.png")
print("saved demo_chart.png")
