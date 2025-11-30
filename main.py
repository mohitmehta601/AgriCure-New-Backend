"""
FastAPI Main Server for AgriCure
Integrates Soil Prediction Model with the Add Farm Form
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import joblib
import pandas as pd
import os
from datetime import datetime
import logging
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AgriCure API",
    description="Soil Prediction and Farm Management API",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# MODEL LOADING
# ============================================================================

MODEL_PATH = os.path.join("Soil Type Prediction", "soil_model_xgb.pkl")
LABEL_ENCODER_PATH = os.path.join("Soil Type Prediction", "soil_label_encoder.pkl")

# Features configuration
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

# Load models at startup
try:
    model = joblib.load(MODEL_PATH)
    label_encoder = joblib.load(LABEL_ENCODER_PATH)
    logger.info("✓ Soil prediction model loaded successfully")
except Exception as e:
    logger.error(f"✗ Failed to load model: {e}")
    model = None
    label_encoder = None

# ============================================================================
# PYDANTIC MODELS (Request/Response Schemas)
# ============================================================================

class LocationData(BaseModel):
    """Location coordinates from browser geolocation"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")

class SoilPredictionRequest(BaseModel):
    """Request model for soil prediction with all required features"""
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")
    elevation: float = Field(..., description="Elevation in meters")
    rainfall: float = Field(..., ge=0, description="Annual rainfall in mm")
    temperature: float = Field(..., description="Average temperature in °C")
    aridity_index: float = Field(..., ge=0, le=1, description="Aridity index (0-1)")
    dist_river_km: float = Field(..., ge=0, description="Distance to nearest river in km")
    dist_coast_km: float = Field(..., ge=0, description="Distance to coast in km")
    ndvi: float = Field(..., ge=-1, le=1, description="Normalized Difference Vegetation Index")
    landcover: str = Field(..., description="Land cover type (e.g., cropland, forest)")
    geology: str = Field(..., description="Geological formation type")

class SoilProperties(BaseModel):
    """Soil chemical and physical properties"""
    clay: Optional[float] = None
    sand: Optional[float] = None
    silt: Optional[float] = None
    phh2o: Optional[float] = None
    cec: Optional[float] = None
    nitrogen: Optional[float] = None
    soc: Optional[float] = None

class LocationInfo(BaseModel):
    """Location information from reverse geocoding"""
    city: str = ""
    locality: str = ""
    region: str = ""
    country: str = ""
    formatted_address: List[str] = []

class SoilDataResponse(BaseModel):
    """Complete soil data response for Add Farm form"""
    location: Dict[str, Any]
    soil_type: str
    soil_properties: SoilProperties
    confidence: float
    sources: List[str]
    success: bool
    location_info: LocationInfo

class SoilPredictionResponse(BaseModel):
    """Response model with predicted soil type and probabilities"""
    predicted_soil: str
    probabilities: Dict[str, float]
    confidence: float
    timestamp: str

class HealthResponse(BaseModel):
    """API health check response"""
    status: str
    timestamp: str
    model_loaded: bool
    message: str

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_default_environmental_data(lat: float, lon: float) -> dict:
    """
    Generate default environmental data based on location.
    In production, this should fetch real data from external APIs.
    """
    avg_lat = abs(lat)
    
    # Temperature estimation based on latitude (very simplified)
    if avg_lat < 15:
        temp = 28 + (15 - avg_lat) * 0.5
    elif avg_lat < 30:
        temp = 25 + (30 - avg_lat) * 0.2
    else:
        temp = 20
    
    # Rainfall estimation (simplified)
    rainfall = 800 if avg_lat < 25 else 600
    
    # Aridity index estimation
    aridity = 0.65 if avg_lat < 20 else 0.5
    
    return {
        "elevation": 300.0,
        "rainfall": rainfall,
        "temperature": temp,
        "aridity_index": aridity,
        "dist_river_km": 10.0,
        "dist_coast_km": 500.0,
        "ndvi": 0.45,
        "landcover": "cropland",
        "geology": "alluvium"
    }

