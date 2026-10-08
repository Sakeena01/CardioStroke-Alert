import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.utils import resample
import joblib

# Load dataset
df = pd.read_csv("data/raw/stroke.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Target variable
df['stroke'] = df['diagnosis'].apply(lambda x: 1 if x == "Stroke" else 0)

# Use real columns
df['age'] = df['age']
df['hypertension'] = df['hypertension'].astype(int)

# 🔥 Generate smartwatch-like features
np.random.seed(42)

df["spo2"] = np.random.normal(96, 3, len(df))
df["heart_rate"] = np.random.normal(75, 12, len(df))

# BP based on hypertension
df["bp_sys"] = np.where(df["hypertension"] == 1,
                       np.random.normal(150, 10, len(df)),
                       np.random.normal(120, 10, len(df)))

df["bp_dia"] = np.where(df["hypertension"] == 1,
                       np.random.normal(95, 8, len(df)),
                       np.random.normal(80, 8, len(df)))

# Select features
X = df[['spo2','heart_rate','age','hypertension','bp_sys','bp_dia']]
y = df['stroke']

# 🔥 Handle imbalance
df_majority = df[df.stroke == 0]
df_minority = df[df.stroke == 1]

df_minority_up = resample(
    df_minority,
    replace=True,
    n_samples=len(df_majority),
    random_state=42
)

df_balanced = pd.concat([df_majority, df_minority_up])

X = df_balanced[['spo2','heart_rate','age','hypertension','bp_sys','bp_dia']]
y = df_balanced['stroke']

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 🔥 Better model
model = XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05
)

model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print("Accuracy:", acc)

# Save model
joblib.dump(model, "models/stroke_model.pkl")

print("Model trained successfully")