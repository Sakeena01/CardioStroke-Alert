from ml.predictor import predict_health


data = [
    45,      # age
    78,      # heart rate
    98,      # spo2
    120,     # sbp
    80,      # dbp
    24.5,    # bmi
    95,      # glucose
    6500     # steps
]


print("================================")
print("WEARABLE MODEL TEST")
print("================================")


prediction, confidence, stroke_probability, normal_probability = predict_health(data)


print("Prediction:", prediction)
print("Confidence:", confidence, "%")
print("Stroke Probability:", stroke_probability, "%")
print("Normal Probability:", normal_probability, "%")