"""
🌾 Fertilizer Recommendation System - Prediction Script
Use the trained model to make predictions on new soil samples
"""

import numpy as np
import pandas as pd
import pickle
import tensorflow as tf
from tensorflow import keras

def load_model_and_preprocessors():
    """Load the trained model and preprocessing objects"""
    print("📦 Loading model and preprocessing objects...")
    
    # Load the best model
    model = keras.models.load_model('best_fertilizer_model.h5')
    
    # Load preprocessing objects
    with open('preprocessing_objects.pkl', 'rb') as f:
        prep_objects = pickle.load(f)
    
    print("✓ Model and preprocessors loaded successfully!")
    return model, prep_objects

def preprocess_input(input_data, prep_objects):
    """
    Preprocess input data for prediction
    
    Parameters:
    -----------
    input_data : dict
        Dictionary containing soil and crop parameters
    prep_objects : dict
        Dictionary containing preprocessing objects (scaler, encoders)
    
    Returns:
    --------
    np.array : Scaled and encoded input ready for prediction
    """
    # Extract encoders and scaler
    scaler = prep_objects['scaler']
    le_soil = prep_objects['le_soil']
    le_crop = prep_objects['le_crop']
    
    # Encode categorical variables
    try:
        soil_encoded = le_soil.transform([input_data['Soil_Type']])[0]
    except ValueError:
        print(f"⚠️ Warning: '{input_data['Soil_Type']}' not in training data. Using 'Alluvial' as default.")
        soil_encoded = le_soil.transform(['Alluvial'])[0]
    
    try:
        crop_encoded = le_crop.transform([input_data['Crop_Type']])[0]
    except ValueError:
        print(f"⚠️ Warning: '{input_data['Crop_Type']}' not in training data. Using 'Rice' as default.")
        crop_encoded = le_crop.transform(['Rice'])[0]
    
    # Create input array
    input_array = np.array([[
        input_data['Nitrogen'],
        input_data['Phosphorus'],
        input_data['Potassium'],
        soil_encoded,
        crop_encoded,
        input_data['pH'],
        input_data['Electrical_Conductivity'],
        input_data['Soil_Moisture'],
        input_data['Soil_Temperature']
    ]])
    
    # Scale the input
    input_scaled = scaler.transform(input_array)
    
    return input_scaled

def interpret_npk_status(n_status, p_status, k_status):
    """Interpret NPK status values"""
    
    def interpret_single(value, nutrient_name):
        if value < 0.5:
            return f"✓ {nutrient_name}: Sufficient (Score: {value:.2f})"
        elif value < 10:
            return f"⚠️ {nutrient_name}: Slight deficiency (Score: {value:.2f})"
        elif value < 30:
            return f"⚠️ {nutrient_name}: Moderate deficiency (Score: {value:.2f})"
        else:
            return f"❗ {nutrient_name}: High deficiency (Score: {value:.2f})"
    
    interpretations = {
        'Nitrogen': interpret_single(n_status, 'Nitrogen'),
        'Phosphorus': interpret_single(p_status, 'Phosphorus'),
        'Potassium': interpret_single(k_status, 'Potassium')
    }
    
    return interpretations

