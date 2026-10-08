import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from xgboost import XGBClassifier


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv("data/stroke.csv")


# ============================================================
# FEATURES
# ============================================================

FEATURES = [
    "age",
    "heart_rate",
    "spo2",
    "sbp",
    "dbp",
    "bmi",
    "glucose",
    "steps"
]

X = df[FEATURES]
y = df["stroke"]


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# SCALING
# ============================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ============================================================
# XGBOOST
# ============================================================

model = XGBClassifier(
    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42,
    eval_metric="logloss"
)


# ============================================================
# TRAIN
# ============================================================

model.fit(
    X_train_scaled,
    y_train
)


# ============================================================
# EVALUATION
# ============================================================

predictions = model.predict(X_test_scaled)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\n===================================")
print("WEARABLE MODEL RESULTS")
print("===================================")

print(
    "Accuracy:",
    round(accuracy * 100, 2),
    "%"
)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions
    )
)

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        predictions
    )
)


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(
    model,
    "models/wearable_model.pkl"
)

joblib.dump(
    scaler,
    "models/wearable_scaler.pkl"
)


# ============================================================
# FINISHED
# ============================================================

print("\n===================================")
print("MODEL SAVED SUCCESSFULLY")
print("===================================")

print("models/wearable_model.pkl")
print("models/wearable_scaler.pkl")

print("\nFeatures used:")

for i, feature in enumerate(FEATURES, start=1):
    print(f"{i}. {feature}")