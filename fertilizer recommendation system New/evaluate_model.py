"""
📊 Model Evaluation and Analysis Script
Detailed analysis of the trained fertilizer recommendation model
"""

import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    accuracy_score, f1_score, precision_score, recall_score,
    classification_report, confusion_matrix
)
from tensorflow import keras
import warnings
warnings.filterwarnings('ignore')

def load_model_and_data():
    """Load the trained model, preprocessing objects, and test data"""
    print("📦 Loading model and data...")
    
    # Load model
    model = keras.models.load_model('best_fertilizer_model.h5')
    
    # Load preprocessing objects
    with open('preprocessing_objects.pkl', 'rb') as f:
        prep_objects = pickle.load(f)
    
    # Load dataset
    df = pd.read_csv('Final AgriCure Dataset.csv')
    
    print("✓ All resources loaded successfully!")
    return model, prep_objects, df

def evaluate_regression_performance(y_true, y_pred, task_name):
    """Evaluate regression task performance"""
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    # Calculate residuals
    residuals = y_true - y_pred
    
    results = {
        'task': task_name,
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'residuals': residuals.flatten(),
        'predictions': y_pred.flatten(),
        'actual': y_true.flatten()
    }
    
    return results

def evaluate_classification_performance(y_true, y_pred_proba, task_name, label_encoder):
    """Evaluate classification task performance"""
    
    # Get predicted classes
    y_pred = np.argmax(y_pred_proba, axis=1)
    
    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='macro', zero_division=0)
    recall = recall_score(y_true, y_pred, average='macro', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
    
    # Top-3 accuracy
    top3_accuracy = np.mean([
        y_true[i] in np.argsort(y_pred_proba[i])[-3:]
        for i in range(len(y_true))
    ])
    
    # Classification report
    class_report = classification_report(
        y_true, y_pred,
        target_names=label_encoder.classes_,
        zero_division=0,
        output_dict=True
    )
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    results = {
        'task': task_name,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'top3_accuracy': top3_accuracy,
        'classification_report': class_report,
        'confusion_matrix': cm,
        'predictions': y_pred,
        'actual': y_true,
        'probabilities': y_pred_proba
    }
    
    return results

def generate_detailed_report(model, prep_objects, df):
    """Generate comprehensive evaluation report"""
    
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE MODEL EVALUATION REPORT")
    print("=" * 80)
    
    # Prepare data (same as training script)
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import MinMaxScaler
    
    # Encode features
    df['Soil_Type_Encoded'] = prep_objects['le_soil'].transform(df['Soil_Type'])
    df['Crop_Type_Encoded'] = prep_objects['le_crop'].transform(df['Crop_Type'])
    df['Primary_Fertilizer_Encoded'] = prep_objects['le_primary'].transform(df['Primary_Fertilizer'])
    df['Secondary_Fertilizer_Encoded'] = prep_objects['le_secondary'].transform(df['Secondary_Fertilizer'])
    df['pH_Amendment_Encoded'] = prep_objects['le_ph'].transform(df['pH_Amendment'])
    
    # Prepare features
    X = df[['Nitrogen(mg/kg)', 'Phosphorus(mg/kg)', 'Potassium(mg/kg)', 
            'Soil_Type_Encoded', 'Crop_Type_Encoded', 'pH', 
            'Electrical_Conductivity', 'Soil_Moisture', 'Soil_Temperture']].values
    
    X_scaled = prep_objects['scaler'].transform(X)
    
    # Prepare targets
    y_n = df['N_Status'].values.reshape(-1, 1)
    y_p = df['P_Status'].values.reshape(-1, 1)
    y_k = df['K_Status'].values.reshape(-1, 1)
    y_prim = df['Primary_Fertilizer_Encoded'].values
    y_sec = df['Secondary_Fertilizer_Encoded'].values
    y_ph = df['pH_Amendment_Encoded'].values
    
    # Split data (same split as training)
    X_train, X_temp, y_n_train, y_n_temp, y_p_train, y_p_temp, y_k_train, y_k_temp, \
    y_prim_train, y_prim_temp, y_sec_train, y_sec_temp, y_ph_train, y_ph_temp = train_test_split(
        X_scaled, y_n, y_p, y_k, y_prim, y_sec, y_ph,
        test_size=0.2, random_state=42
    )
    
    X_val, X_test, y_n_val, y_n_test, y_p_val, y_p_test, y_k_val, y_k_test, \
    y_prim_val, y_prim_test, y_sec_val, y_sec_test, y_ph_val, y_ph_test = train_test_split(
        X_temp, y_n_temp, y_p_temp, y_k_temp, y_prim_temp, y_sec_temp, y_ph_temp,
        test_size=0.5, random_state=42
    )
    
    # Make predictions
    print("\n🔮 Making predictions on test set...")
    predictions = model.predict(X_test, verbose=0)
    
    # Evaluate regression tasks
    print("\n" + "─" * 80)
    print("📈 REGRESSION PERFORMANCE (NPK Status)")
    print("─" * 80)
    
    n_results = evaluate_regression_performance(y_n_test, predictions[0], 'N_Status')
    p_results = evaluate_regression_performance(y_p_test, predictions[1], 'P_Status')
    k_results = evaluate_regression_performance(y_k_test, predictions[2], 'K_Status')
    
    # Print regression results
    for results in [n_results, p_results, k_results]:
        print(f"\n{results['task']}:")
        print(f"  RMSE:     {results['rmse']:.4f}")
        print(f"  MAE:      {results['mae']:.4f}")
        print(f"  R² Score: {results['r2']:.4f}")
    
    # Evaluate classification tasks
    print("\n" + "─" * 80)
    print("📈 CLASSIFICATION PERFORMANCE (Fertilizer Recommendations)")
    print("─" * 80)
    
    prim_results = evaluate_classification_performance(
        y_prim_test, predictions[3], 'Primary_Fertilizer', prep_objects['le_primary']
    )
    sec_results = evaluate_classification_performance(
        y_sec_test, predictions[4], 'Secondary_Fertilizer', prep_objects['le_secondary']
    )
    ph_results = evaluate_classification_performance(
        y_ph_test, predictions[5], 'pH_Amendment', prep_objects['le_ph']
    )
    
    # Print classification results
    for results in [prim_results, sec_results, ph_results]:
        print(f"\n{results['task']}:")
        print(f"  Accuracy:      {results['accuracy']:.4f} ({results['accuracy']*100:.2f}%)")
        print(f"  Precision:     {results['precision']:.4f}")
        print(f"  Recall:        {results['recall']:.4f}")
        print(f"  F1-Score:      {results['f1']:.4f}")
        print(f"  Top-3 Accuracy: {results['top3_accuracy']:.4f} ({results['top3_accuracy']*100:.2f}%)")
    
    # Overall summary
    print("\n" + "=" * 80)
    print("📊 OVERALL MODEL PERFORMANCE SUMMARY")
    print("=" * 80)
    
    avg_rmse = (n_results['rmse'] + p_results['rmse'] + k_results['rmse']) / 3
    avg_mae = (n_results['mae'] + p_results['mae'] + k_results['mae']) / 3
    avg_r2 = (n_results['r2'] + p_results['r2'] + k_results['r2']) / 3
    
    avg_acc = (prim_results['accuracy'] + sec_results['accuracy'] + ph_results['accuracy']) / 3
    avg_f1 = (prim_results['f1'] + sec_results['f1'] + ph_results['f1']) / 3
    
    print("\n🔹 Regression Tasks (NPK Status):")
    print(f"  Average RMSE:     {avg_rmse:.4f}")
    print(f"  Average MAE:      {avg_mae:.4f}")
    print(f"  Average R²:       {avg_r2:.4f}")
    
    print("\n🔹 Classification Tasks (Fertilizer Recommendations):")
    print(f"  Average Accuracy: {avg_acc:.4f} ({avg_acc*100:.2f}%)")
    print(f"  Average F1-Score: {avg_f1:.4f}")
    
    # Save detailed results
    results_dict = {
        'regression': {
            'n_status': n_results,
            'p_status': p_results,
            'k_status': k_results
        },
        'classification': {
            'primary_fertilizer': prim_results,
            'secondary_fertilizer': sec_results,
            'ph_amendment': ph_results
        },
        'summary': {
            'avg_rmse': avg_rmse,
            'avg_mae': avg_mae,
            'avg_r2': avg_r2,
            'avg_accuracy': avg_acc,
            'avg_f1': avg_f1
        }
    }
    
    return results_dict

def plot_feature_importance_analysis(df, prep_objects):
    """Analyze and visualize feature distributions by crop and soil type"""
    
    print("\n" + "=" * 80)
    print("📊 FEATURE IMPORTANCE ANALYSIS")
    print("=" * 80)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Feature Analysis by Crop and Soil Type', fontsize=16, fontweight='bold')
    
    # NPK by Crop Type
    crop_npk = df.groupby('Crop_Type')[['Nitrogen(mg/kg)', 'Phosphorus(mg/kg)', 'Potassium(mg/kg)']].mean()
    crop_npk.plot(kind='bar', ax=axes[0, 0], rot=45)
    axes[0, 0].set_title('Average NPK Levels by Crop Type')
    axes[0, 0].set_ylabel('mg/kg')
    axes[0, 0].legend(['Nitrogen', 'Phosphorus', 'Potassium'])
    axes[0, 0].grid(True, alpha=0.3)
    
    # NPK by Soil Type
    soil_npk = df.groupby('Soil_Type')[['Nitrogen(mg/kg)', 'Phosphorus(mg/kg)', 'Potassium(mg/kg)']].mean()
    soil_npk.plot(kind='bar', ax=axes[0, 1], rot=45)
    axes[0, 1].set_title('Average NPK Levels by Soil Type')
    axes[0, 1].set_ylabel('mg/kg')
    axes[0, 1].legend(['Nitrogen', 'Phosphorus', 'Potassium'])
    axes[0, 1].grid(True, alpha=0.3)
    
    # pH distribution by Soil Type
    df.boxplot(column='pH', by='Soil_Type', ax=axes[1, 0], rot=45)
    axes[1, 0].set_title('pH Distribution by Soil Type')
    axes[1, 0].set_ylabel('pH')
    axes[1, 0].set_xlabel('Soil Type')
    plt.setp(axes[1, 0].get_xticklabels(), rotation=45, ha='right')
    
    # EC distribution by Crop Type
    df.boxplot(column='Electrical_Conductivity', by='Crop_Type', ax=axes[1, 1], rot=45)
    axes[1, 1].set_title('Electrical Conductivity by Crop Type')
    axes[1, 1].set_ylabel('EC (μS/cm)')
    axes[1, 1].set_xlabel('Crop Type')
    plt.setp(axes[1, 1].get_xticklabels(), rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig('feature_analysis.png', dpi=300, bbox_inches='tight')
    print("\n✓ Feature analysis plot saved: feature_analysis.png")
    plt.close()

def generate_performance_comparison_chart(results_dict):
    """Create a comprehensive performance comparison chart"""
    
    print("\n📊 Creating performance comparison charts...")
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')
    
    # Regression metrics comparison
    reg_tasks = ['N_Status', 'P_Status', 'K_Status']
    rmse_values = [
        results_dict['regression']['n_status']['rmse'],
        results_dict['regression']['p_status']['rmse'],
        results_dict['regression']['k_status']['rmse']
    ]
    r2_values = [
        results_dict['regression']['n_status']['r2'],
        results_dict['regression']['p_status']['r2'],
        results_dict['regression']['k_status']['r2']
    ]
    
    x = np.arange(len(reg_tasks))
    width = 0.35
    
    ax1 = axes[0]
    ax1_twin = ax1.twinx()
    
    bars1 = ax1.bar(x - width/2, rmse_values, width, label='RMSE', color='steelblue')
    bars2 = ax1_twin.bar(x + width/2, r2_values, width, label='R² Score', color='orange')
    
    ax1.set_xlabel('Task')
    ax1.set_ylabel('RMSE', color='steelblue')
    ax1_twin.set_ylabel('R² Score', color='orange')
    ax1.set_title('Regression Performance')
    ax1.set_xticks(x)
    ax1.set_xticklabels(reg_tasks)
    ax1.tick_params(axis='y', labelcolor='steelblue')
    ax1_twin.tick_params(axis='y', labelcolor='orange')
    ax1.grid(True, alpha=0.3)
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom', fontsize=9)
    
    for bar in bars2:
        height = bar.get_height()
        ax1_twin.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height:.3f}', ha='center', va='bottom', fontsize=9)
    
    # Classification metrics comparison
    class_tasks = ['Primary\nFertilizer', 'Secondary\nFertilizer', 'pH\nAmendment']
    accuracy_values = [
        results_dict['classification']['primary_fertilizer']['accuracy'],
        results_dict['classification']['secondary_fertilizer']['accuracy'],
        results_dict['classification']['ph_amendment']['accuracy']
    ]
    f1_values = [
        results_dict['classification']['primary_fertilizer']['f1'],
        results_dict['classification']['secondary_fertilizer']['f1'],
        results_dict['classification']['ph_amendment']['f1']
    ]
    
    x = np.arange(len(class_tasks))
    
    bars1 = axes[1].bar(x - width/2, accuracy_values, width, label='Accuracy', color='green')
    bars2 = axes[1].bar(x + width/2, f1_values, width, label='F1-Score', color='coral')
    
    axes[1].set_xlabel('Task')
    axes[1].set_ylabel('Score')
    axes[1].set_title('Classification Performance')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(class_tasks)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    axes[1].set_ylim(0, 1.1)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            axes[1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.3f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Performance comparison chart saved: performance_comparison.png")
    plt.close()

def save_results_to_excel(results_dict, df):
    """Save comprehensive results to Excel file"""
    
    print("\n💾 Saving results to Excel...")
    
    with pd.ExcelWriter('model_evaluation_report.xlsx', engine='openpyxl') as writer:
        
        # Summary sheet
        summary_data = {
            'Metric': ['Average RMSE', 'Average MAE', 'Average R²', 
                      'Average Accuracy', 'Average F1-Score'],
            'Value': [
                results_dict['summary']['avg_rmse'],
                results_dict['summary']['avg_mae'],
                results_dict['summary']['avg_r2'],
                results_dict['summary']['avg_accuracy'],
                results_dict['summary']['avg_f1']
            ]
        }
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
        
        # Regression results
        reg_data = {
            'Task': ['N_Status', 'P_Status', 'K_Status'],
            'RMSE': [
                results_dict['regression']['n_status']['rmse'],
                results_dict['regression']['p_status']['rmse'],
                results_dict['regression']['k_status']['rmse']
            ],
            'MAE': [
                results_dict['regression']['n_status']['mae'],
                results_dict['regression']['p_status']['mae'],
                results_dict['regression']['k_status']['mae']
            ],
            'R² Score': [
                results_dict['regression']['n_status']['r2'],
                results_dict['regression']['p_status']['r2'],
                results_dict['regression']['k_status']['r2']
            ]
        }
        pd.DataFrame(reg_data).to_excel(writer, sheet_name='Regression_Results', index=False)
        
        # Classification results
        class_data = {
            'Task': ['Primary Fertilizer', 'Secondary Fertilizer', 'pH Amendment'],
            'Accuracy': [
                results_dict['classification']['primary_fertilizer']['accuracy'],
                results_dict['classification']['secondary_fertilizer']['accuracy'],
                results_dict['classification']['ph_amendment']['accuracy']
            ],
            'Precision': [
                results_dict['classification']['primary_fertilizer']['precision'],
                results_dict['classification']['secondary_fertilizer']['precision'],
                results_dict['classification']['ph_amendment']['precision']
            ],
            'Recall': [
                results_dict['classification']['primary_fertilizer']['recall'],
                results_dict['classification']['secondary_fertilizer']['recall'],
                results_dict['classification']['ph_amendment']['recall']
            ],
            'F1-Score': [
                results_dict['classification']['primary_fertilizer']['f1'],
                results_dict['classification']['secondary_fertilizer']['f1'],
                results_dict['classification']['ph_amendment']['f1']
            ],
            'Top-3 Accuracy': [
                results_dict['classification']['primary_fertilizer']['top3_accuracy'],
                results_dict['classification']['secondary_fertilizer']['top3_accuracy'],
                results_dict['classification']['ph_amendment']['top3_accuracy']
            ]
        }
        pd.DataFrame(class_data).to_excel(writer, sheet_name='Classification_Results', index=False)
        
        # Dataset statistics
        stats_data = {
            'Feature': ['Samples', 'Input Features', 'Soil Types', 'Crop Types',
                       'Primary Fertilizers', 'Secondary Fertilizers', 'pH Amendments'],
            'Count': [
                len(df),
                9,
                df['Soil_Type'].nunique(),
                df['Crop_Type'].nunique(),
                df['Primary_Fertilizer'].nunique(),
                df['Secondary_Fertilizer'].nunique(),
                df['pH_Amendment'].nunique()
            ]
        }
        pd.DataFrame(stats_data).to_excel(writer, sheet_name='Dataset_Statistics', index=False)
    
    print("✓ Evaluation report saved: model_evaluation_report.xlsx")

# Main execution
if __name__ == "__main__":
    
    print("=" * 80)
    print("📊 FERTILIZER RECOMMENDATION SYSTEM - EVALUATION & ANALYSIS")
    print("=" * 80)
    
    # Load resources
    model, prep_objects, df = load_model_and_data()
    
    # Generate comprehensive report
    results_dict = generate_detailed_report(model, prep_objects, df)
    
    # Feature importance analysis
    plot_feature_importance_analysis(df, prep_objects)
    
    # Performance comparison chart
    generate_performance_comparison_chart(results_dict)
    
    # Save results to Excel
    save_results_to_excel(results_dict, df)
    
    print("\n" + "=" * 80)
    print("✅ EVALUATION COMPLETE")
    print("=" * 80)
    
    print("\n📁 Generated Files:")
    print("  ✓ feature_analysis.png")
    print("  ✓ performance_comparison.png")
    print("  ✓ model_evaluation_report.xlsx")
    
    print("\n🎯 Model is ready for deployment!")
    print("=" * 80)
