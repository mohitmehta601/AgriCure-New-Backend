"""
Fertilizer Recommendation ML Model
Uses Random Forest, XGBoost, CatBoost, and LightGBM with 5-fold Cross-Validation and OOF Predictions
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
import xgboost as xgb
from catboost import CatBoostClassifier
import lightgbm as lgb
import warnings
warnings.filterwarnings('ignore')

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('Primary and pH Dataset.csv')
print(f"Dataset shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nFirst few rows:")
print(df.head())

# Separate features and targets
# For Primary_Fertilizer: use only 4 features (removed Soil_Type)
feature_cols_primary = ['Nitrogen(mg/kg)', 'Phosphorus(mg/kg)', 'Potassium(mg/kg)', 
                        'Crop_Type']

# For other targets (N_Status, P_Status, K_Status, pH_Amendment): use all 8 features (removed Soil_Type)
feature_cols_all = ['Nitrogen(mg/kg)', 'Phosphorus(mg/kg)', 'Potassium(mg/kg)', 
                    'Crop_Type', 'pH', 'Electrical_Conductivity', 
                    'Soil_Moisture', 'Soil_Temperture']

target_cols = ['N_Status', 'P_Status', 'K_Status', 'Primary_Fertilizer', 'pH_Amendment']

# Define which features to use for each target
target_feature_mapping = {
    'Primary_Fertilizer': feature_cols_primary,
    'N_Status': feature_cols_all,
    'P_Status': feature_cols_all,
    'K_Status': feature_cols_all,
    'pH_Amendment': feature_cols_all
}

y = df[target_cols].copy()

print(f"\nPrimary_Fertilizer features (4): {feature_cols_primary}")
print(f"Other targets features (8): {feature_cols_all}")
print(f"Targets: {target_cols}")

# Identify categorical columns (removed Soil_Type)
categorical_features = ['Crop_Type']

# Prepare encoded versions for all features
X_all = df[feature_cols_all].copy()
X_primary = df[feature_cols_primary].copy()

X_all_encoded = X_all.copy()
X_primary_encoded = X_primary.copy()
label_encoders_features = {}

for col in categorical_features:
    le = LabelEncoder()
    le.fit(df[col])  # Fit on all data
    X_all_encoded[col] = le.transform(X_all[col])
    X_primary_encoded[col] = le.transform(X_primary[col])
    label_encoders_features[col] = le

print(f"\nCategorical features: {categorical_features}")

# Encode target variables
label_encoders_targets = {}
y_encoded = y.copy()

for col in target_cols:
    le = LabelEncoder()
    y_encoded[col] = le.fit_transform(y[col])
    label_encoders_targets[col] = le
    print(f"\n{col} classes ({len(le.classes_)}): {le.classes_[:10]}...")  # Show first 10

# Initialize 5-fold cross-validation
n_splits = 5
skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

# Store OOF predictions and model performance
oof_predictions = {target: {} for target in target_cols}
model_scores = {target: {} for target in target_cols}
trained_models = {target: {} for target in target_cols}

print("\n" + "="*80)
print("TRAINING MULTI-OUTPUT MODELS WITH 5-FOLD CROSS-VALIDATION")
print("="*80)

# Train separate models for each target variable
for target in target_cols:
    print(f"\n{'='*80}")
    print(f"TARGET: {target}")
    print(f"{'='*80}")
    
    # Select appropriate features for this target
    if target == 'Primary_Fertilizer':
        X_use = X_primary
        X_use_encoded = X_primary_encoded
        print(f"Using 5 features: {feature_cols_primary}")
    else:
        X_use = X_all
        X_use_encoded = X_all_encoded
        print(f"Using 9 features: {feature_cols_all}")
    
    y_target = y_encoded[target].values
    n_classes = len(np.unique(y_target))
    
    # Initialize OOF prediction arrays for each model
    oof_rf = np.zeros(len(X_use))
    oof_xgb = np.zeros(len(X_use))
    oof_cat = np.zeros(len(X_use))
    oof_lgb = np.zeros(len(X_use))
    
    # Store fold scores
    fold_scores = {'rf': [], 'xgb': [], 'cat': [], 'lgb': []}
    
    # Store trained models for each fold
    models_rf = []
    models_xgb = []
    models_cat = []
    models_lgb = []
    
    # 5-Fold Cross-Validation
    for fold, (train_idx, val_idx) in enumerate(skf.split(X_use_encoded, y_target), 1):
        print(f"\n--- Fold {fold}/{n_splits} ---")
        
        X_train, X_val = X_use_encoded.iloc[train_idx], X_use_encoded.iloc[val_idx]
        y_train, y_val = y_target[train_idx], y_target[val_idx]
        
        # Get original categorical data for CatBoost
        X_train_cat = X_use.iloc[train_idx].copy()
        X_val_cat = X_use.iloc[val_idx].copy()
        
        # ===== Random Forest =====
        print("Training Random Forest...")
        rf_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'
        )
        rf_model.fit(X_train, y_train)
        rf_pred = rf_model.predict(X_val)
        rf_score = accuracy_score(y_val, rf_pred)
        fold_scores['rf'].append(rf_score)
        oof_rf[val_idx] = rf_pred
        models_rf.append(rf_model)
        print(f"  RF Accuracy: {rf_score:.4f}")
        
        # ===== XGBoost =====
        print("Training XGBoost...")
        xgb_model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=10,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            eval_metric='mlogloss' if n_classes > 2 else 'logloss'
        )
        xgb_model.fit(X_train, y_train, verbose=False)
        xgb_pred = xgb_model.predict(X_val)
        xgb_score = accuracy_score(y_val, xgb_pred)
        fold_scores['xgb'].append(xgb_score)
        oof_xgb[val_idx] = xgb_pred
        models_xgb.append(xgb_model)
        print(f"  XGB Accuracy: {xgb_score:.4f}")
        
        # ===== CatBoost =====
        print("Training CatBoost...")
        cat_model = CatBoostClassifier(
            iterations=200,
            depth=10,
            learning_rate=0.1,
            random_state=42,
            verbose=False,
            cat_features=categorical_features
        )
        cat_model.fit(X_train_cat, y_train)
        cat_pred = cat_model.predict(X_val_cat).flatten().astype(int)
        cat_score = accuracy_score(y_val, cat_pred)
        fold_scores['cat'].append(cat_score)
        oof_cat[val_idx] = cat_pred
        models_cat.append(cat_model)
        print(f"  CAT Accuracy: {cat_score:.4f}")
        
        # ===== LightGBM =====
        print("Training LightGBM...")
        lgb_model = lgb.LGBMClassifier(
            n_estimators=200,
            max_depth=10,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            verbose=-1
        )
        lgb_model.fit(X_train, y_train)
        lgb_pred = lgb_model.predict(X_val)
        lgb_score = accuracy_score(y_val, lgb_pred)
        fold_scores['lgb'].append(lgb_score)
        oof_lgb[val_idx] = lgb_pred
        models_lgb.append(lgb_model)
        print(f"  LGB Accuracy: {lgb_score:.4f}")
    
    # Store OOF predictions
    oof_predictions[target]['rf'] = oof_rf
    oof_predictions[target]['xgb'] = oof_xgb
    oof_predictions[target]['cat'] = oof_cat
    oof_predictions[target]['lgb'] = oof_lgb
    
    # Store trained models
    trained_models[target]['rf'] = models_rf
    trained_models[target]['xgb'] = models_xgb
    trained_models[target]['cat'] = models_cat
    trained_models[target]['lgb'] = models_lgb
    
    # Calculate and store average scores
    print(f"\n--- {target} - Cross-Validation Results ---")
    for model_name in ['rf', 'xgb', 'cat', 'lgb']:
        mean_score = np.mean(fold_scores[model_name])
        std_score = np.std(fold_scores[model_name])
        model_scores[target][model_name] = {
            'mean': mean_score,
            'std': std_score,
            'folds': fold_scores[model_name]
        }
        print(f"{model_name.upper():6s}: {mean_score:.4f} (+/- {std_score:.4f})")
    
    # Ensemble predictions (voting)
    ensemble_pred = np.round((oof_rf + oof_xgb + oof_cat + oof_lgb) / 4).astype(int)
    ensemble_score = accuracy_score(y_target, ensemble_pred)
    model_scores[target]['ensemble'] = {'mean': ensemble_score}
    oof_predictions[target]['ensemble'] = ensemble_pred
    print(f"ENSEMBLE: {ensemble_score:.4f}")

# ===== OVERALL PERFORMANCE SUMMARY =====
print("\n" + "="*80)
print("OVERALL PERFORMANCE SUMMARY")
print("="*80)

summary_data = []
for target in target_cols:
    for model_name in ['rf', 'xgb', 'cat', 'lgb', 'ensemble']:
        if model_name == 'ensemble':
            score = model_scores[target][model_name]['mean']
            summary_data.append({
                'Target': target,
                'Model': model_name.upper(),
                'Mean_Accuracy': f"{score:.4f}",
                'Std_Dev': 'N/A'
            })
        else:
            mean = model_scores[target][model_name]['mean']
            std = model_scores[target][model_name]['std']
            summary_data.append({
                'Target': target,
                'Model': model_name.upper(),
                'Mean_Accuracy': f"{mean:.4f}",
                'Std_Dev': f"{std:.4f}"
            })

summary_df = pd.DataFrame(summary_data)
print("\n", summary_df.to_string(index=False))

# ===== DETAILED EVALUATION FOR EACH TARGET =====
print("\n" + "="*80)
print("DETAILED EVALUATION METRICS")
print("="*80)

for target in target_cols:
    print(f"\n{'='*80}")
    print(f"TARGET: {target}")
    print(f"{'='*80}")
    
    y_true = y_encoded[target].values
    
    for model_name in ['rf', 'xgb', 'cat', 'lgb', 'ensemble']:
        print(f"\n--- {model_name.upper()} Model ---")
        y_pred = oof_predictions[target][model_name].astype(int)
        
        # Accuracy
        acc = accuracy_score(y_true, y_pred)
        print(f"Accuracy: {acc:.4f}")
        
        # F1 Score
        f1_macro = f1_score(y_true, y_pred, average='macro', zero_division=0)
        f1_weighted = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        print(f"F1-Score (Macro): {f1_macro:.4f}")
        print(f"F1-Score (Weighted): {f1_weighted:.4f}")
        
        # Classification Report
        print("\nClassification Report:")
        labels = sorted(np.unique(y_true))
        target_names = [label_encoders_targets[target].inverse_transform([i])[0] for i in labels]
        print(classification_report(y_true, y_pred, labels=labels, target_names=target_names, zero_division=0))

# ===== SAVE RESULTS =====
print("\n" + "="*80)
print("SAVING RESULTS")
print("="*80)

# Save OOF predictions
oof_df = pd.DataFrame()
for target in target_cols:
    for model_name in ['rf', 'xgb', 'cat', 'lgb', 'ensemble']:
        oof_df[f'{target}_{model_name}'] = oof_predictions[target][model_name]

oof_df.to_csv('oof_predictions.csv', index=False)
print("✓ OOF predictions saved to 'oof_predictions.csv'")

# Save model performance summary
summary_df.to_csv('model_performance_summary.csv', index=False)
print("✓ Model performance summary saved to 'model_performance_summary.csv'")

# Save detailed scores
import json
with open('detailed_scores.json', 'w') as f:
    json.dump(model_scores, f, indent=2)
print("✓ Detailed scores saved to 'detailed_scores.json'")

print("\n" + "="*80)
print("TRAINING COMPLETED SUCCESSFULLY!")
print("="*80)

# ===== PREDICTION FUNCTION =====
def predict_fertilizer(nitrogen, phosphorus, potassium, crop_type, 
                       ph=None, electrical_conductivity=None, soil_moisture=None, soil_temperature=None):
    """
    Predict fertilizer recommendations for given input parameters
    
    Args:
        nitrogen: Nitrogen level in mg/kg
        phosphorus: Phosphorus level in mg/kg
        potassium: Potassium level in mg/kg
        crop_type: Type of crop (e.g., 'Wheat', 'Rice', 'Maize', etc.)
        ph: pH level (optional, required for N_Status, P_Status, K_Status, pH_Amendment)
        electrical_conductivity: EC value (optional, required for other targets)
        soil_moisture: Soil moisture % (optional, required for other targets)
        soil_temperature: Soil temperature (optional, required for other targets)
    
    Returns:
        Dictionary with predictions from all models and ensemble for each target
    """
    # Create input dataframe for Primary_Fertilizer (4 features, removed Soil_Type)
    input_data_primary = pd.DataFrame({
        'Nitrogen(mg/kg)': [nitrogen],
        'Phosphorus(mg/kg)': [phosphorus],
        'Potassium(mg/kg)': [potassium],
        'Crop_Type': [crop_type]
    })
    
    # Create input dataframe for other targets (8 features, removed Soil_Type) if all params provided
    input_data_all = None
    if all(v is not None for v in [ph, electrical_conductivity, soil_moisture, soil_temperature]):
        input_data_all = pd.DataFrame({
            'Nitrogen(mg/kg)': [nitrogen],
            'Phosphorus(mg/kg)': [phosphorus],
            'Potassium(mg/kg)': [potassium],
            'Crop_Type': [crop_type],
            'pH': [ph],
            'Electrical_Conductivity': [electrical_conductivity],
            'Soil_Moisture': [soil_moisture],
            'Soil_Temperture': [soil_temperature]
        })
    
    # Encode for non-CatBoost models
    input_primary_encoded = input_data_primary.copy()
    for col in categorical_features:
        input_primary_encoded[col] = label_encoders_features[col].transform(input_data_primary[col])
    
    if input_data_all is not None:
        input_all_encoded = input_data_all.copy()
        for col in categorical_features:
            input_all_encoded[col] = label_encoders_features[col].transform(input_data_all[col])
    
    results = {}
    
    for target in target_cols:
        # Skip targets that need all 9 features if not all params provided
        if target != 'Primary_Fertilizer' and input_data_all is None:
            continue
            
        target_results = {}
        
        # Select appropriate input data
        if target == 'Primary_Fertilizer':
            input_for_pred = input_data_primary
            input_for_pred_encoded = input_primary_encoded
        else:
            input_for_pred = input_data_all
            input_for_pred_encoded = input_all_encoded
        
        # Get predictions from all folds and average
        for model_type in ['rf', 'xgb', 'cat', 'lgb']:
            fold_predictions = []
            
            for i, model in enumerate(trained_models[target][model_type]):
                if model_type == 'cat':
                    pred = model.predict(input_for_pred)[0]
                else:
                    pred = model.predict(input_for_pred_encoded)[0]
                fold_predictions.append(pred)
            
            # Average prediction across folds (majority vote)
            avg_pred = int(np.round(np.mean(fold_predictions)))
            pred_label = label_encoders_targets[target].inverse_transform([avg_pred])[0]
            target_results[model_type] = pred_label
        
        # Ensemble (majority vote across models)
        all_preds = [target_results['rf'], target_results['xgb'], 
                     target_results['cat'], target_results['lgb']]
        ensemble_pred = max(set(all_preds), key=all_preds.count)
        target_results['ensemble'] = ensemble_pred
        
        results[target] = target_results
    
    return results

# ===== EXAMPLE PREDICTION =====
print("\n" + "="*80)
print("EXAMPLE PREDICTION")
print("="*80)

# Example 1: Primary_Fertilizer only (4 features, removed Soil_Type)
print("\n--- Example 1: Primary Fertilizer Only (4 features) ---")
example_input_primary = {
    'nitrogen': 126.39,
    'phosphorus': 7.18,
    'potassium': 181.53,
    'crop_type': 'Barley'
}

print("\nInput Parameters:")
for key, value in example_input_primary.items():
    print(f"  {key}: {value}")

predictions_primary = predict_fertilizer(**example_input_primary)

print("\nPredictions:")
for target, preds in predictions_primary.items():
    print(f"\n{target}:")
    for model, pred in preds.items():
        print(f"  {model.upper():10s}: {pred}")

# Example 2: All targets (8 features, removed Soil_Type)
print("\n\n--- Example 2: All Predictions (8 features) ---")
example_input_all = {
    'nitrogen': 126.39,
    'phosphorus': 7.18,
    'potassium': 181.53,
    'crop_type': 'Barley',
    'ph': 7.11,
    'electrical_conductivity': 743.8,
    'soil_moisture': 18.99,
    'soil_temperature': 30.13
}

print("\nInput Parameters:")
for key, value in example_input_all.items():
    print(f"  {key}: {value}")

predictions_all = predict_fertilizer(**example_input_all)

print("\nPredictions:")
for target, preds in predictions_all.items():
    print(f"\n{target}:")
    for model, pred in preds.items():
        print(f"  {model.upper():10s}: {pred}")

print("\n" + "="*80)
print("ALL OPERATIONS COMPLETED!")
print("="*80)
