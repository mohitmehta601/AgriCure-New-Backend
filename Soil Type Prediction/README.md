# India Soil Type Prediction System

Complete ML pipeline for predicting soil types across India using geolocation and environmental features.

## Features

- **XGBoost-based classifier** for multi-class soil type prediction
- **Geospatial features**: latitude, longitude, elevation, distance to rivers/coasts
- **Environmental features**: rainfall, temperature, aridity index, NDVI
- **Categorical features**: land cover, geology
- **Production-ready FastAPI server** for deployment

## Soil Types Supported

- Alluvial
- Black
- Red
- Laterite
- Arid
- Clayey
- Alkaline

## Installation

```bash
pip install -r requirements.txt
```

## Dataset Format

Your CSV file should contain these columns:

**Numeric features:**

- `lat` - Latitude
- `lon` - Longitude
- `elevation` - Elevation in meters
- `rainfall` - Annual rainfall in mm
- `temperature` - Average temperature in °C
- `aridity_index` - Aridity index (0-1)
- `dist_river_km` - Distance to nearest river in km
- `dist_coast_km` - Distance to coast in km
- `ndvi` - Normalized Difference Vegetation Index

**Categorical features:**

- `landcover` - Land cover type (e.g., cropland, forest, grassland)
- `geology` - Geological formation (e.g., basalt, granite, alluvium)

**Target:**

- `soil_type` - Soil classification

## Usage

### 1. Train the Model

```bash
python train_soil_model.py
```

This will:

- Load your dataset from `india_soil_dataset.csv`
- Train an XGBoost classifier
- Save the model to `soil_model_xgb.pkl`
- Save the label encoder to `soil_label_encoder.pkl`
- Print evaluation metrics

**Configuration:** Edit `DATA_PATH` in `train_soil_model.py` to point to your dataset.

### 2. Make Single Predictions

```bash
python predict_single.py
```

Or use in your code:

```python
from predict_single import predict_soil_type

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

soil_type, probabilities = predict_soil_type(sample)
print(f"Predicted: {soil_type}")
print(f"Probabilities: {probabilities}")
```

### 3. Deploy API Server

```bash
uvicorn api_server:app --reload --port 8000
```

**API Endpoint:** `POST http://localhost:8000/predict`

**Request example:**

```json
{
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
```

**Response example:**

```json
{
  "predicted_soil": "Black",
  "probabilities": {
    "Alluvial": 0.05,
    "Black": 0.78,
    "Red": 0.1,
    "Laterite": 0.02,
    "Arid": 0.01,
    "Clayey": 0.03,
    "Alkaline": 0.01
  }
}
```

**Test with curl:**

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

## Model Architecture

- **Preprocessing Pipeline:**
  - Numeric features: passthrough
  - Categorical features: One-Hot Encoding
- **Classifier:** XGBoost
  - 400 estimators
  - Learning rate: 0.05
  - Max depth: 8
  - Subsample: 0.8
  - Multi-class softprob objective

## Files

- `train_soil_model.py` - Training script
- `predict_single.py` - Single prediction utility
- `api_server.py` - FastAPI production server
- `requirements.txt` - Python dependencies
- `soil_model_xgb.pkl` - Saved trained model (generated after training)
- `soil_label_encoder.pkl` - Saved label encoder (generated after training)

## Customization

### Add/Remove Features

Edit the feature lists in all three Python files:

```python
NUMERIC_FEATURES = [...]
CATEGORICAL_FEATURES = [...]
```

### Tune Hyperparameters

In `train_soil_model.py`, modify the `XGBClassifier` parameters:

```python
xgb_clf = XGBClassifier(
    n_estimators=400,      # Number of trees
    learning_rate=0.05,    # Step size
    max_depth=8,           # Tree depth
    # ... more parameters
)
```

## Production Deployment

For production use:

1. **Use environment variables** for paths
2. **Add authentication** to API endpoints
3. **Set up logging** and monitoring
4. **Deploy with Docker** or cloud services
5. **Use production ASGI server**:
   ```bash
   uvicorn api_server:app --host 0.0.0.0 --port 8000 --workers 4
   ```

## License

MIT
