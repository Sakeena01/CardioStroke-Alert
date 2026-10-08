import joblib

model = joblib.load("models/stroke_model.pkl")

print("MODEL TYPE:")
print(type(model))

print("\nNUMBER OF FEATURES:")
print(model.n_features_in_)

print("\nFEATURE NAMES:")
if hasattr(model, "feature_names_in_"):
    print(model.feature_names_in_)
else:
    print("Feature names are not stored in the model.")

print("\nMODEL PARAMETERS:")
print(model.get_params())