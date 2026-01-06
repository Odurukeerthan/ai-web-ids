import json
import pandas as pd
import numpy as np

LOG_FILE = "../backend/logs/requests.log"

records = []
with open(LOG_FILE, "r") as f:
    for line in f:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue

df = pd.DataFrame(records)
print("Raw rows:", len(df))

# -----------------------------
# Timestamp handling
# -----------------------------
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, format="mixed")
df = df.sort_values("timestamp")

# -----------------------------
# Base features
# -----------------------------
df["time_delta"] = (
    df.groupby("ip")["timestamp"]
    .diff()
    .dt.total_seconds()
    .fillna(999)
)

df["auth_fail"] = (df["status"] == 401).astype(int)
df["rapid_request"] = (df["time_delta"] < 1.5).astype(int)
df["large_payload"] = (df["payloadSize"] > 45).astype(int)
df["is_get"] = (df["method"] == "GET").astype(int)

# Content patterns
df["xss_pattern"] = df["payloadSnippet"].str.contains(
    r"<script|onerror=|onload=|<svg|<img|javascript:",
    case=False,
    na=False
).astype(int)

df["sqli_pattern"] = df["payloadSnippet"].str.contains(
    r"'|\"|--|/\*|\bor\b|\band\b|\bunion\b|\bselect\b",
    case=False,
    na=False,
    regex=True
).astype(int)

# -----------------------------
# Rolling behavior (KEY FIX)
# -----------------------------
df["fail_rolling"] = (
    df.groupby("ip")["auth_fail"]
    .rolling(window=30, min_periods=3)
    .sum()
    .reset_index(level=0, drop=True)
)

# -----------------------------
# Final IDS labeling logic
# -----------------------------
def label_attack(row):
    # Highest confidence attacks
    if row["xss_pattern"]:
        return "xss"

    if row["sqli_pattern"] and row["auth_fail"]:
        return "sql_injection"

    # Brute force = repeated auth failures in short history
    if row["fail_rolling"] >= 4:
        return "brute_force"

    # Recon
    if row["is_get"] and row["status"] in [403, 404]:
        return "recon"

    return "normal"

df["label"] = df.apply(label_attack, axis=1)

# -----------------------------
# Verification
# -----------------------------
print("\nFinal label distribution:")
print(df["label"].value_counts())

df.to_csv("ids_dataset_day3.csv", index=False)
print("\nSaved ids_dataset_day3.csv")
