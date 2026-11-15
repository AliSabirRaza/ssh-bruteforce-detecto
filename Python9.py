# CONCEPT 9: pandas - a table (DataFrame) and groupby
#
# Install once:  py -m pip install pandas
#
# Expected output: a table with one row per record, then each IP with its
# number of failed rows (192.168.1.5 has 2).

import pandas as pd  # type: ignore[reportMissingModuleSource]

records = [
    {"ip": "192.168.1.5", "result": "Failed"},
    {"ip": "10.0.0.7", "result": "Accepted"},
    {"ip": "192.168.1.5", "result": "Failed"},
]

df = pd.DataFrame(records)              # list of dicts -> table, one row per dict
print(df)

failures = df[df["result"] == "Failed"] # keep only the rows that match
print(failures.groupby("ip").size())    # count the rows for each IP
