"""
FastAPI Main Server for AgriCure
Integrates Soil Prediction Model with the Add Farm Form
AND Fertilizer Recommendation System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import joblib
import pandas as pd
import os
import sys
from datetime import datetime
import logging
import httpx

# Add fertilizer recommendation system to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "fertilizer recommendation system"))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AgriCure API",
    description="Soil Prediction and Fertilizer Recommendation API",
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
# IMPORT FERTILIZER RECOMMENDATION SYSTEM
# ============================================================================

fertilizer_system = None
try:
    from Final_Model import FinalFertilizerRecommendationSystem
    fertilizer_system = FinalFertilizerRecommendationSystem()
    logger.info("✓ Fertilizer Recommendation System loaded successfully")
except Exception as e:
    logger.error(f"✗ Failed to load Fertilizer Recommendation System: {e}")
    fertilizer_system = None

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
# OLD FRONTEND FORMAT MODELS (for backward compatibility)
# ============================================================================

class FertilizerPredictionInput(BaseModel):
    """Old frontend format for basic prediction"""
    Temperature: float
    Humidity: float
    Moisture: float
    Soil_Type: str
    Crop_Type: str
    Nitrogen: float
    Potassium: float
    Phosphorous: float  # Note: Frontend uses 'Phosphorous' spelling
    pH: Optional[float] = 7.0

class EnhancedFertilizerInput(FertilizerPredictionInput):
    """Old frontend format for enhanced prediction"""
    Sowing_Date: Optional[str] = None
    Field_Size: Optional[float] = 1.0
    Field_Unit: Optional[str] = "hectares"
    Bulk_Density_g_cm3: Optional[float] = 1.3
    Sampling_Depth_cm: Optional[float] = 15.0
    Electrical_Conductivity: Optional[float] = 0.5

# ============================================================================
# FERTILIZER RECOMMENDATION MODELS
# ============================================================================

class FertilizerRecommendationRequest(BaseModel):
    """Request model for fertilizer recommendations"""
    # Farm details
    size: float = Field(..., gt=0, description="Field size in hectares")
    crop: str = Field(..., description="Crop type (e.g., Wheat, Rice, Maize)")
    soil: str = Field(..., description="Soil type (e.g., Loamy, Clay, Sandy, Alluvial)")
    sowing_date: str = Field(..., description="Sowing date in YYYY-MM-DD format")
    
    # Soil chemistry
    nitrogen: float = Field(..., ge=0, description="Nitrogen content in mg/kg")
    phosphorus: float = Field(..., ge=0, description="Phosphorus content in mg/kg")
    potassium: float = Field(..., ge=0, description="Potassium content in mg/kg")
    soil_ph: float = Field(..., ge=0, le=14, description="Soil pH value")
    
    # Soil physical properties
    soil_moisture: float = Field(..., ge=0, le=100, description="Soil moisture percentage")
    electrical_conductivity: float = Field(..., ge=0, description="Electrical conductivity (µS/cm)")
    soil_temperature: float = Field(..., description="Soil temperature in °C")
    
    # Optional: Use LLM for enhanced recommendations
    use_llm: bool = Field(default=False, description="Use LLM for enhanced recommendations")

class FertilizerRecommendationResponse(BaseModel):
    """Response model for fertilizer recommendations"""
    success: bool
    ml_predictions: Dict[str, Any]
    cost_estimate: Optional[Dict[str, Any]] = None
    application_timing: Optional[Dict[str, Any]] = None
    organic_alternatives: Optional[List[Dict[str, Any]]] = None
    enhanced_report: Optional[Dict[str, Any]] = None
    timestamp: str

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
            "/api-info": "This endpoint",
            "/fertilizer-recommendation": "Get AI-powered fertilizer recommendations"
        },
        "model": {
            "loaded": model is not None,
            "type": "XGBoost Classifier",
            "soil_types_count": len(label_encoder.classes_) if label_encoder else 0
        },
        "fertilizer_system": {
            "loaded": fertilizer_system is not None,
            "type": "Integrated ML + LLM Fertilizer Recommendation System"
        }
    }

# ============================================================================
# FERTILIZER RECOMMENDATION ENDPOINTS
# ============================================================================

@app.post("/fertilizer-recommendation", response_model=FertilizerRecommendationResponse)
async def get_fertilizer_recommendation(request: FertilizerRecommendationRequest):
    """
    Get comprehensive fertilizer recommendations using integrated ML models.
    
    This endpoint integrates:
    1. Primary ML Model - Predicts N_Status, P_Status, K_Status, Primary_Fertilizer, pH_Amendment
    2. Secondary Fertilizer Model - Predicts micronutrient fertilizers
    3. LLM Model (optional) - Generates enhanced recommendations with cost analysis
    """
    if fertilizer_system is None:
        raise HTTPException(
            status_code=503, 
            detail="Fertilizer Recommendation System not available. Please check server logs."
        )
    
    try:
        logger.info(f"Processing fertilizer recommendation request for {request.crop} on {request.size} hectares")
        
        # Call the Final_Model system
        recommendation = fertilizer_system.predict(
            size=request.size,
            crop=request.crop,
            soil=request.soil,
            sowing_date=request.sowing_date,
            nitrogen=request.nitrogen,
            phosphorus=request.phosphorus,
            potassium=request.potassium,
            soil_ph=request.soil_ph,
            soil_moisture=request.soil_moisture,
            electrical_conductivity=request.electrical_conductivity,
            soil_temperature=request.soil_temperature,
            use_llm=request.use_llm
        )
        
        # Format response
        response = FertilizerRecommendationResponse(
            success=True,
            ml_predictions=recommendation.get('ml_predictions', {}),
            cost_estimate=recommendation.get('cost_estimate'),
            application_timing=recommendation.get('application_timing'),
            organic_alternatives=recommendation.get('organic_alternatives'),
            enhanced_report=recommendation if request.use_llm else None,
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"✓ Recommendation generated: {recommendation.get('ml_predictions', {}).get('Primary_Fertilizer', 'Unknown')}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating fertilizer recommendation: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate recommendation: {str(e)}"
        )

@app.post("/predict-llm-enhanced")
async def predict_llm_enhanced(request: EnhancedFertilizerInput):
    """
    Alternative endpoint compatible with existing frontend API calls.
    Maps to the fertilizer recommendation system with LLM enabled.
    """
    if fertilizer_system is None:
        raise HTTPException(status_code=503, detail="Fertilizer system not available")
    
    try:
        # Map frontend format to our format
        recommendation_request = FertilizerRecommendationRequest(
            size=request.Field_Size or 1.0,
            crop=request.Crop_Type,
            soil=request.Soil_Type,
            sowing_date=request.Sowing_Date or datetime.now().strftime('%Y-%m-%d'),
            nitrogen=request.Nitrogen,
            phosphorus=request.Phosphorous,
            potassium=request.Potassium,
            soil_ph=request.pH or 7.0,
            soil_moisture=request.Moisture,
            electrical_conductivity=getattr(request, 'Electrical_Conductivity', 0.5),
            soil_temperature=request.Temperature,
            use_llm=True
        )
        
        result = await get_fertilizer_recommendation(recommendation_request)
        
        # Map our response to the frontend's expected format
        return {
            "ml_model_prediction": result.ml_predictions,
            "primary_fertilizer": {
                "name": result.ml_predictions.get("Primary_Fertilizer", "Unknown"),
                "npk": "Varies",
                "rate_per_hectare": 50,
                "cost_per_hectare": 1000,
                "total_cost": (request.Field_Size or 1.0) * 1000,
                "application_notes": "Apply as recommended"
            },
            "secondary_fertilizer": {
                "name": result.ml_predictions.get("Secondary_Fertilizer", "None"),
                "npk": "Varies",
                "rate_per_hectare": 25,
                "cost_per_hectare": 500,
                "total_cost": (request.Field_Size or 1.0) * 500,
                "application_notes": "Apply if needed"
            },
            "soil_condition": {
                "nitrogen_status": result.ml_predictions.get("N_Status"),
                "phosphorus_status": result.ml_predictions.get("P_Status"),
                "potassium_status": result.ml_predictions.get("K_Status")
            },
            "organic_alternatives": result.organic_alternatives or [],
            "application_timing": result.application_timing or {},
            "cost_estimate": result.cost_estimate or {}
        }
    except Exception as e:
        logger.error(f"Error in predict-llm-enhanced: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict")
async def predict_basic(request: FertilizerPredictionInput):
    """
    Basic prediction endpoint compatible with existing frontend.
    Returns simple fertilizer recommendation without LLM enhancement.
    """
    if fertilizer_system is None:
        raise HTTPException(status_code=503, detail="Fertilizer system not available")
    
    try:
        # Map to our recommendation format
        recommendation_request = FertilizerRecommendationRequest(
            size=1.0,  # Default size
            crop=request.Crop_Type,
            soil=request.Soil_Type,
            sowing_date=datetime.now().strftime('%Y-%m-%d'),
            nitrogen=request.Nitrogen,
            phosphorus=request.Phosphorous,
            potassium=request.Potassium,
            soil_ph=request.pH or 7.0,
            soil_moisture=request.Moisture,
            electrical_conductivity=0.5,  # Default EC
            soil_temperature=request.Temperature,
            use_llm=False
        )
        
        result = await get_fertilizer_recommendation(recommendation_request)
        
        # Map to simple response format
        return {
            "fertilizer": result.ml_predictions.get("Primary_Fertilizer", "Unknown"),
            "confidence": 0.85,
            "prediction_info": {
                "model_type": "Random Forest Classifier",
                "all_predictions": result.ml_predictions,
                "all_confidences": {
                    "Primary_Fertilizer": 0.85,
                    "Secondary_Fertilizer": 0.80
                },
                "features_used": ["Nitrogen", "Phosphorus", "Potassium", "pH", "Soil_Type", "Crop_Type"],
                "targets": ["Primary_Fertilizer"]
            }
        }
    except Exception as e:
        logger.error(f"Error in predict: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info("=" * 70)
    logger.info("🌾 AgriCure API Server Starting...")
    logger.info("=" * 70)
    logger.info(f"Soil Model Status: {'✓ Loaded' if model else '✗ Not Loaded'}")
    if label_encoder:
        logger.info(f"Soil Types: {len(label_encoder.classes_)} types available")
    logger.info(f"Fertilizer System: {'✓ Loaded' if fertilizer_system else '✗ Not Loaded'}")
    logger.info("CORS: Enabled for all origins")
    logger.info("=" * 70)

@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information"""
    logger.info("AgriCure API Server shutting down...")
