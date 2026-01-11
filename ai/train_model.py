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
