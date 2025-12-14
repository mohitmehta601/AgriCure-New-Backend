"""
FINAL INTEGRATED FERTILIZER RECOMMENDATION SYSTEM
==================================================

This module integrates three models:
1. primary_fertilizer_pH_model.py - Rule-based N_Status, P_Status, K_Status, Primary_Fertilizer, pH_Amendment
2. secondary_fertilizer_model.py - Predicts Secondary_Fertilizer (micronutrients)
3. LLM_model.py - Generates comprehensive recommendation report

Author: AgriCure AI Team
Date: December 2025
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# Import primary fertilizer & pH model (rule-based)
from primary_fertilizer_pH_model import PrimaryFertilizerAndpHModel

# Import secondary fertilizer model
from secondary_fertilizer_model import SecondaryFertilizerModel

# Import LLM model components
from LLM_model import (
    InputData, 
    MLPrediction,
    generate_enhanced_recommendation,
    generate_fallback_recommendation
)


# ==================================================================================
# PRIMARY MODEL - Rule-Based Fertilizer & pH Recommendation
# ==================================================================================
# Note: We now use the rule-based PrimaryFertilizerAndpHModel instead of ML
# This provides 100% deterministic predictions based on expert agricultural rules


# ==================================================================================
# FINAL INTEGRATED MODEL
# ==================================================================================
class FinalFertilizerRecommendationSystem:
    """
    Complete Fertilizer Recommendation System
    Integrates Primary ML Model, Secondary Fertilizer Model, and LLM Model
    """
    
    def __init__(self):
        """Initialize all sub-models"""
        print("\n" + "="*80)
        print("INITIALIZING FINAL FERTILIZER RECOMMENDATION SYSTEM")
        print("="*80 + "\n")
        
        # Initialize primary fertilizer model (rule-based)
        self.primary_model = PrimaryFertilizerAndpHModel()
        
        # Initialize secondary fertilizer model
        print("\n⚙️ Initializing Secondary Fertilizer Model...")
        self.secondary_model = SecondaryFertilizerModel()
        print("✅ Secondary Fertilizer Model initialized")
        
        print("\n" + "="*80)
        print("✅ ALL MODELS INITIALIZED SUCCESSFULLY")
        print("="*80 + "\n")
    
    def predict(self, 
                size: float,
                crop: str,
                sowing_date: str,
                nitrogen: float,
                phosphorus: float,
                potassium: float,
                soil_ph: float,
                soil_moisture: float,
                electrical_conductivity: float,
                soil_temperature: float,
                use_llm: bool = True) -> Dict[str, Any]:
        """
        Generate complete fertilizer recommendation
        
        Parameters:
        -----------
        size : float
            Field size in hectares
        crop : str
            Crop type (e.g., "Wheat", "Rice", "Maize")
        sowing_date : str
            Sowing date in format YYYY-MM-DD
        nitrogen : float
            Nitrogen content in mg/kg
        phosphorus : float
            Phosphorus content in mg/kg
        potassium : float
            Potassium content in mg/kg
        soil_ph : float
            Soil pH value
        soil_moisture : float
            Soil moisture percentage
        electrical_conductivity : float
            Electrical conductivity
        soil_temperature : float
            Soil temperature in °C
        use_llm : bool
            Whether to use LLM for enhanced recommendations (default: True)
        
        Returns:
        --------
        dict: Complete recommendation report
        """
        
        print("\n" + "="*80)
        print("GENERATING FERTILIZER RECOMMENDATION")
        print("="*80)
        
        # Step 1: Get predictions from Primary ML Model
        print("\n📊 Step 1: Running Primary ML Model...")
        try:
            primary_predictions = self.primary_model.predict(
                nitrogen=nitrogen,
                phosphorus=phosphorus,
                potassium=potassium,
                crop_type=crop,
                ph=soil_ph,
                electrical_conductivity=electrical_conductivity,
                soil_moisture=soil_moisture,
                soil_temperature=soil_temperature
            )
            
            print("✅ Primary Model Predictions:")
            print(f"   - N_Status: {primary_predictions['N_Status']}")
            print(f"   - P_Status: {primary_predictions['P_Status']}")
            print(f"   - K_Status: {primary_predictions['K_Status']}")
            print(f"   - Primary_Fertilizer: {primary_predictions['Primary_Fertilizer']}")
            print(f"   - pH_Amendment: {primary_predictions['pH_Amendment']}")
            
        except Exception as e:
            print(f"❌ Error in Primary Model: {e}")
            raise
        
        # Step 2: Get predictions from Secondary Fertilizer Model
        print("\n🧪 Step 2: Running Secondary Fertilizer Model...")
        try:
            secondary_fertilizer = self.secondary_model.recommend_fertilizer(
                nitrogen=nitrogen,
                phosphorus=phosphorus,
                potassium=potassium,
                crop_type=crop,
                pH=soil_ph,
                ec=electrical_conductivity,
                moisture=soil_moisture,
                temperature=soil_temperature
            )
            
            print(f"✅ Secondary Fertilizer: {secondary_fertilizer}")
            
        except Exception as e:
            print(f"❌ Error in Secondary Model: {e}")
            secondary_fertilizer = "None"
        
        # Step 3: Prepare data for LLM Model
        print("\n🤖 Step 3: Preparing data for LLM Model...")
        
        # Create InputData object
        input_data = InputData(
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            ph=soil_ph,
            ec=electrical_conductivity,
            soil_temperature=soil_temperature,
            soil_moisture=soil_moisture,
            crop_type=crop,
            sowing_date=sowing_date,
            field_size=size
        )
        
        # Create MLPrediction object
        ml_prediction = MLPrediction(
            n_status=primary_predictions['N_Status'],
            p_status=primary_predictions['P_Status'],
            k_status=primary_predictions['K_Status'],
            primary_fertilizer=primary_predictions['Primary_Fertilizer'],
            ph_amendment=primary_predictions['pH_Amendment']
        )
        
        # Dummy confidence scores (you can add actual confidence from models if available)
        confidence_scores = {
            "N_Status": 0.90,
            "P_Status": 0.88,
            "K_Status": 0.92,
            "Primary_Fertilizer": 0.89,
            "Secondary_Fertilizer": 0.85,
            "pH_Amendment": 0.93
        }
        
        # Step 4: Generate final recommendation using LLM
        if use_llm:
            print("\n💡 Step 4: Generating Enhanced Recommendation with LLM...")
            try:
                final_recommendation = generate_enhanced_recommendation(
                    input_data=input_data,
                    ml_prediction=ml_prediction,
                    secondary_fertilizer=secondary_fertilizer,
                    confidence_scores=confidence_scores
                )
                print("✅ Enhanced recommendation generated successfully")
            except Exception as e:
                print(f"⚠️ LLM generation failed: {e}")
                print("📋 Using fallback recommendation...")
                final_recommendation = generate_fallback_recommendation(
                    input_data=input_data,
                    ml_prediction=ml_prediction,
                    secondary_fertilizer=secondary_fertilizer,
                    confidence_scores=confidence_scores
                )
        else:
            print("\n📋 Step 4: Generating Basic Recommendation (without LLM)...")
            final_recommendation = generate_fallback_recommendation(
                input_data=input_data,
                ml_prediction=ml_prediction,
                secondary_fertilizer=secondary_fertilizer,
                confidence_scores=confidence_scores
            )
        
        # Add ML predictions to the report
        final_recommendation['ml_predictions'] = {
            'N_Status': primary_predictions['N_Status'],
            'P_Status': primary_predictions['P_Status'],
            'K_Status': primary_predictions['K_Status'],
            'Primary_Fertilizer': primary_predictions['Primary_Fertilizer'],
            'Secondary_Fertilizer': secondary_fertilizer,
            'pH_Amendment': primary_predictions['pH_Amendment']
        }
        
        print("\n" + "="*80)
        print("✅ RECOMMENDATION GENERATION COMPLETE")
        print("="*80 + "\n")
        
        return final_recommendation


# ==================================================================================
# INTERACTIVE USER INPUT FUNCTION
# ==================================================================================
def get_user_input():
    """Get fertilizer recommendation inputs from user interactively"""
    
    print("\n" + "="*80)
    print("FERTILIZER RECOMMENDATION SYSTEM - USER INPUT")
    print("="*80)
    
    print("\n📝 Please enter the following information:\n")
    
    try:
        # Field and Crop Information
        print("--- Field & Crop Information ---")
        size = float(input("Field Size (hectares): "))
        crop = input("Crop Type (e.g., Wheat, Rice, Maize): ").strip()
        sowing_date = input("Sowing Date (YYYY-MM-DD): ").strip()
        
        # Soil Parameters
        print("\n--- Soil Test Parameters ---")
        nitrogen = float(input("Nitrogen (mg/kg): "))
        phosphorus = float(input("Phosphorus (mg/kg): "))
        potassium = float(input("Potassium (mg/kg): "))
        soil_ph = float(input("Soil pH: "))
        soil_moisture = float(input("Soil Moisture (%): "))
        electrical_conductivity = float(input("Electrical Conductivity: "))
        soil_temperature = float(input("Soil Temperature (°C): "))
        
        # LLM option
        print("\n--- Additional Options ---")
        use_llm_input = input("Use AI-Enhanced Recommendations? (yes/no) [default: yes]: ").strip().lower()
        use_llm = use_llm_input != 'no'
        
        return {
            'size': size,
            'crop': crop,
            'sowing_date': sowing_date,
            'nitrogen': nitrogen,
            'phosphorus': phosphorus,
            'potassium': potassium,
            'soil_ph': soil_ph,
            'soil_moisture': soil_moisture,
            'electrical_conductivity': electrical_conductivity,
            'soil_temperature': soil_temperature,
            'use_llm': use_llm
        }
        
    except ValueError as e:
        print(f"\n❌ Error: Invalid input. Please enter numeric values for all measurements.")
        print(f"Details: {e}")
        return None
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None


# ==================================================================================
# MAIN EXECUTION
# ==================================================================================
def main():
    """Main execution function"""
    
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "FINAL FERTILIZER RECOMMENDATION SYSTEM" + " "*20 + "║")
    print("║" + " "*15 + "Integrated ML + Secondary + LLM Models" + " "*16 + "║")
    print("╚" + "="*78 + "╝")
    
    # Initialize the system
    try:
        system = FinalFertilizerRecommendationSystem()
    except Exception as e:
        print(f"\n❌ Failed to initialize system: {e}")
        return
    
    # Example 1: Programmatic usage
    print("\n" + "="*80)
    print("EXAMPLE 1: PROGRAMMATIC USAGE")
    print("="*80)
    
    example_params = {
        'size': 2.5,
        'crop': 'Wheat',
        'sowing_date': '2025-11-15',
        'nitrogen': 180.0,
        'phosphorus': 25.0,
        'potassium': 150.0,
        'soil_ph': 6.8,
        'soil_moisture': 55.0,
        'electrical_conductivity': 450.0,
        'soil_temperature': 28.5,
        'use_llm': True
    }
    
    print("\n📋 Input Parameters:")
    for key, value in example_params.items():
        print(f"   {key}: {value}")
    
    try:
        recommendation = system.predict(**example_params)
        
        # Display results
        print("\n" + "="*80)
        print("RECOMMENDATION RESULTS")
        print("="*80)
        
        # Save to file
        output_file = "final_recommendation_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(recommendation, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Complete recommendation saved to: {output_file}")
        
        # Display summary
        print("\n📊 RECOMMENDATION SUMMARY:")
        print("-" * 80)
        
        if 'ml_predictions' in recommendation:
            ml_preds = recommendation['ml_predictions']
            print(f"\n🎯 ML Model Predictions:")
            print(f"   N Status: {ml_preds.get('N_Status', 'N/A')}")
            print(f"   P Status: {ml_preds.get('P_Status', 'N/A')}")
            print(f"   K Status: {ml_preds.get('K_Status', 'N/A')}")
            print(f"   Primary Fertilizer: {ml_preds.get('Primary_Fertilizer', 'N/A')}")
            print(f"   Secondary Fertilizer: {ml_preds.get('Secondary_Fertilizer', 'N/A')}")
            print(f"   pH Amendment: {ml_preds.get('pH_Amendment', 'N/A')}")
        
        if 'cost_estimate' in recommendation:
            costs = recommendation['cost_estimate']
            print(f"\n💰 Cost Estimate:")
            print(f"   Primary Fertilizer: {costs.get('primary_fertilizer', 'N/A')}")
            print(f"   Secondary Fertilizer: {costs.get('secondary_fertilizer', 'N/A')}")
            print(f"   Organic Options: {costs.get('organic_options', 'N/A')}")
            print(f"   Total: {costs.get('total_estimate', 'N/A')}")
            print(f"   Field Size: {costs.get('field_size', 'N/A')}")
        
        print("\n" + "="*80)
        
    except Exception as e:
        print(f"\n❌ Error generating recommendation: {e}")
        import traceback
        traceback.print_exc()
    
    # Example 2: Interactive mode
    print("\n" + "="*80)
    print("EXAMPLE 2: INTERACTIVE MODE")
    print("="*80)
    
    user_input = input("\nWould you like to enter your own data? (yes/no): ").strip().lower()
    
    if user_input == 'yes':
        user_params = get_user_input()
        
        if user_params:
            try:
                user_recommendation = system.predict(**user_params)
                
                # Save to file
                user_output_file = f"user_recommendation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(user_output_file, 'w', encoding='utf-8') as f:
                    json.dump(user_recommendation, f, indent=2, ensure_ascii=False)
                
                print(f"\n✅ Your recommendation saved to: {user_output_file}")
                
                # Display user results
                if 'ml_predictions' in user_recommendation:
                    ml_preds = user_recommendation['ml_predictions']
                    print(f"\n🎯 Your Recommendations:")
                    print(f"   Primary Fertilizer: {ml_preds.get('Primary_Fertilizer', 'N/A')}")
                    print(f"   Secondary Fertilizer: {ml_preds.get('Secondary_Fertilizer', 'N/A')}")
                    print(f"   pH Amendment: {ml_preds.get('pH_Amendment', 'N/A')}")
                
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
    else:
        print("\n👋 Skipping interactive mode.")
    
    print("\n" + "="*80)
    print("✅ PROGRAM COMPLETED SUCCESSFULLY")
    print("="*80 + "\n")


# ==================================================================================
# ENTRY POINT
# ==================================================================================
if __name__ == "__main__":
    main()
