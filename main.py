"""
FastAPI Main Server for AgriCure
Fertilizer Recommendation System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import os
import sys
from datetime import datetime
import logging

# Add fertilizer recommendation system to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "fertilizer recommendation system"))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AgriCure API",
    description="Fertilizer Recommendation API",
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
# PYDANTIC MODELS (Request/Response Schemas)
# ============================================================================

# ============================================================================
# OLD FRONTEND FORMAT MODELS (for backward compatibility)
# ============================================================================

class FertilizerPredictionInput(BaseModel):
    """Old frontend format for basic prediction"""
    Temperature: float
    Humidity: float
    Moisture: float
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
    size: float = Field(..., gt=0, description="Field size (will be converted to hectares)")
    unit: str = Field(default="hectares", description="Unit of field size: 'hectares', 'acres', or 'bigha'")
    crop: str = Field(..., description="Crop type (e.g., Wheat, Rice, Maize)")
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

def convert_to_hectares(size: float, unit: str) -> float:
    """
    Convert field size from various units to hectares.
    
    Args:
        size: Field size value
        unit: Unit of measurement ('hectares', 'acres', 'bigha')
        
    Returns:
        Size in hectares
        
    Conversion factors:
        - 1 acre = 0.404686 hectares
        - 1 bigha = 0.25 hectares (standard bigha, varies by region)
    """
    unit_lower = unit.lower().strip()
    
    if unit_lower in ['hectare', 'hectares', 'ha']:
        return size
    elif unit_lower in ['acre', 'acres']:
        return size * 0.404686
    elif unit_lower in ['bigha', 'bighas']:
        # Standard bigha (varies by region: 0.165 to 0.33 hectares)
        # Using 0.25 hectares as average
        return size * 0.25
    else:
        logger.warning(f"Unknown unit '{unit}', assuming hectares")
        return size

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "fertilizer_system_loaded": fertilizer_system is not None,
        "message": "AgriCure API is running"
    }

@app.get("/health")
async def health_check():
    """
    Detailed health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "fertilizer_system_loaded": fertilizer_system is not None,
        "message": "AgriCure API is running"
    }

@app.get("/api-info")
async def get_api_info():
    """
    Get API information and available endpoints
    """
    return {
        "name": "AgriCure Fertilizer Recommendation API",
        "version": "1.0.0",
        "description": "AI-powered fertilizer recommendations for farm management",
        "endpoints": {
            "/": "Health check",
            "/health": "Detailed health status",
            "/api-info": "This endpoint",
            "/fertilizer-recommendation": "Get AI-powered fertilizer recommendations",
            "/predict-llm-enhanced": "LLM-enhanced predictions (frontend compatible)",
            "/predict": "Basic predictions (frontend compatible)"
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
        # Convert field size to hectares
        size_in_hectares = convert_to_hectares(request.size, request.unit)
        logger.info(f"Field size: {request.size} {request.unit} = {size_in_hectares:.4f} hectares")
        logger.info(f"Processing fertilizer recommendation request for {request.crop} on {size_in_hectares:.4f} hectares")
        
        # Call the Final_Model system
        recommendation = fertilizer_system.predict(
            size=size_in_hectares,
            crop=request.crop,
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
        # Convert field size to hectares
        field_unit = request.Field_Unit or "hectares"
        size_in_hectares = convert_to_hectares(request.Field_Size or 1.0, field_unit)
        logger.info(f"Field size: {request.Field_Size} {field_unit} = {size_in_hectares:.4f} hectares")
        
        # Map frontend format to our format
        recommendation_request = FertilizerRecommendationRequest(
            size=size_in_hectares,
            unit="hectares",
            crop=request.Crop_Type,
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
                "total_cost": size_in_hectares * 1000,
                "application_notes": "Apply as recommended"
            },
            "secondary_fertilizer": {
                "name": result.ml_predictions.get("Secondary_Fertilizer", "None"),
                "npk": "Varies",
                "rate_per_hectare": 25,
                "cost_per_hectare": 500,
                "total_cost": size_in_hectares * 500,
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
                "features_used": ["Nitrogen", "Phosphorus", "Potassium", "pH", "Crop_Type"],
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
    logger.info(f"Fertilizer System: {'✓ Loaded' if fertilizer_system else '✗ Not Loaded'}")
    logger.info("CORS: Enabled for all origins")
    logger.info("=" * 70)

@app.on_event("shutdown")
async def shutdown_event():
    """Log shutdown information"""
    logger.info("AgriCure API Server shutting down...")