def predict_fertilizer(input_data, model=None, prep_objects=None):
    """
    Make fertilizer recommendation prediction
    
    Parameters:
    -----------
    input_data : dict
        Dictionary with keys: Nitrogen, Phosphorus, Potassium, Soil_Type, 
        Crop_Type, pH, Electrical_Conductivity, Soil_Moisture, Soil_Temperature
    model : keras.Model (optional)
        Pre-loaded model. If None, will load from file
    prep_objects : dict (optional)
        Pre-loaded preprocessing objects. If None, will load from file
    
    Returns:
    --------
    dict : Dictionary containing all predictions and interpretations
    """
    
    # Load model and preprocessors if not provided
    if model is None or prep_objects is None:
        model, prep_objects = load_model_and_preprocessors()
    
    # Preprocess input
    input_scaled = preprocess_input(input_data, prep_objects)
    
    # Make prediction
    predictions = model.predict(input_scaled, verbose=0)
    
    # Extract predictions
    n_status = predictions[0][0][0]
    p_status = predictions[1][0][0]
    k_status = predictions[2][0][0]
    
    # Get classification predictions (top class)
    primary_idx = np.argmax(predictions[3][0])
    secondary_idx = np.argmax(predictions[4][0])
    ph_idx = np.argmax(predictions[5][0])
    
    # Get top-3 recommendations for each classification
    primary_top3_idx = np.argsort(predictions[3][0])[-3:][::-1]
    secondary_top3_idx = np.argsort(predictions[4][0])[-3:][::-1]
    ph_top3_idx = np.argsort(predictions[5][0])[-3:][::-1]
    
    # Decode predictions
    le_primary = prep_objects['le_primary']
    le_secondary = prep_objects['le_secondary']
    le_ph = prep_objects['le_ph']
    
    primary_fertilizer = le_primary.inverse_transform([primary_idx])[0]
    secondary_fertilizer = le_secondary.inverse_transform([secondary_idx])[0]
    ph_amendment = le_ph.inverse_transform([ph_idx])[0]
    
    # Get top-3 recommendations with confidence
    primary_top3 = [
        {
            'fertilizer': le_primary.inverse_transform([idx])[0],
            'confidence': predictions[3][0][idx]
        }
        for idx in primary_top3_idx
    ]
    
    secondary_top3 = [
        {
            'fertilizer': le_secondary.inverse_transform([idx])[0],
            'confidence': predictions[4][0][idx]
        }
        for idx in secondary_top3_idx
    ]
    
    ph_top3 = [
        {
            'amendment': le_ph.inverse_transform([idx])[0],
            'confidence': predictions[5][0][idx]
        }
        for idx in ph_top3_idx
    ]
    
    # Interpret NPK status
    npk_interpretations = interpret_npk_status(n_status, p_status, k_status)
    
    # Compile results
    results = {
        'input': input_data,
        'npk_status': {
            'N_Status': n_status,
            'P_Status': p_status,
            'K_Status': k_status,
            'interpretations': npk_interpretations
        },
        'recommendations': {
            'primary_fertilizer': primary_fertilizer,
            'secondary_fertilizer': secondary_fertilizer,
            'ph_amendment': ph_amendment
        },
        'top_recommendations': {
            'primary_fertilizer': primary_top3,
            'secondary_fertilizer': secondary_top3,
            'ph_amendment': ph_top3
        }
    }
    
    return results

def print_prediction_results(results):
    """Print prediction results in a formatted way"""
    
    print("\n" + "=" * 80)
    print("🌾 FERTILIZER RECOMMENDATION RESULTS")
    print("=" * 80)
    
    print("\n📥 Input Parameters:")
    for key, value in results['input'].items():
        print(f"  {key:.<30} {value}")
    
    print("\n" + "─" * 80)
    print("📊 NUTRIENT STATUS ANALYSIS")
    print("─" * 80)
    
    npk = results['npk_status']
    for nutrient, interpretation in npk['interpretations'].items():
        print(f"  {interpretation}")
    
    print("\n" + "─" * 80)
    print("💊 FERTILIZER RECOMMENDATIONS")
    print("─" * 80)
    
    rec = results['recommendations']
    print(f"\n  🥇 Primary Fertilizer:")
    print(f"     {rec['primary_fertilizer']}")
    
    print(f"\n  🥈 Secondary Fertilizer:")
    print(f"     {rec['secondary_fertilizer']}")
    
    print(f"\n  🧪 pH Amendment:")
    print(f"     {rec['ph_amendment']}")
    
    print("\n" + "─" * 80)
    print("🎯 ALTERNATIVE RECOMMENDATIONS (Top 3)")
    print("─" * 80)
    
    print(f"\n  Primary Fertilizer Options:")
    for i, option in enumerate(results['top_recommendations']['primary_fertilizer'], 1):
        print(f"    {i}. {option['fertilizer']:<50} (Confidence: {option['confidence']:.2%})")
    
    print(f"\n  Secondary Fertilizer Options:")
    for i, option in enumerate(results['top_recommendations']['secondary_fertilizer'], 1):
        print(f"    {i}. {option['fertilizer']:<50} (Confidence: {option['confidence']:.2%})")
    
    print(f"\n  pH Amendment Options:")
    for i, option in enumerate(results['top_recommendations']['ph_amendment'], 1):
        print(f"    {i}. {option['amendment']:<50} (Confidence: {option['confidence']:.2%})")
    
    print("\n" + "=" * 80)

