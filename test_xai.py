from ml.explainable_ai import explain_prediction


result = explain_prediction(

    age=24,

    heart_rate=98,

    spo2=98,

    sbp=148,

    dbp=80,

    bmi=30.5,

    glucose=175,

    steps=1030,

    prediction=1,

    confidence=96.08

)


print()
print("========== EXPLAINABLE AI ==========")

print()

print(
    "Prediction:",
    result["prediction"]
)

print(
    "Confidence:",
    result["confidence"],
    "%"
)

print()

print(
    "High Factors:",
    result["high_count"]
)

print(
    "Moderate Factors:",
    result["moderate_count"]
)

print(
    "Normal Factors:",
    result["normal_count"]
)

print()

print("---------- FACTORS ----------")

for factor in result["factors"]:

    print(
        factor["name"],
        ":",
        factor["value"],
        "->",
        factor["severity"]
    )

print()

print("---------- SUMMARY ----------")

print(
    result["summary"]
)

print()