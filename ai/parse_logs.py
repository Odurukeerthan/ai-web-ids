import json
import pandas as pd

LOG_FILE = "../backend/logs/requests.log"

records = []

# -----------------------------
# 1. Load JSON logs
# -----------------------------
with open(LOG_FILE, "r") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue

df = pd.DataFrame(records)

print("Raw rows:", len(df))
print(df.head())

# -----------------------------
# 2. Timestamp handling
# -----------------------------
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

# -----------------------------
# 3. Feature engineering
# -----------------------------

# Time delta per IP
df["time_delta"] = (
    df.groupby("ip")["timestamp"]
    .diff()
    .dt.total_seconds()
    .fillna(0)
)

# Rapid requests (brute-force signal)
df["rapid_request"] = (df["time_delta"] < 0.1).astype(int)

# Authentication failure
df["auth_fail"] = (df["status"] == 401).astype(int)

# Payload anomaly (SQLi proxy)
df["large_payload"] = (df["payloadSize"] > 45).astype(int)

# HTTP method flag
df["is_get"] = (df["method"] == "GET").astype(int)

# -----------------------------
# 4. XSS detection (content-based)
# -----------------------------
df["xss_pattern"] = df["payloadSnippet"].str.contains(
    r"<script|onerror=|onload=|<img|<svg",
    case=False,
    na=False
).astype(int)

# -----------------------------
# 5. Weak-supervision labeling
# -----------------------------
def label_attack(row):
    if row["rapid_request"] and row["auth_fail"]:
        return "brute_force"

    if row["large_payload"] and row["auth_fail"]:
        return "sql_injection"

    if row["xss_pattern"] == 1:
        return "xss"

    if row["is_get"] and row["status"] in [403, 404]:
        return "recon"

    return "normal"


df["label"] = df.apply(label_attack, axis=1)

# -----------------------------
# 6. Verification
# -----------------------------
print("\nLabel distribution:")
print(df["label"].value_counts())

# -----------------------------
# 7. Save dataset
# -----------------------------
df.to_csv("ids_dataset_day3.csv", index=False)
print("\nSaved: ids_dataset_day3.csv")