async def get_location_info(latitude: float, longitude: float) -> LocationInfo:
    """
    Get detailed location information using reverse geocoding.
    Uses Nominatim (OpenStreetMap) API - free and no API key required.
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Nominatim requires a User-Agent header
            headers = {
                "User-Agent": "AgriCure/1.0 (Farm Management Application)"
            }
            
            url = "https://nominatim.openstreetmap.org/reverse"
            params = {
                "lat": latitude,
                "lon": longitude,
                "format": "json",
                "addressdetails": 1,
                "zoom": 18  # Highest detail level
            }
            
            response = await client.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                address = data.get("address", {})
                
                # Extract location components
                city = (
                    address.get("city") or 
                    address.get("town") or 
                    address.get("village") or 
                    address.get("municipality") or
                    ""
                )
                
                locality = (
                    address.get("suburb") or
                    address.get("neighbourhood") or
                    address.get("locality") or
                    address.get("hamlet") or
                    ""
                )
                
                region = (
                    address.get("state") or
                    address.get("province") or
                    address.get("region") or
                    ""
                )
                
                country = address.get("country", "India")
                
                # Build formatted address parts
                formatted_parts = []
                if locality and locality != city:
                    formatted_parts.append(locality)
                if city:
                    formatted_parts.append(city)
                if region:
                    formatted_parts.append(region)
                if country:
                    formatted_parts.append(country)
                
                # Add postal code if available
                if address.get("postcode"):
                    formatted_parts.append(f"PIN: {address.get('postcode')}")
                
                return LocationInfo(
                    city=city,
                    locality=locality,
                    region=region,
                    country=country,
                    formatted_address=formatted_parts
                )
            else:
                logger.warning(f"Reverse geocoding failed with status {response.status_code}")
                return LocationInfo(country="India")
                
    except Exception as e:
        logger.error(f"Error during reverse geocoding: {e}")
        return LocationInfo(country="India")

def predict_soil_type_from_model(request: SoilPredictionRequest) -> SoilPredictionResponse:
    """
    Make soil type prediction using the loaded XGBoost model
    """
    if model is None or label_encoder is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Create feature dictionary in correct order
        features = {
            'lat': request.lat,
            'lon': request.lon,
            'elevation': request.elevation,
            'rainfall': request.rainfall,
            'temperature': request.temperature,
            'aridity_index': request.aridity_index,
            'dist_river_km': request.dist_river_km,
            'dist_coast_km': request.dist_coast_km,
            'ndvi': request.ndvi,
            'landcover': request.landcover,
            'geology': request.geology
        }
        
        # Convert to DataFrame
        X = pd.DataFrame([features])
        
        # Make prediction
        pred = model.predict(X)[0]
        probs = model.predict_proba(X)[0]
        
        # Get predicted soil type
        soil_pred = label_encoder.inverse_transform([pred])[0]
        
        # Get confidence (probability of predicted class)
        idx = pred
        
        # Create probability map for all classes
        prob_map = {
            label_encoder.classes_[i]: float(probs[i])
            for i in range(len(label_encoder.classes_))
        }
        
        return SoilPredictionResponse(
            predicted_soil=soil_pred,
            probabilities=prob_map,
            confidence=float(probs[idx]),
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - API health check"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        model_loaded=model is not None,
        message="AgriCure API is running"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check endpoint"""
    return HealthResponse(
        status="healthy" if model is not None else "degraded",
        timestamp=datetime.now().isoformat(),
        model_loaded=model is not None,
        message="Soil prediction model loaded" if model else "Model not loaded"
    )

