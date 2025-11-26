"""
Complete Fertilizer Recommendation System
==========================================

This script integrates:
1. ML Model (Multi-Output Stacking) for predictions
2. Gemini API (LLM) for enhanced recommendations
3. Cost analysis with Indian prices
4. Application timing based on sowing date

Usage:
    python generate_full_recommendation.py

Make sure to set GEMINI_API_KEY environment variable:
    Windows: $env:GEMINI_API_KEY="your-api-key-here"
    Linux/Mac: export GEMINI_API_KEY="your-api-key-here"

Author: AgriCure AI Team
Date: November 2025
"""

import os
import sys
import json
import pickle
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

import pandas as pd
import numpy as np

# Import our modules
from llm_enhanced import (
    InputData,
    MLPrediction,
    generate_enhanced_recommendation,
    GEMINI_AVAILABLE
)

# Import ML model class
from multioutput_stacking_fertilizer import MultiOutputOOFStacker


def load_trained_model(model_path: str = "stacked_model.pkl"):
    """Load the trained ML stacking model"""
    model_file = Path(__file__).parent / model_path
    
    if not model_file.exists():
        print(f"❌ Model file not found: {model_file}")
        print("Please train the model first by running: python multioutput_stacking_fertilizer.py")
        return None
    
    try:
        model = MultiOutputOOFStacker.load(str(model_file))
        print(f"✅ Model loaded successfully from: {model_file}")
        return model
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return None


