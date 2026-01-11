import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay


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

# Feature importance

features = X.columns
importances = rf.feature_importances_

fi = pd.Series(importances, index=features).sort_values(ascending=False)

plt.figure(figsize=(10,5))
fi.head(10).plot(kind="bar")
plt.title("Top Feature Importances (Random Forest)")
plt.ylabel("Importance")
plt.tight_layout()
plt.savefig("plots/feature_importance.png")
plt.show()

# Confusion matrix

ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred_rf,
    display_labels=label_map.keys(),
    xticks_rotation=45
)
plt.title("Random Forest Confusion Matrix")
plt.tight_layout()
plt.savefig("plots/confusion_matrix.png")
plt.show()

# Dataset class distribution

df["label"].value_counts().plot(
    kind="bar", figsize=(7,4), title="Final Dataset Class Distribution"
)
plt.ylabel("Window Count")
plt.tight_layout()
plt.savefig("plots/class_distribution.png")
plt.show()

# Brute force temporal pattern

bf = df[df["label"] == "brute_force"]

plt.figure(figsize=(10,4))
plt.plot(bf["req_count"].values[:200])
plt.title("Brute Force Request Burst Pattern")
plt.ylabel("Requests per Window")
plt.xlabel("Window Index")
plt.tight_layout()
plt.savefig("plots/bruteforce_timeline.png")
plt.show()
