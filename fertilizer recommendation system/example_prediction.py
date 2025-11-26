"""
Example: Using the Trained Multi-Output Stacking Model
======================================================

This script demonstrates how to load the trained model and make predictions
on new agricultural data for fertilizer recommendations.

Author: AI ML Engineer
Date: November 2025
"""

import pandas as pd
import numpy as np
from pathlib import Path
from multioutput_stacking_fertilizer import MultiOutputOOFStacker


def create_sample_data():
    """
    Create sample agricultural data for demonstration.
    
    Returns:
        DataFrame with sample input features
    """
    sample_data = pd.DataFrame({
        'Temperature': [30.5, 25.0, 35.2, 22.8, 28.5],
        'Humidity': [65.0, 75.0, 45.0, 80.0, 60.0],
        'Moisture': [45.0, 60.0, 30.0, 70.0, 50.0],
        'Soil_Type': ['Alluvial', 'Black', 'Red', 'Clayey', 'Laterite'],
        'Crop': ['rice', 'wheat', 'cotton', 'maize', 'sugarcane'],
        'Nitrogen': [75, 60, 85, 50, 70],
        'Phosphorus': [50, 45, 60, 40, 55],
        'Potassium': [60, 55, 65, 45, 58],
        'pH': [6.8, 7.2, 6.5, 7.0, 6.9],
        'EC(mmhos/cm2)': [1.2, 0.9, 1.5, 1.1, 1.0]
    })
    
    return sample_data


def display_predictions(sample_data, predictions):
    """
    Display predictions in a user-friendly format.
    
    Args:
        sample_data: Input dataframe
        predictions: Dictionary of predictions
    """
    print("\n" + "="*100)
    print("FERTILIZER RECOMMENDATIONS")
    print("="*100)
    
    for idx in range(len(sample_data)):
        print(f"\n{'─'*100}")
        print(f"Sample {idx + 1}:")
        print(f"{'─'*100}")
        
        # Input conditions
        print("\n📊 Input Conditions:")
        print(f"  • Crop: {sample_data.iloc[idx]['Crop']}")
        print(f"  • Soil Type: {sample_data.iloc[idx]['Soil_Type']}")
        print(f"  • Temperature: {sample_data.iloc[idx]['Temperature']}°C")
        print(f"  • Humidity: {sample_data.iloc[idx]['Humidity']}%")
        print(f"  • Moisture: {sample_data.iloc[idx]['Moisture']}%")
        print(f"  • pH: {sample_data.iloc[idx]['pH']}")
        print(f"  • EC: {sample_data.iloc[idx]['EC(mmhos/cm2)']} mmhos/cm²")
        
        # Nutrient levels
        print("\n🌱 Current Nutrient Levels:")
        print(f"  • Nitrogen (N): {sample_data.iloc[idx]['Nitrogen']} kg/ha")
        print(f"  • Phosphorus (P): {sample_data.iloc[idx]['Phosphorus']} kg/ha")
        print(f"  • Potassium (K): {sample_data.iloc[idx]['Potassium']} kg/ha")
        
        # Predictions
        print("\n🎯 AI Recommendations:")
        print(f"  • N Status: {predictions['N_Status'][idx]}")
        print(f"  • P Status: {predictions['P_Status'][idx]}")
        print(f"  • K Status: {predictions['K_Status'][idx]}")
        print(f"\n💊 Fertilizer Recommendations:")
        print(f"  • Primary: {predictions['Primary_Fertilizer'][idx]}")
        print(f"  • Secondary: {predictions['Secondary_Fertilizer'][idx]}")
        print(f"  • pH Amendment: {predictions['pH_Amendment'][idx]}")
    
    print("\n" + "="*100)


def main():
    """
    Main execution function for demonstration.
    """
    print("\n" + "="*100)
    print("FERTILIZER RECOMMENDATION SYSTEM - PREDICTION DEMO")
    print("="*100)
    
    # Check if model exists
    model_path = Path(__file__).parent / "stacked_model.pkl"
    
    if not model_path.exists():
        print("\n❌ Error: Model file 'stacked_model.pkl' not found!")
        print("Please run 'multioutput_stacking_fertilizer.py' first to train the model.")
        return
    
    # Load the trained model
    print("\n📦 Loading trained model...")
    try:
        model = MultiOutputOOFStacker.load(model_path)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # Create sample data
    print("\n🌾 Creating sample agricultural data...")
    sample_data = create_sample_data()
    print(f"✅ Created {len(sample_data)} sample records")
    
    # Make predictions
    print("\n🔮 Making predictions...")
    try:
        predictions = model.predict(sample_data)
        print("✅ Predictions completed!")
    except Exception as e:
        print(f"❌ Error making predictions: {e}")
        return
    
    # Display results
    display_predictions(sample_data, predictions)
    
    # Save predictions to CSV
    output_path = Path(__file__).parent / "predictions_output.csv"
    print(f"\n💾 Saving predictions to: {output_path}")
    
    # Combine input and predictions
    output_df = sample_data.copy()
    for target_col, pred_values in predictions.items():
        output_df[f'Predicted_{target_col}'] = pred_values
    
    output_df.to_csv(output_path, index=False)
    print("✅ Predictions saved successfully!")
    
    print("\n" + "="*100)
    print("Demo completed successfully!")
    print("="*100)


if __name__ == "__main__":
    main()
