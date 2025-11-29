# api_server.py

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Load once at startup
MODEL_PATH = "soil_model_xgb.pkl"
LABEL_ENCODER_PATH = "soil_label_encoder.pkl"

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)

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

class SoilRequest(BaseModel):
    lat: float
    lon: float
    elevation: float
    rainfall: float
    temperature: float
    aridity_index: float
    dist_river_km: float
    dist_coast_km: float
    ndvi: float
    landcover: str
    geology: str

class SoilResponse(BaseModel):
    predicted_soil: str
    probabilities: dict

app = FastAPI(title="India Soil Type Prediction API")

@app.post("/predict", response_model=SoilResponse)
def predict(req: SoilRequest):
    # Build row as DataFrame (required for column transformer)
    row_dict = {col: [getattr(req, col)] for col in NUMERIC_FEATURES + CATEGORICAL_FEATURES}
    df = pd.DataFrame(row_dict)

    probs = model.predict_proba(df)[0]
    idx = probs.argmax()
    soil_pred = label_encoder.inverse_transform([idx])[0]

    prob_map = {
        label_encoder.classes_[i]: float(probs[i])
        for i in range(len(label_encoder.classes_))
    }

    return SoilResponse(predicted_soil=soil_pred, probabilities=prob_map)
