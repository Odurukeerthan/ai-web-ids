import pandas as pd

WINDOW_SIZE = 20      # requests per window
STEP_SIZE = 5         # sliding step

df = pd.read_csv("ids_dataset_day3.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True, format="mixed")
df = df.sort_values("timestamp")

rows = []

def resolve_label(labels):
    priority = ["xss", "sql_injection", "brute_force", "recon", "normal"]
    for p in priority:
        if p in labels.values:
            return p
    return "normal"

for ip, group in df.groupby("ip"):
    group = group.reset_index(drop=True)

    for start in range(0, len(group) - WINDOW_SIZE + 1, STEP_SIZE):
        window = group.iloc[start:start + WINDOW_SIZE]

        rows.append({
            "ip": ip,
            "start_time": window["timestamp"].iloc[0],
            "req_count": len(window),
            "auth_fail_count": window["auth_fail"].sum(),
            "rapid_req_count": window["rapid_request"].sum(),
            "large_payload_count": window["large_payload"].sum(),
            "xss_hits": window["xss_pattern"].sum(),
            "sqli_hits": window["sqli_pattern"].sum(),
            "get_requests": window["is_get"].sum(),
            "avg_response_time": window["responseTimeMs"].mean(),
            "label": resolve_label(window["label"])
        })

sliding_df = pd.DataFrame(rows)

print("Sliding-window samples:", len(sliding_df))
print("\nSliding label distribution:")
print(sliding_df["label"].value_counts())

sliding_df.to_csv("ids_dataset_sliding.csv", index=False)
print("\nSaved ids_dataset_sliding.csv")
