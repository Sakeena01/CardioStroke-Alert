import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

from xgboost import XGBClassifier


# ===============================
# Load Dataset
# ===============================

df = pd.read_csv("data/stroke.csv")

# ===============================
# Select Features
# ===============================

X = df[[
    "age",
    "heart_rate",
    "spo2",
    "sbp",
    "dbp",
    "bmi",
    "glucose",
    "steps",
    "ecg",
    "fall"
]]

y = df["stroke"]

# ===============================
# Split Dataset
# ===============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ===============================
# Feature Scaling
# ===============================

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save Scaler
joblib.dump(scaler, "models/scaler.pkl")

# ===============================
# XGBoost Model
# ===============================

model = XGBClassifier(

    n_estimators=200,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.9,
    colsample_bytree=0.9,
    random_state=42,
    eval_metric="logloss"

)

model.fit(X_train, y_train)

# ===============================
# Evaluation
# ===============================

pred = model.predict(X_test)

accuracy = accuracy_score(y_test, pred)

print("\nAccuracy :", round(accuracy * 100, 2), "%\n")

print(classification_report(y_test, pred))

# ===============================
# Save Model
# ===============================

joblib.dump(model, "models/stroke_model.pkl")

print("\nModel Saved Successfully")
print("Scaler Saved Successfully")