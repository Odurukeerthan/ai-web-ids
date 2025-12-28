import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# -----------------------------
# 1. Load dataset
# -----------------------------
df = pd.read_csv("ids_dataset_day3.csv")

print("Total samples:", len(df))
print("Labels:\n", df["label"].value_counts())

# -----------------------------
# 2. Select features
# -----------------------------
FEATURES = [
    "time_delta",
    "rapid_request",
    "auth_fail",
    "large_payload",
    "is_get",
    "xss_pattern",
    "responseTimeMs"
]

X = df[FEATURES]
y = df["label"]

# -----------------------------
# 3. Encode labels
# -----------------------------
le = LabelEncoder()
y_encoded = le.fit_transform(y)

print("\nLabel mapping:")
for i, label in enumerate(le.classes_):
    print(f"{label} -> {i}")

# -----------------------------
# 4. Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.3, random_state=42
)

# -----------------------------
# 5. Train a small model
# -----------------------------
model = RandomForestClassifier(
    n_estimators=50,
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# 6. Evaluate (SANITY ONLY)
# -----------------------------
y_pred = model.predict(X_test)

print("\nClassification Report (Sanity Check):")
print(classification_report(y_test, y_pred, target_names=le.classes_))