@app.post("/soil-data", response_model=SoilDataResponse)
async def get_soil_data(location: LocationData):
    """
    Main endpoint for Add Farm form.
    Accepts location coordinates and returns complete soil data with reverse geocoding.
    """
    if model is None or label_encoder is None:
        raise HTTPException(status_code=503, detail="Soil prediction model not available")
    
    try:
        # Get default environmental data based on location
        env_data = get_default_environmental_data(location.latitude, location.longitude)
        
        # Create prediction request
        prediction_request = SoilPredictionRequest(
            lat=location.latitude,
            lon=location.longitude,
            **env_data
        )
        
        # Get soil prediction
        prediction = predict_soil_type_from_model(prediction_request)
        
        # Get detailed location information via reverse geocoding
        location_info = await get_location_info(location.latitude, location.longitude)
        
        # Format response for frontend
        response = SoilDataResponse(
            location={
                "latitude": location.latitude,
                "longitude": location.longitude,
                "timestamp": datetime.now().isoformat()
            },
            soil_type=prediction.predicted_soil,
            soil_properties=SoilProperties(
                clay=None,
                sand=None,
                silt=None,
                phh2o=None,
                cec=None,
                nitrogen=None,
                soc=None
            ),
            confidence=prediction.confidence,
            sources=["ML Model Prediction", "XGBoost Classifier"],
            success=True,
            location_info=location_info
        )
        
        logger.info(f"Soil prediction: {prediction.predicted_soil} (confidence: {prediction.confidence:.2%})")
        if location_info.formatted_address:
            logger.info(f"Location: {', '.join(location_info.formatted_address)}")
        return response
        
    except Exception as e:
        logger.error(f"Error in soil-data endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get soil data: {str(e)}")

@app.post("/predict-soil", response_model=SoilPredictionResponse)
async def predict_soil(request: SoilPredictionRequest):
    """
    Direct soil prediction endpoint with full environmental data.
    For advanced users who have all the required parameters.
    """
    return predict_soil_type_from_model(request)

@app.get("/soil-types")
async def get_soil_types():
    """
    Get list of all possible soil types that the model can predict
    """
    if label_encoder is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "soil_types": label_encoder.classes_.tolist(),
        "count": len(label_encoder.classes_)
    }

@app.get("/model-info")
async def get_model_info():
    """
    Get detailed model information for ML status dashboard
    """
    if model is None or label_encoder is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": "XGBoost Classifier (Soil Prediction)",
        "features": NUMERIC_FEATURES + CATEGORICAL_FEATURES,
        "targets": ["soil_type"],
        "label_encoders": {
            "soil_type": label_encoder.classes_.tolist()
        },
        "n_features": len(NUMERIC_FEATURES + CATEGORICAL_FEATURES),
        "n_classes": len(label_encoder.classes_),
        "status": "loaded"
    }

@app.get("/api-info")
async def get_api_info():
    """
    Get API information and available endpoints
    """
    return {
        "name": "AgriCure Soil Prediction API",
        "version": "1.0.0",
        "description": "Soil type prediction for farm management",
        "endpoints": {
            "/": "Health check",
            "/health": "Detailed health status",
            "/soil-data": "Get soil data from location (for Add Farm form)",
            "/predict-soil": "Direct soil prediction with full parameters",
            "/soil-types": "List all predictable soil types",
            "/model-info": "Detailed model information",
            "/api-info": "This endpoint"
        },
        "model": {
            "loaded": model is not None,
            "type": "XGBoost Classifier",
            "soil_types_count": len(label_encoder.classes_) if label_encoder else 0
        }
    }

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info("=" * 70)
    logger.info("🌾 AgriCure API Server Starting...")
    logger.info("=" * 70)
    logger.info(f"Model Status: {'✓ Loaded' if model else '✗ Not Loaded'}")
    if label_encoder:
        logger.info(f"Soil Types: {len(label_encoder.classes_)} types available")
    logger.info("CORS: Enabled for all origins")
    logger.info("=" * 70)

@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information"""
    logger.info("AgriCure API Server shutting down...")
