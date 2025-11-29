# predict_single.py

import joblib
import numpy as np
import pandas as pd

MODEL_PATH = "soil_model_xgb.pkl"
LABEL_ENCODER_PATH = "soil_label_encoder.pkl"

# Same feature order as training
NUMERIC_FEATURES = [
    "lat", "lon",
    "elevation",
    "rainfall",
    "temperature",
    "aridity_index",
    "dist_river_km",
    "dist_coast_km",
    "ndvi"
]

CATEGORICAL_FEATURES = [
    "landcover",
    "geology"
]

def load_model():
    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)
    return model, label_encoder

def predict_soil_type(sample: dict):
    """
    sample = {
        "lat": 23.5,
        "lon": 78.2,
        "elevation": 400,
        "rainfall": 800,
        "temperature": 26,
        "aridity_index": 0.6,
        "dist_river_km": 5.0,
        "dist_coast_km": 800.0,
        "ndvi": 0.45,
        "landcover": "cropland",
        "geology": "basalt"
    }
    """

    model, label_encoder = load_model()

    # Build row as DataFrame (required for column transformer)
    row_dict = {col: [sample[col]] for col in NUMERIC_FEATURES + CATEGORICAL_FEATURES}
    df = pd.DataFrame(row_dict)

    probs = model.predict_proba(df)[0]
    class_index = probs.argmax()
    soil_pred = label_encoder.inverse_transform([class_index])[0]

    # pack probabilities
    prob_map = {
        label_encoder.classes_[i]: float(probs[i])
        for i in range(len(label_encoder.classes_))
    }

    return soil_pred, prob_map

if __name__ == "__main__":
    sample_input = {
        "lat": 23.5,
        "lon": 78.2,
        "elevation": 400,
        "rainfall": 800,
        "temperature": 26,
        "aridity_index": 0.6,
        "dist_river_km": 5.0,
        "dist_coast_km": 800.0,
        "ndvi": 0.45,
        "landcover": "cropland",
        "geology": "basalt"
    }

    soil, probs = predict_soil_type(sample_input)
    print("Predicted soil type:", soil)
    print("Class probabilities:", probs)
