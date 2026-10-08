from ml.risk_forecast import forecast
from ml.risk_forecast import forecast_from_trend


print("===================================")
print("RISK FORECAST TEST")
print("===================================")


# Current health score
current_score = 80

print("\nCurrent Score:", current_score)
print("Current Risk:", forecast(current_score))


# Improving example
result = forecast_from_trend(
    current_score=85,
    previous_score=75,
    trend="Improving"
)

print("\nImproving Test")
print(result)


# Worsening example
result = forecast_from_trend(
    current_score=60,
    previous_score=80,
    trend="Worsening"
)

print("\nWorsening Test")
print(result)


# Stable example
result = forecast_from_trend(
    current_score=80,
    previous_score=81,
    trend="Stable"
)

print("\nStable Test")
print(result)