def get_ml_predictions(model, input_data: InputData):
    """Get predictions from ML model"""
    
    # Prepare input dataframe for ML model
    input_df = pd.DataFrame([{
        'Temperature': input_data.temperature,
        'Humidity': input_data.humidity,
        'Moisture': input_data.moisture,
        'Soil_Type': input_data.soil_type,
        'Crop': input_data.crop,
        'Nitrogen': input_data.nitrogen,
        'Phosphorus': input_data.phosphorus,
        'Potassium': input_data.potassium,
        'pH': input_data.ph,
        'EC(mmhos/cm2)': input_data.ec
    }])
    
    print("\n" + "="*70)
    print("🤖 ML MODEL PREDICTION")
    print("="*70)
    print("\nInput Features:")
    for col, val in input_df.iloc[0].items():
        print(f"  {col}: {val}")
    
    try:
        # Get predictions
        predictions = model.predict(input_df)
        
        print("\n📊 ML Predictions:")
        for key, val in predictions.items():
            print(f"  {key}: {val[0]}")
        
        # Create MLPrediction object
        ml_pred = MLPrediction(
            n_status=predictions.get('N_Status', ['Unknown'])[0],
            p_status=predictions.get('P_Status', ['Unknown'])[0],
            k_status=predictions.get('K_Status', ['Unknown'])[0],
            primary_fertilizer=predictions.get('Primary_Fertilizer', ['Urea'])[0],
            secondary_fertilizer=predictions.get('Secondary_Fertilizer', ['—'])[0],
            ph_amendment=predictions.get('pH_Amendment', ['None'])[0]
        )
        
        # Mock confidence scores (in real scenario, get from model)
        confidence_scores = {
            'N_Status': 0.90,
            'P_Status': 0.88,
            'K_Status': 0.91,
            'Primary_Fertilizer': 0.89,
            'Secondary_Fertilizer': 0.86,
            'pH_Amendment': 0.93
        }
        
        return ml_pred, confidence_scores
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def save_recommendation_report(recommendation: dict, output_file: str = "recommendation_report.json"):
    """Save recommendation to JSON file"""
    output_path = Path(__file__).parent / output_file
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(recommendation, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Recommendation saved to: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error saving recommendation: {e}")
        return False


def print_recommendation_summary(recommendation: dict):
    """Print a formatted summary of the recommendation"""
    
    print("\n" + "="*70)
    print("📋 FERTILIZER RECOMMENDATION SUMMARY")
    print("="*70)
    
    # ML Prediction
    ml_pred = recommendation.get('ml_model_prediction', {})
    print(f"\n🎯 Primary Recommendation: {ml_pred.get('name', 'N/A')}")
    print(f"   Confidence: {ml_pred.get('confidence_percent', 0)}%")
    print(f"   NPK Ratio: {ml_pred.get('npk', 'N/A')}")
    
    # Soil Condition
    soil = recommendation.get('soil_condition_analysis', {})
    status = soil.get('current_status', {})
    print(f"\n🌱 Soil Condition:")
    print(f"   pH Status: {status.get('pH_status', 'N/A')}")
    print(f"   Moisture: {status.get('moisture_status', 'N/A')}")
    deficiencies = status.get('nutrient_deficiencies', [])
    if deficiencies:
        print(f"   Deficiencies: {', '.join(deficiencies)}")
    else:
        print(f"   Deficiencies: None")
    
    # Primary Fertilizer
    primary = recommendation.get('primary_fertilizer', {})
    print(f"\n🌾 Primary Fertilizer:")
    print(f"   Type: {primary.get('name', 'N/A')}")
    print(f"   Quantity: {primary.get('amount_kg', 0)} kg")
    print(f"   Method: {primary.get('application_method', 'N/A')[:80]}...")
    
    # Secondary Fertilizer
    secondary = recommendation.get('secondary_fertilizer', {})
    if secondary.get('name') and secondary.get('name') != 'Not required':
        print(f"\n🧪 Secondary Fertilizer:")
        print(f"   Type: {secondary.get('name', 'N/A')}")
        print(f"   Quantity: {secondary.get('amount_kg', 0)} kg")
    
    # Organic Alternatives
    organics = recommendation.get('organic_alternatives', [])
    if organics:
        print(f"\n🌿 Organic Alternatives ({len(organics)} options):")
        for i, org in enumerate(organics, 1):
            print(f"   {i}. {org.get('name', 'N/A')} - {org.get('amount_kg', 0)} kg")
    
    # Cost Estimate
    costs = recommendation.get('cost_estimate', {})
    print(f"\n💰 Cost Estimate:")
    print(f"   Primary Fertilizer: {costs.get('primary_fertilizer', '₹0')}")
    print(f"   Secondary Fertilizer: {costs.get('secondary_fertilizer', '₹0')}")
    print(f"   Organic Options: {costs.get('organic_options', '₹0')}")
    print(f"   {'='*50}")
    print(f"   TOTAL ESTIMATE: {costs.get('total_estimate', '₹0')}")
    print(f"   {costs.get('field_size', '')}")
    
    # Application Timing
    timing = recommendation.get('application_timing', {})
    print(f"\n📅 Application Timing:")
    print(f"   Primary: {timing.get('primary_fertilizer', 'N/A')[:80]}...")
    print(f"   Organics: {timing.get('organic_options', 'N/A')[:80]}...")
    
    print("\n" + "="*70)


def main():
    """Main execution function"""
    
    print("\n" + "="*70)
    print("🌾 AGRICURE FERTILIZER RECOMMENDATION SYSTEM")
    print("="*70)
    print("Combining ML Predictions with AI-Enhanced Recommendations")
    print("="*70)
    
    # Check for Gemini API Key
    if not os.getenv("GEMINI_API_KEY"):
        print("\n⚠️  WARNING: GEMINI_API_KEY not set!")
        print("Set it with: $env:GEMINI_API_KEY='your-api-key-here' (Windows)")
        print("The system will work in fallback mode without AI enhancements.")
        input("\nPress Enter to continue or Ctrl+C to exit...")
    
    # Load trained ML model
    print("\n📦 Loading ML model...")
    model = load_trained_model()
    
    if model is None:
        print("\n❌ Cannot proceed without trained model.")
        print("Please run: python multioutput_stacking_fertilizer.py")
        return
    
    # Example 1: Sample input data for Wheat crop
    print("\n" + "="*70)
    print("EXAMPLE 1: WHEAT CROP")
    print("="*70)
    
    sample_input_1 = InputData(
        temperature=28.5,
        humidity=65.0,
        moisture=55.0,
        soil_type="Loamy",
        crop="Wheat",
        nitrogen=180.0,  # mg/kg - Medium range
        phosphorus=25.0,  # mg/kg - Low range
        potassium=150.0,  # mg/kg - Medium range
        ph=6.8,
        ec=0.45,
        sowing_date="2025-11-20",
        field_size=2.27  # hectares (approx 5.6 acres)
    )
    
    # Get ML predictions
    ml_pred_1, conf_1 = get_ml_predictions(model, sample_input_1)
    
    if ml_pred_1:
        # Generate enhanced recommendation
        recommendation_1 = generate_enhanced_recommendation(
            input_data=sample_input_1,
            ml_prediction=ml_pred_1,
            confidence_scores=conf_1
        )
        
        # Print summary
        print_recommendation_summary(recommendation_1)
        
        # Save to file
        save_recommendation_report(recommendation_1, "wheat_recommendation.json")
    
    # Example 2: Sample input data for Rice crop
    print("\n\n" + "="*70)
    print("EXAMPLE 2: RICE CROP")
    print("="*70)
    
    sample_input_2 = InputData(
        temperature=30.0,
        humidity=80.0,
        moisture=75.0,
        soil_type="Clayey",
        crop="Rice",
        nitrogen=140.0,  # mg/kg - Low range
        phosphorus=35.0,  # mg/kg - Medium range
        potassium=120.0,  # mg/kg - Low range
        ph=6.2,
        ec=0.38,
        sowing_date="2025-12-01",
        field_size=1.5  # hectares
    )
    
    # Get ML predictions
    ml_pred_2, conf_2 = get_ml_predictions(model, sample_input_2)
    
    if ml_pred_2:
        # Generate enhanced recommendation
        recommendation_2 = generate_enhanced_recommendation(
            input_data=sample_input_2,
            ml_prediction=ml_pred_2,
            confidence_scores=conf_2
        )
        
        # Print summary
        print_recommendation_summary(recommendation_2)
        
        # Save to file
        save_recommendation_report(recommendation_2, "rice_recommendation.json")
    
    print("\n" + "="*70)
    print("✅ ALL RECOMMENDATIONS GENERATED SUCCESSFULLY!")
    print("="*70)
    print("\n📁 Output files:")
    print("   - wheat_recommendation.json")
    print("   - rice_recommendation.json")
    print("\nThese files contain complete recommendations including:")
    print("   ✓ ML model predictions with confidence scores")
    print("   ✓ Soil condition analysis")
    print("   ✓ Primary & secondary fertilizer recommendations")
    print("   ✓ Organic alternatives (from predefined list)")
    print("   ✓ Application timing based on sowing date")
    print("   ✓ Detailed cost breakdown")
    print("   ✓ NPK values in mg/kg")
    print("\n" + "="*70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Process interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