def predict_from_csv(csv_file, output_file='predictions.csv'):
    """
    Make predictions for multiple samples from a CSV file
    
    Parameters:
    -----------
    csv_file : str
        Path to CSV file with soil samples
    output_file : str
        Path to save predictions
    """
    
    print(f"\n📂 Loading samples from: {csv_file}")
    df = pd.read_csv(csv_file)
    
    print(f"✓ Loaded {len(df)} samples")
    
    # Load model once
    model, prep_objects = load_model_and_preprocessors()
    
    # Prepare results storage
    results_list = []
    
    print("\n🔄 Processing samples...")
    for idx, row in df.iterrows():
        input_data = {
            'Nitrogen': row['Nitrogen(mg/kg)'],
            'Phosphorus': row['Phosphorus(mg/kg)'],
            'Potassium': row['Potassium(mg/kg)'],
            'Soil_Type': row['Soil_Type'],
            'Crop_Type': row['Crop_Type'],
            'pH': row['pH'],
            'Electrical_Conductivity': row['Electrical_Conductivity'],
            'Soil_Moisture': row['Soil_Moisture'],
            'Soil_Temperature': row['Soil_Temperture']
        }
        
        result = predict_fertilizer(input_data, model, prep_objects)
        
        # Extract for CSV
        results_list.append({
            'Sample_ID': idx + 1,
            'Nitrogen': input_data['Nitrogen'],
            'Phosphorus': input_data['Phosphorus'],
            'Potassium': input_data['Potassium'],
            'Soil_Type': input_data['Soil_Type'],
            'Crop_Type': input_data['Crop_Type'],
            'pH': input_data['pH'],
            'EC': input_data['Electrical_Conductivity'],
            'Moisture': input_data['Soil_Moisture'],
            'Temperature': input_data['Soil_Temperature'],
            'Predicted_N_Status': result['npk_status']['N_Status'],
            'Predicted_P_Status': result['npk_status']['P_Status'],
            'Predicted_K_Status': result['npk_status']['K_Status'],
            'Primary_Fertilizer': result['recommendations']['primary_fertilizer'],
            'Secondary_Fertilizer': result['recommendations']['secondary_fertilizer'],
            'pH_Amendment': result['recommendations']['ph_amendment']
        })
        
        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1}/{len(df)} samples...")
    
    # Save to CSV
    results_df = pd.DataFrame(results_list)
    results_df.to_csv(output_file, index=False)
    
    print(f"\n✓ Predictions saved to: {output_file}")
    print(f"✓ Total samples processed: {len(results_df)}")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    
    print("=" * 80)
    print("🌾 FERTILIZER RECOMMENDATION SYSTEM - PREDICTION")
    print("=" * 80)
    
    # Example 1: Single Prediction (from specification)
    print("\n📝 Example 1: Single Prediction")
    
    sample_input = {
        'Nitrogen': 5,
        'Phosphorus': 10,
        'Potassium': 130,
        'Soil_Type': 'Sandy',
        'Crop_Type': 'Rice',
        'pH': 5.2,
        'Electrical_Conductivity': 300,
        'Soil_Moisture': 15,
        'Soil_Temperature': 29
    }
    
    results = predict_fertilizer(sample_input)
    print_prediction_results(results)
    
    # Example 2: Another sample
    print("\n\n📝 Example 2: Different Sample")
    
    sample_input_2 = {
        'Nitrogen': 150,
        'Phosphorus': 40,
        'Potassium': 200,
        'Soil_Type': 'Alluvial',
        'Crop_Type': 'Wheat',
        'pH': 7.5,
        'Electrical_Conductivity': 800,
        'Soil_Moisture': 25,
        'Soil_Temperature': 28
    }
    
    results_2 = predict_fertilizer(sample_input_2)
    print_prediction_results(results_2)
    
    print("\n\n💡 Usage Tips:")
    print("  1. For single predictions: Call predict_fertilizer(input_data)")
    print("  2. For batch predictions: Call predict_from_csv('your_file.csv')")
    print("  3. Required inputs: N, P, K, Soil_Type, Crop_Type, pH, EC, Moisture, Temperature")
    
    print("\n✅ Prediction script ready!")
    print("=" * 80)
