import pandas as pd
import numpy as np

WINDOW = "10s"

# -----------------------------
# Load request-level dataset
# -----------------------------
df = pd.read_csv("ids_dataset_day3.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, format="mixed")
df = df.sort_values("timestamp")
df = df.set_index("timestamp")

# -----------------------------
# Window label resolver (priority-based)
# -----------------------------
def window_label(labels):
    priority = ["xss", "sql_injection", "brute_force", "recon", "normal"]
    for p in priority:
        if p in labels.values:
            return p
    return "normal"

# -----------------------------
# Aggregate per IP per window
# -----------------------------
agg = (
    df.groupby("ip")
      .resample(WINDOW)
      .agg(
          req_count=("status", "count"),
          auth_fail_count=("auth_fail", "sum"),
          rapid_req_count=("rapid_request", "sum"),
          large_payload_count=("large_payload", "sum"),
          xss_hits=("xss_pattern", "sum"),
          sqli_hits=("sqli_pattern", "sum"),
          get_requests=("is_get", "sum"),
          avg_response_time=("responseTimeMs", "mean"),
          label=("label", window_label)
      )
)

# -----------------------------
# Cleanup
# -----------------------------
agg = agg.fillna(0).reset_index()
agg = agg[agg["req_count"] > 0]

print("Window-level samples:", len(agg))
print("\nWindow label distribution:")
print(agg["label"].value_counts())

# -----------------------------
# Save final ML dataset
# -----------------------------
agg.to_csv("ids_dataset_day5.csv", index=False)
print("\nSaved ids_dataset_day5.csv")
