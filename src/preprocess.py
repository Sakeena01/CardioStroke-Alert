import numpy as np

def preprocess(data):
    return np.array([[
        data["spo2"],
        data["heart_rate"],
        data["age"],
        data["hypertension"],
        data["bp_sys"],
        data["bp_dia"]
    ]])