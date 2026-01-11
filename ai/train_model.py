import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("ids_dataset_final.csv")

# -----------------------------
# Encode labels
# -----------------------------
label_map = {label: i for i, label in enumerate(df["label"].unique())}
df["label_enc"] = df["label"].map(label_map)

y = df["label_enc"]

# -----------------------------
# Select ONLY numeric features
# -----------------------------
X = df.select_dtypes(include=["number"]).drop(columns=["label_enc"])

# -----------------------------
# Train / test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# -----------------------------
# Scaling (only numeric)
# -----------------------------
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
# -----------------------------
# Baseline Model: Logistic Regression
# -----------------------------
lr = LogisticRegression(
    max_iter=2000,
    class_weight="balanced",
    n_jobs=-1
)

lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

print("\n=== Logistic Regression ===")
print(classification_report(y_test, y_pred_lr))
print(confusion_matrix(y_test, y_pred_lr))
# -----------------------------
# Strong Model: Random Forest
# -----------------------------
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=20,
    class_weight="balanced_subsample",
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

print("\n=== Random Forest ===")
print(classification_report(y_test, y_pred_rf))
print(confusion_matrix(y_test, y_pred_rf))
