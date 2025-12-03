"""
🌱 Multi-Task Deep Learning Model for Fertilizer Recommendation System
Performs both regression (NPK status) and classification (fertilizer recommendations)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, Model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

print("=" * 80)
print("🌾 FERTILIZER RECOMMENDATION SYSTEM - Multi-Task Deep Learning Model")
print("=" * 80)

# ============================================================================
# 1️⃣ DATA LOADING
# ============================================================================
print("\n📂 Loading Dataset...")
df = pd.read_csv('Final AgriCure Dataset.csv')
print(f"✓ Dataset loaded: {df.shape[0]} samples, {df.shape[1]} features")
print(f"\nDataset Info:")
print(df.info())
print(f"\nFirst few rows:")
print(df.head())

# Check for missing values
print(f"\n🔍 Missing Values:")
print(df.isnull().sum())

# ============================================================================
# 2️⃣ DATA PREPROCESSING
# ============================================================================
print("\n" + "=" * 80)
print("🔧 DATA PREPROCESSING")
print("=" * 80)

# Separate features and targets
input_features = ['Nitrogen(mg/kg)', 'Phosphorus(mg/kg)', 'Potassium(mg/kg)', 
                  'Soil_Type', 'Crop_Type', 'pH', 'Electrical_Conductivity', 
                  'Soil_Moisture', 'Soil_Temperture']

# Regression targets (numeric NPK status)
regression_targets = ['N_Status', 'P_Status', 'K_Status']

# Classification targets (categorical recommendations)
classification_targets = ['Primary_Fertilizer', 'Secondary_Fertilizer', 'pH_Amendment']

print(f"\n✓ Input Features: {len(input_features)}")
print(f"  - Numeric: Nitrogen, Phosphorus, Potassium, pH, EC, Moisture, Temperature")
print(f"  - Categorical: Soil_Type, Crop_Type")
print(f"\n✓ Regression Targets: {regression_targets}")
print(f"✓ Classification Targets: {classification_targets}")

# ============================================================================
# 2.1 Encode Categorical Features
# ============================================================================
print("\n📋 Encoding Categorical Variables...")

# Label Encoding for Soil_Type and Crop_Type
le_soil = LabelEncoder()
le_crop = LabelEncoder()

df['Soil_Type_Encoded'] = le_soil.fit_transform(df['Soil_Type'])
df['Crop_Type_Encoded'] = le_crop.fit_transform(df['Crop_Type'])

print(f"✓ Soil Types: {list(le_soil.classes_)}")
print(f"✓ Crop Types: {list(le_crop.classes_)}")

# Label Encoding for Classification Targets
le_primary = LabelEncoder()
le_secondary = LabelEncoder()
le_ph = LabelEncoder()

df['Primary_Fertilizer_Encoded'] = le_primary.fit_transform(df['Primary_Fertilizer'])
df['Secondary_Fertilizer_Encoded'] = le_secondary.fit_transform(df['Secondary_Fertilizer'])
df['pH_Amendment_Encoded'] = le_ph.fit_transform(df['pH_Amendment'])

n_classes_primary = len(le_primary.classes_)
n_classes_secondary = len(le_secondary.classes_)
n_classes_ph = len(le_ph.classes_)

print(f"\n✓ Primary Fertilizer Classes: {n_classes_primary}")
print(f"✓ Secondary Fertilizer Classes: {n_classes_secondary}")
print(f"✓ pH Amendment Classes: {n_classes_ph}")

# ============================================================================
# 2.2 Prepare Input Features (X)
# ============================================================================
print("\n🔢 Preparing Input Features...")

# Create feature matrix with encoded categorical variables
X = df[['Nitrogen(mg/kg)', 'Phosphorus(mg/kg)', 'Potassium(mg/kg)', 
        'Soil_Type_Encoded', 'Crop_Type_Encoded', 'pH', 
        'Electrical_Conductivity', 'Soil_Moisture', 'Soil_Temperture']].values

print(f"✓ Input shape before scaling: {X.shape}")

# Min-Max Scaling (0-1 normalization)
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

print(f"✓ Input shape after scaling: {X_scaled.shape}")
print(f"✓ Feature ranges normalized to [0, 1]")

# ============================================================================
# 2.3 Prepare Target Variables (Y)
# ============================================================================
print("\n🎯 Preparing Target Variables...")

# Regression targets (numeric NPK status)
y_n_status = df['N_Status'].values.reshape(-1, 1)
y_p_status = df['P_Status'].values.reshape(-1, 1)
y_k_status = df['K_Status'].values.reshape(-1, 1)

# Classification targets (encoded fertilizer recommendations)
y_primary = df['Primary_Fertilizer_Encoded'].values
y_secondary = df['Secondary_Fertilizer_Encoded'].values
y_ph_amendment = df['pH_Amendment_Encoded'].values

print(f"✓ Regression targets prepared:")
print(f"  - N_Status: {y_n_status.shape}")
print(f"  - P_Status: {y_p_status.shape}")
print(f"  - K_Status: {y_k_status.shape}")
print(f"\n✓ Classification targets prepared:")
print(f"  - Primary Fertilizer: {y_primary.shape}")
print(f"  - Secondary Fertilizer: {y_secondary.shape}")
print(f"  - pH Amendment: {y_ph_amendment.shape}")

# ============================================================================
# 3️⃣ TRAIN-VALIDATION-TEST SPLIT
# ============================================================================
print("\n" + "=" * 80)
print("✂️ SPLITTING DATA")
print("=" * 80)

# First split: 80% train, 20% temp
X_train, X_temp, y_n_train, y_n_temp, y_p_train, y_p_temp, y_k_train, y_k_temp, \
y_prim_train, y_prim_temp, y_sec_train, y_sec_temp, y_ph_train, y_ph_temp = train_test_split(
    X_scaled, y_n_status, y_p_status, y_k_status, y_primary, y_secondary, y_ph_amendment,
    test_size=0.2, random_state=42
)

# Second split: Split temp into 50-50 (10% val, 10% test of original)
X_val, X_test, y_n_val, y_n_test, y_p_val, y_p_test, y_k_val, y_k_test, \
y_prim_val, y_prim_test, y_sec_val, y_sec_test, y_ph_val, y_ph_test = train_test_split(
    X_temp, y_n_temp, y_p_temp, y_k_temp, y_prim_temp, y_sec_temp, y_ph_temp,
    test_size=0.5, random_state=42
)

print(f"✓ Training Set:   {X_train.shape[0]} samples ({X_train.shape[0]/len(X_scaled)*100:.1f}%)")
print(f"✓ Validation Set: {X_val.shape[0]} samples ({X_val.shape[0]/len(X_scaled)*100:.1f}%)")
print(f"✓ Test Set:       {X_test.shape[0]} samples ({X_test.shape[0]/len(X_scaled)*100:.1f}%)")

# ============================================================================
# 4️⃣ BUILD MULTI-TASK NEURAL NETWORK
# ============================================================================
print("\n" + "=" * 80)
print("🧠 BUILDING MULTI-TASK NEURAL NETWORK")
print("=" * 80)

# Input layer
input_layer = layers.Input(shape=(9,), name='input_layer')

# Shared Feature Learning Layers
print("\n🔷 Shared Feature Learning Layers:")
shared_1 = layers.Dense(64, activation='relu', name='shared_dense_1')(input_layer)
print(f"  ✓ Layer 1: 64 neurons, ReLU activation")

shared_2 = layers.Dense(128, activation='relu', name='shared_dense_2')(shared_1)
print(f"  ✓ Layer 2: 128 neurons, ReLU activation")

dropout = layers.Dropout(0.3, name='dropout_layer')(shared_2)
print(f"  ✓ Dropout: 30% (prevents overfitting)")

shared_3 = layers.Dense(64, activation='relu', name='shared_dense_3')(dropout)
print(f"  ✓ Layer 3: 64 neurons, ReLU activation")

# ============================================================================
# 4.1 Regression Output Branches (NPK Status)
# ============================================================================
print("\n🔷 Regression Branches (Numeric NPK Status):")

# N_Status output
n_status_output = layers.Dense(1, activation='linear', name='n_status_output')(shared_3)
print(f"  ✓ N_Status: 1 neuron, Linear activation")

# P_Status output
p_status_output = layers.Dense(1, activation='linear', name='p_status_output')(shared_3)
print(f"  ✓ P_Status: 1 neuron, Linear activation")

# K_Status output
k_status_output = layers.Dense(1, activation='linear', name='k_status_output')(shared_3)
print(f"  ✓ K_Status: 1 neuron, Linear activation")

# ============================================================================
# 4.2 Classification Output Branches (Fertilizer Recommendations)
# ============================================================================
print("\n🔷 Classification Branches (Fertilizer Recommendations):")

# Primary Fertilizer output
primary_fertilizer_output = layers.Dense(
    n_classes_primary, activation='softmax', name='primary_fertilizer_output'
)(shared_3)
print(f"  ✓ Primary Fertilizer: {n_classes_primary} classes, Softmax activation")

# Secondary Fertilizer output
secondary_fertilizer_output = layers.Dense(
    n_classes_secondary, activation='softmax', name='secondary_fertilizer_output'
)(shared_3)
print(f"  ✓ Secondary Fertilizer: {n_classes_secondary} classes, Softmax activation")

# pH Amendment output
ph_amendment_output = layers.Dense(
    n_classes_ph, activation='softmax', name='ph_amendment_output'
)(shared_3)
print(f"  ✓ pH Amendment: {n_classes_ph} classes, Softmax activation")

# ============================================================================
# 4.3 Create Multi-Task Model
# ============================================================================
print("\n🔷 Creating Multi-Task Model...")

model = Model(
    inputs=input_layer,
    outputs=[
        n_status_output,           # Regression 1
        p_status_output,           # Regression 2
        k_status_output,           # Regression 3
        primary_fertilizer_output, # Classification 1
        secondary_fertilizer_output, # Classification 2
        ph_amendment_output        # Classification 3
    ],
    name='Fertilizer_Recommendation_Model'
)

print(f"\n✓ Multi-Task Model Created Successfully!")
print(f"  - Input: 9 features")
print(f"  - Outputs: 3 regression + 3 classification")

# ============================================================================
# 5️⃣ COMPILE MODEL
# ============================================================================
print("\n" + "=" * 80)
print("⚙️ COMPILING MODEL")
print("=" * 80)

# Define losses for each output
losses = {
    'n_status_output': 'mse',           # Mean Squared Error for regression
    'p_status_output': 'mse',
    'k_status_output': 'mse',
    'primary_fertilizer_output': 'sparse_categorical_crossentropy',   # CE for classification
    'secondary_fertilizer_output': 'sparse_categorical_crossentropy',
    'ph_amendment_output': 'sparse_categorical_crossentropy'
}

# Define metrics for each output
metrics = {
    'n_status_output': ['mae'],
    'p_status_output': ['mae'],
    'k_status_output': ['mae'],
    'primary_fertilizer_output': ['accuracy'],
    'secondary_fertilizer_output': ['accuracy'],
    'ph_amendment_output': ['accuracy']
}

# Compile model
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss=losses,
    metrics=metrics
)

print("\n✓ Model Compiled Successfully!")
print("\n📊 Loss Functions:")
print("  - Regression (N,P,K): Mean Squared Error (MSE)")
print("  - Classification: Sparse Categorical Cross-Entropy")
print("\n📊 Optimizer: Adam (learning_rate=0.001)")
print("\n📊 Metrics:")
print("  - Regression: Mean Absolute Error (MAE)")
print("  - Classification: Accuracy")

# Display model architecture
print("\n" + "=" * 80)
print("📐 MODEL ARCHITECTURE SUMMARY")
print("=" * 80)
model.summary()

# ============================================================================
# 6️⃣ SETUP CALLBACKS
# ============================================================================
print("\n" + "=" * 80)
print("🔔 SETTING UP TRAINING CALLBACKS")
print("=" * 80)

# Early Stopping
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=20,
    restore_best_weights=True,
    verbose=1
)
print("✓ Early Stopping: patience=20, monitor=val_loss")

# Learning Rate Reduction
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=10,
    min_lr=1e-7,
    verbose=1
)
print("✓ Learning Rate Reduction: factor=0.5, patience=10")

# Model Checkpoint
checkpoint = ModelCheckpoint(
    'best_fertilizer_model.h5',
    monitor='val_loss',
    save_best_only=True,
    verbose=1
)
print("✓ Model Checkpoint: saves best model to 'best_fertilizer_model.h5'")

# ============================================================================
# 7️⃣ TRAIN MODEL
# ============================================================================
print("\n" + "=" * 80)
print("🚀 TRAINING MODEL")
print("=" * 80)

# Prepare training data dictionary
train_data = {
    'n_status_output': y_n_train,
    'p_status_output': y_p_train,
    'k_status_output': y_k_train,
    'primary_fertilizer_output': y_prim_train,
    'secondary_fertilizer_output': y_sec_train,
    'ph_amendment_output': y_ph_train
}

# Prepare validation data dictionary
val_data = {
    'n_status_output': y_n_val,
    'p_status_output': y_p_val,
    'k_status_output': y_k_val,
    'primary_fertilizer_output': y_prim_val,
    'secondary_fertilizer_output': y_sec_val,
    'ph_amendment_output': y_ph_val
}

print(f"\n⏱️ Starting training...")
print(f"Epochs: 100, Batch Size: 32")

# Train the model
history = model.fit(
    X_train,
    train_data,
    validation_data=(X_val, val_data),
    epochs=100,
    batch_size=32,
    callbacks=[early_stop, reduce_lr, checkpoint],
    verbose=1
)

print("\n✓ Training Completed!")

# ============================================================================
# 8️⃣ EVALUATE MODEL
# ============================================================================
print("\n" + "=" * 80)
print("📊 MODEL EVALUATION")
print("=" * 80)

# Make predictions on test set
predictions = model.predict(X_test)

# Unpack predictions
pred_n_status = predictions[0]
pred_p_status = predictions[1]
pred_k_status = predictions[2]
pred_primary = predictions[3]
pred_secondary = predictions[4]
pred_ph = predictions[5]

# ============================================================================
# 8.1 Regression Metrics (NPK Status)
# ============================================================================
print("\n" + "=" * 80)
print("📈 REGRESSION METRICS (NPK Status)")
print("=" * 80)

# N_Status Metrics
rmse_n = np.sqrt(mean_squared_error(y_n_test, pred_n_status))
mae_n = mean_absolute_error(y_n_test, pred_n_status)
r2_n = r2_score(y_n_test, pred_n_status)

print("\n🔹 N_Status (Nitrogen Deficiency):")
print(f"  RMSE: {rmse_n:.4f}")
print(f"  MAE:  {mae_n:.4f}")
print(f"  R² Score: {r2_n:.4f}")

# P_Status Metrics
rmse_p = np.sqrt(mean_squared_error(y_p_test, pred_p_status))
mae_p = mean_absolute_error(y_p_test, pred_p_status)
r2_p = r2_score(y_p_test, pred_p_status)

print("\n🔹 P_Status (Phosphorus Deficiency):")
print(f"  RMSE: {rmse_p:.4f}")
print(f"  MAE:  {mae_p:.4f}")
print(f"  R² Score: {r2_p:.4f}")

# K_Status Metrics
rmse_k = np.sqrt(mean_squared_error(y_k_test, pred_k_status))
mae_k = mean_absolute_error(y_k_test, pred_k_status)
r2_k = r2_score(y_k_test, pred_k_status)

print("\n🔹 K_Status (Potassium Deficiency):")
print(f"  RMSE: {rmse_k:.4f}")
print(f"  MAE:  {mae_k:.4f}")
print(f"  R² Score: {r2_k:.4f}")

# Overall regression summary
avg_rmse = (rmse_n + rmse_p + rmse_k) / 3
avg_mae = (mae_n + mae_p + mae_k) / 3
avg_r2 = (r2_n + r2_p + r2_k) / 3

print("\n" + "─" * 80)
print("📊 Overall Regression Performance:")
print(f"  Average RMSE: {avg_rmse:.4f}")
print(f"  Average MAE:  {avg_mae:.4f}")
print(f"  Average R²:   {avg_r2:.4f}")

# ============================================================================
# 8.2 Classification Metrics (Fertilizer Recommendations)
# ============================================================================
print("\n" + "=" * 80)
print("📈 CLASSIFICATION METRICS (Fertilizer Recommendations)")
print("=" * 80)

# Convert softmax probabilities to class predictions
pred_primary_class = np.argmax(pred_primary, axis=1)
pred_secondary_class = np.argmax(pred_secondary, axis=1)
pred_ph_class = np.argmax(pred_ph, axis=1)

# Primary Fertilizer Metrics
acc_primary = accuracy_score(y_prim_test, pred_primary_class)
f1_primary = f1_score(y_prim_test, pred_primary_class, average='macro')

print("\n🔹 Primary Fertilizer:")
print(f"  Accuracy:     {acc_primary:.4f} ({acc_primary*100:.2f}%)")
print(f"  Macro F1-Score: {f1_primary:.4f}")

# Secondary Fertilizer Metrics
acc_secondary = accuracy_score(y_sec_test, pred_secondary_class)
f1_secondary = f1_score(y_sec_test, pred_secondary_class, average='macro')

print("\n🔹 Secondary Fertilizer:")
print(f"  Accuracy:     {acc_secondary:.4f} ({acc_secondary*100:.2f}%)")
print(f"  Macro F1-Score: {f1_secondary:.4f}")

# pH Amendment Metrics
acc_ph = accuracy_score(y_ph_test, pred_ph_class)
f1_ph = f1_score(y_ph_test, pred_ph_class, average='macro')

print("\n🔹 pH Amendment:")
print(f"  Accuracy:     {acc_ph:.4f} ({acc_ph*100:.2f}%)")
print(f"  Macro F1-Score: {f1_ph:.4f}")

# Overall classification summary
avg_accuracy = (acc_primary + acc_secondary + acc_ph) / 3
avg_f1 = (f1_primary + f1_secondary + f1_ph) / 3

print("\n" + "─" * 80)
print("📊 Overall Classification Performance:")
print(f"  Average Accuracy: {avg_accuracy:.4f} ({avg_accuracy*100:.2f}%)")
print(f"  Average Macro F1: {avg_f1:.4f}")

# ============================================================================
# 8.3 Top-K Accuracy for Classification
# ============================================================================
print("\n" + "=" * 80)
print("🎯 TOP-K ACCURACY (Classification)")
print("=" * 80)

def top_k_accuracy(y_true, y_pred_proba, k=3):
    """Calculate top-k accuracy"""
    top_k_predictions = np.argsort(y_pred_proba, axis=1)[:, -k:]
    correct = sum([y_true[i] in top_k_predictions[i] for i in range(len(y_true))])
    return correct / len(y_true)

# Calculate Top-3 Accuracy
top3_primary = top_k_accuracy(y_prim_test, pred_primary, k=3)
top3_secondary = top_k_accuracy(y_sec_test, pred_secondary, k=3)
top3_ph = top_k_accuracy(y_ph_test, pred_ph, k=3)

print(f"\n🔹 Top-3 Accuracy:")
print(f"  Primary Fertilizer:   {top3_primary:.4f} ({top3_primary*100:.2f}%)")
print(f"  Secondary Fertilizer: {top3_secondary:.4f} ({top3_secondary*100:.2f}%)")
print(f"  pH Amendment:         {top3_ph:.4f} ({top3_ph*100:.2f}%)")

# ============================================================================
# 9️⃣ SAVE MODEL AND ENCODERS
# ============================================================================
print("\n" + "=" * 80)
print("💾 SAVING MODEL AND PREPROCESSING OBJECTS")
print("=" * 80)

# Save the final model
model.save('fertilizer_recommendation_model.h5')
print("✓ Model saved: fertilizer_recommendation_model.h5")

# Save the best model (from checkpoint)
print("✓ Best model saved: best_fertilizer_model.h5")

# Save preprocessing objects
import pickle

preprocessing_objects = {
    'scaler': scaler,
    'le_soil': le_soil,
    'le_crop': le_crop,
    'le_primary': le_primary,
    'le_secondary': le_secondary,
    'le_ph': le_ph,
    'n_classes_primary': n_classes_primary,
    'n_classes_secondary': n_classes_secondary,
    'n_classes_ph': n_classes_ph
}

with open('preprocessing_objects.pkl', 'wb') as f:
    pickle.dump(preprocessing_objects, f)
print("✓ Preprocessing objects saved: preprocessing_objects.pkl")

# Save training history
with open('training_history.pkl', 'wb') as f:
    pickle.dump(history.history, f)
print("✓ Training history saved: training_history.pkl")

# ============================================================================
# 🔟 TEST PREDICTION EXAMPLE
# ============================================================================
print("\n" + "=" * 80)
print("🌾 EXAMPLE PREDICTION")
print("=" * 80)

# Example input (from your specification)
example_input = {
    'Nitrogen': 5,
    'Phosphorus': 10,
    'Potassium': 130,
    'Soil_Type': 'Sandy',
    'Crop_Type': 'Rice',
    'pH': 5.2,
    'EC': 300,
    'Moisture': 15,
    'Temperature': 29
}

print("\n📥 Input Parameters:")
for key, value in example_input.items():
    print(f"  {key}: {value}")

# Encode categorical inputs
try:
    soil_encoded = le_soil.transform([example_input['Soil_Type']])[0]
except:
    print(f"\n⚠️ Warning: '{example_input['Soil_Type']}' not in training data. Using default.")
    soil_encoded = 0

try:
    crop_encoded = le_crop.transform([example_input['Crop_Type']])[0]
except:
    print(f"\n⚠️ Warning: '{example_input['Crop_Type']}' not in training data. Using default.")
    crop_encoded = 0

# Create input array
example_array = np.array([[
    example_input['Nitrogen'],
    example_input['Phosphorus'],
    example_input['Potassium'],
    soil_encoded,
    crop_encoded,
    example_input['pH'],
    example_input['EC'],
    example_input['Moisture'],
    example_input['Temperature']
]])

# Scale the input
example_scaled = scaler.transform(example_array)

# Make prediction
example_pred = model.predict(example_scaled, verbose=0)

# Extract predictions
pred_n = example_pred[0][0][0]
pred_p = example_pred[1][0][0]
pred_k = example_pred[2][0][0]
pred_prim_idx = np.argmax(example_pred[3][0])
pred_sec_idx = np.argmax(example_pred[4][0])
pred_ph_idx = np.argmax(example_pred[5][0])

# Decode predictions
pred_primary_name = le_primary.inverse_transform([pred_prim_idx])[0]
pred_secondary_name = le_secondary.inverse_transform([pred_sec_idx])[0]
pred_ph_name = le_ph.inverse_transform([pred_ph_idx])[0]

print("\n📤 Model Predictions:")
print(f"\n  Nutrient Status (Numeric):")
print(f"    N_Status: {pred_n:.4f}")
print(f"    P_Status: {pred_p:.4f}")
print(f"    K_Status: {pred_k:.4f}")

print(f"\n  Fertilizer Recommendations:")
print(f"    Primary Fertilizer:   {pred_primary_name}")
print(f"    Secondary Fertilizer: {pred_secondary_name}")
print(f"    pH Amendment:         {pred_ph_name}")

# Interpretation
print(f"\n  Interpretation:")
if pred_n < 0.5:
    print(f"    ✓ Nitrogen: Sufficient")
elif pred_n < 20:
    print(f"    ⚠️ Nitrogen: Moderate deficiency")
else:
    print(f"    ❗ Nitrogen: High deficiency")

if pred_p < 0.5:
    print(f"    ✓ Phosphorus: Sufficient")
elif pred_p < 2:
    print(f"    ⚠️ Phosphorus: Moderate deficiency")
else:
    print(f"    ❗ Phosphorus: High deficiency")

if pred_k < 0.5:
    print(f"    ✓ Potassium: Sufficient")
elif pred_k < 20:
    print(f"    ⚠️ Potassium: Moderate deficiency")
else:
    print(f"    ❗ Potassium: High deficiency")

# ============================================================================
# 1️⃣1️⃣ VISUALIZATION - TRAINING HISTORY
# ============================================================================
print("\n" + "=" * 80)
print("📊 GENERATING VISUALIZATIONS")
print("=" * 80)

fig, axes = plt.subplots(3, 2, figsize=(15, 12))
fig.suptitle('Training History - Multi-Task Model', fontsize=16, fontweight='bold')

# Total Loss
axes[0, 0].plot(history.history['loss'], label='Training Loss', linewidth=2)
axes[0, 0].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
axes[0, 0].set_title('Total Loss')
axes[0, 0].set_xlabel('Epoch')
axes[0, 0].set_ylabel('Loss')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# N_Status Loss
axes[0, 1].plot(history.history['n_status_output_loss'], label='Training', linewidth=2)
axes[0, 1].plot(history.history['val_n_status_output_loss'], label='Validation', linewidth=2)
axes[0, 1].set_title('N_Status Loss (MSE)')
axes[0, 1].set_xlabel('Epoch')
axes[0, 1].set_ylabel('Loss')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# P_Status Loss
axes[1, 0].plot(history.history['p_status_output_loss'], label='Training', linewidth=2)
axes[1, 0].plot(history.history['val_p_status_output_loss'], label='Validation', linewidth=2)
axes[1, 0].set_title('P_Status Loss (MSE)')
axes[1, 0].set_xlabel('Epoch')
axes[1, 0].set_ylabel('Loss')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3)

# K_Status Loss
axes[1, 1].plot(history.history['k_status_output_loss'], label='Training', linewidth=2)
axes[1, 1].plot(history.history['val_k_status_output_loss'], label='Validation', linewidth=2)
axes[1, 1].set_title('K_Status Loss (MSE)')
axes[1, 1].set_xlabel('Epoch')
axes[1, 1].set_ylabel('Loss')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

# Primary Fertilizer Accuracy
axes[2, 0].plot(history.history['primary_fertilizer_output_accuracy'], label='Training', linewidth=2)
axes[2, 0].plot(history.history['val_primary_fertilizer_output_accuracy'], label='Validation', linewidth=2)
axes[2, 0].set_title('Primary Fertilizer Accuracy')
axes[2, 0].set_xlabel('Epoch')
axes[2, 0].set_ylabel('Accuracy')
axes[2, 0].legend()
axes[2, 0].grid(True, alpha=0.3)

# pH Amendment Accuracy
axes[2, 1].plot(history.history['ph_amendment_output_accuracy'], label='Training', linewidth=2)
axes[2, 1].plot(history.history['val_ph_amendment_output_accuracy'], label='Validation', linewidth=2)
axes[2, 1].set_title('pH Amendment Accuracy')
axes[2, 1].set_xlabel('Epoch')
axes[2, 1].set_ylabel('Accuracy')
axes[2, 1].legend()
axes[2, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('training_history.png', dpi=300, bbox_inches='tight')
print("✓ Training history plot saved: training_history.png")
plt.close()

# ============================================================================
# 1️⃣2️⃣ CONFUSION MATRICES
# ============================================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Confusion Matrices - Classification Tasks', fontsize=16, fontweight='bold')

# Primary Fertilizer Confusion Matrix
cm_primary = confusion_matrix(y_prim_test, pred_primary_class)
sns.heatmap(cm_primary, annot=True, fmt='d', cmap='Blues', ax=axes[0], cbar=False)
axes[0].set_title(f'Primary Fertilizer\nAccuracy: {acc_primary:.2%}')
axes[0].set_xlabel('Predicted')
axes[0].set_ylabel('Actual')

# Secondary Fertilizer Confusion Matrix
cm_secondary = confusion_matrix(y_sec_test, pred_secondary_class)
sns.heatmap(cm_secondary, annot=True, fmt='d', cmap='Greens', ax=axes[1], cbar=False)
axes[1].set_title(f'Secondary Fertilizer\nAccuracy: {acc_secondary:.2%}')
axes[1].set_xlabel('Predicted')
axes[1].set_ylabel('Actual')

# pH Amendment Confusion Matrix
cm_ph = confusion_matrix(y_ph_test, pred_ph_class)
sns.heatmap(cm_ph, annot=True, fmt='d', cmap='Oranges', ax=axes[2], cbar=False)
axes[2].set_title(f'pH Amendment\nAccuracy: {acc_ph:.2%}')
axes[2].set_xlabel('Predicted')
axes[2].set_ylabel('Actual')

plt.tight_layout()
plt.savefig('confusion_matrices.png', dpi=300, bbox_inches='tight')
print("✓ Confusion matrices saved: confusion_matrices.png")
plt.close()

# ============================================================================
# 1️⃣3️⃣ REGRESSION PREDICTIONS vs ACTUAL
# ============================================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Regression Predictions vs Actual Values', fontsize=16, fontweight='bold')

# N_Status
axes[0].scatter(y_n_test, pred_n_status, alpha=0.5, s=20)
axes[0].plot([y_n_test.min(), y_n_test.max()], [y_n_test.min(), y_n_test.max()], 'r--', lw=2)
axes[0].set_title(f'N_Status\nR² = {r2_n:.4f}')
axes[0].set_xlabel('Actual')
axes[0].set_ylabel('Predicted')
axes[0].grid(True, alpha=0.3)

# P_Status
axes[1].scatter(y_p_test, pred_p_status, alpha=0.5, s=20, color='green')
axes[1].plot([y_p_test.min(), y_p_test.max()], [y_p_test.min(), y_p_test.max()], 'r--', lw=2)
axes[1].set_title(f'P_Status\nR² = {r2_p:.4f}')
axes[1].set_xlabel('Actual')
axes[1].set_ylabel('Predicted')
axes[1].grid(True, alpha=0.3)

# K_Status
axes[2].scatter(y_k_test, pred_k_status, alpha=0.5, s=20, color='orange')
axes[2].plot([y_k_test.min(), y_k_test.max()], [y_k_test.min(), y_k_test.max()], 'r--', lw=2)
axes[2].set_title(f'K_Status\nR² = {r2_k:.4f}')
axes[2].set_xlabel('Actual')
axes[2].set_ylabel('Predicted')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('regression_predictions.png', dpi=300, bbox_inches='tight')
print("✓ Regression predictions plot saved: regression_predictions.png")
plt.close()

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("✅ MODEL TRAINING AND EVALUATION COMPLETE")
print("=" * 80)

print("\n📊 Final Performance Summary:")
print("\n  Regression (NPK Status):")
print(f"    Average RMSE: {avg_rmse:.4f}")
print(f"    Average MAE:  {avg_mae:.4f}")
print(f"    Average R²:   {avg_r2:.4f}")

print("\n  Classification (Fertilizer Recommendations):")
print(f"    Average Accuracy: {avg_accuracy:.2%}")
print(f"    Average Macro F1: {avg_f1:.4f}")

print("\n💾 Saved Files:")
print("  ✓ fertilizer_recommendation_model.h5")
print("  ✓ best_fertilizer_model.h5")
print("  ✓ preprocessing_objects.pkl")
print("  ✓ training_history.pkl")
print("  ✓ training_history.png")
print("  ✓ confusion_matrices.png")
print("  ✓ regression_predictions.png")

print("\n🎯 Model Ready for Deployment!")
print("=" * 80)
