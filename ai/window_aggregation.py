import pandas as pd

WINDOW_SIZE = "5s"  # 5-second windows

df = pd.read_csv("ids_dataset_day3.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

# Set time index
df = df.set_index("timestamp")

# Aggregate per IP per window
agg = df.groupby("ip").resample(WINDOW_SIZE).agg({
    "auth_fail": "sum",
    "rapid_request": "sum",
    "large_payload": "sum",
    "xss_pattern": "sum",
    "is_get": "sum",
    "responseTimeMs": "mean",
    "label": lambda x: x.value_counts().idxmax() if len(x) > 0 else "normal"
})


agg = agg.reset_index()

print("Window samples:", len(agg))
print(agg["label"].value_counts())

agg.to_csv("ids_dataset_day5.csv", index=False)
print("Saved ids_dataset_day5.csv")
