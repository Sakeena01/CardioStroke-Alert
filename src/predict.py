import joblib

model = joblib.load("models/stroke_model.pkl")

def predict(data):
    return model.predict(data)[0]