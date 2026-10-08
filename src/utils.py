def format_result(pred):
    if pred == 1:
        return "⚠ High Stroke Risk"
    else:
        return "✅ Low Risk"