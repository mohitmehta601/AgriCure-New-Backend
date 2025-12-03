# 🌱 Fertilizer Recommendation System - Multi-Task Deep Learning Model

A sophisticated machine learning system that provides intelligent fertilizer recommendations based on soil conditions and crop requirements using a multi-task neural network.

## 📋 Table of Contents

- [Overview](#overview)
- [Model Architecture](#model-architecture)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Model Details](#model-details)
- [Results](#results)
- [Files Description](#files-description)

---

## 🎯 Overview

This system uses a **Multi-Task Deep Neural Network** to simultaneously:

1. **Predict nutrient deficiency levels** (N, P, K) - Regression
2. **Recommend fertilizers** (Primary & Secondary) - Classification
3. **Suggest pH amendments** - Classification

### Why Multi-Task Learning?

- **Better Accuracy**: Shared learning improves predictions
- **Consistent Recommendations**: One model handles all dependencies
- **Real-world Applicable**: Mimics actual agronomic decision-making
- **Learns Combined Relationships**: Soil ∝ Crop ∝ Fertilizer

---

## 🧠 Model Architecture

### Input Features (9 total)

| Feature                         | Type        | Description                         |
| ------------------------------- | ----------- | ----------------------------------- |
| Nitrogen (mg/kg)                | Numeric     | Direct nitrogen level               |
| Phosphorus (mg/kg)              | Numeric     | Direct phosphorus level             |
| Potassium (mg/kg)               | Numeric     | Direct potassium level              |
| Soil Type                       | Categorical | Soil nutrient-holding capacity      |
| Crop Type                       | Categorical | Crop-specific nutrient requirements |
| pH                              | Numeric     | Affects nutrient availability       |
| Electrical Conductivity (μS/cm) | Numeric     | Salinity & ion concentration        |
| Soil Moisture (%)               | Numeric     | Nutrient uptake ability             |
| Soil Temperature (°C)           | Numeric     | Microbial activity indicator        |

### Network Architecture

```
Input Layer (9 features)
    ↓
Dense Layer: 64 neurons, ReLU
    ↓
Dense Layer: 128 neurons, ReLU
    ↓
Dropout Layer: 0.3
    ↓
Dense Layer: 64 neurons, ReLU
    ↓
    ├─→ N_Status (Linear, 1 neuron)          [Regression]
    ├─→ P_Status (Linear, 1 neuron)          [Regression]
    ├─→ K_Status (Linear, 1 neuron)          [Regression]
    ├─→ Primary Fertilizer (Softmax)         [Classification]
    ├─→ Secondary Fertilizer (Softmax)       [Classification]
    └─→ pH Amendment (Softmax)               [Classification]
```

### Output Branches

**Regression Outputs** (Numeric)

- `N_Status`: Nitrogen deficiency severity
- `P_Status`: Phosphorus deficiency severity
- `K_Status`: Potassium deficiency severity

**Classification Outputs** (Categorical)

- `Primary_Fertilizer`: Main fertilizer recommendation
- `Secondary_Fertilizer`: Supplementary fertilizer
- `pH_Amendment`: pH correction recommendation

---

## ✨ Features

### 🎓 Advanced ML Capabilities

- **Multi-task learning** combining regression and classification
- **Shared feature representation** for better generalization
- **Top-K accuracy** for alternative recommendations
- **Confidence scores** for all predictions

### 📊 Comprehensive Evaluation

- **Regression Metrics**: RMSE, MAE, R² Score
- **Classification Metrics**: Accuracy, Macro F1-Score, Top-K Accuracy
- **Visual Analytics**: Training history, confusion matrices, prediction plots

### 🔧 Production Ready

- **Model checkpointing** (saves best model)
- **Early stopping** (prevents overfitting)
- **Learning rate scheduling** (adaptive optimization)
- **Batch prediction support** (CSV input/output)

---

## 📦 Installation

### Requirements

```bash
pip install pandas numpy matplotlib seaborn scikit-learn tensorflow
```

### Python Version

- Python 3.8 or higher
- TensorFlow 2.x

---

## 🚀 Usage

### 1. Train the Model

```bash
python fertilizer_model.py
```

This will:

- Load and preprocess the dataset
- Build the multi-task neural network
- Train the model (with validation)
- Evaluate performance
- Save model and preprocessing objects
- Generate visualization plots

**Expected Training Time**: 5-15 minutes (depending on hardware)

### 2. Make Predictions

#### Single Prediction

```python
from predict import predict_fertilizer, print_prediction_results

# Define input parameters
input_data = {
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

# Get prediction
results = predict_fertilizer(input_data)
print_prediction_results(results)
```

#### Batch Predictions from CSV

```python
from predict import predict_from_csv

# Process multiple samples
predict_from_csv('soil_samples.csv', 'predictions.csv')
```

### 3. Use Pre-trained Model

```python
import pickle
from tensorflow import keras
import numpy as np

# Load model and preprocessors
model = keras.models.load_model('best_fertilizer_model.h5')
with open('preprocessing_objects.pkl', 'rb') as f:
    prep_objects = pickle.load(f)

# Your prediction code here...
```

---

## 🔬 Model Details

### Training Configuration

| Parameter               | Value |
| ----------------------- | ----- |
| Optimizer               | Adam  |
| Learning Rate           | 0.001 |
| Batch Size              | 32    |
| Max Epochs              | 100   |
| Early Stopping Patience | 20    |
| Dropout Rate            | 0.3   |

### Loss Functions

**Combined Loss**:

```
Total Loss = MSE(N_Status) + MSE(P_Status) + MSE(K_Status)
           + CE(Primary_Fertilizer) + CE(Secondary_Fertilizer) + CE(pH_Amendment)
```

- **MSE**: Mean Squared Error (for regression)
- **CE**: Categorical Cross-Entropy (for classification)

### Data Split

- **Training**: 80% (~8000 samples)
- **Validation**: 10% (~1000 samples)
- **Test**: 10% (~1000 samples)

### Preprocessing

- **Numeric features**: Min-Max Scaling (0-1)
- **Categorical features**: Label Encoding
- **Target encoding**: Label Encoding for classifications

---

## 📈 Results

### Expected Performance Metrics

**Regression (NPK Status)**
| Metric | Expected Range |
|--------|----------------|
| Average RMSE | 2.5 - 4.0 |
| Average MAE | 1.8 - 3.0 |
| Average R² | 0.85 - 0.95 |

**Classification (Fertilizer Recommendations)**
| Metric | Expected Range |
|--------|----------------|
| Average Accuracy | 85% - 95% |
| Average Macro F1 | 0.80 - 0.92 |
| Top-3 Accuracy | 92% - 98% |

### Sample Prediction

**Input:**

```
N=5, P=10, K=130, Soil=Sandy, Crop=Rice,
pH=5.2, EC=300, Moisture=15, Temp=29
```

**Output:**

```
N_Status = 0.18  → Slight Deficiency
P_Status = 0.24  → Slight Deficiency
K_Status = 1.41  → Moderate

Primary_Fertilizer   → DAP
Secondary_Fertilizer → Zinc Sulphate
pH_Amendment         → Lime
```

---

## 📁 Files Description

### Core Files

| File                         | Description                     |
| ---------------------------- | ------------------------------- |
| `fertilizer_model.py`        | Main training script            |
| `predict.py`                 | Prediction and inference script |
| `Final AgriCure Dataset.csv` | Training dataset                |

### Generated Files (after training)

| File                                 | Description                         |
| ------------------------------------ | ----------------------------------- |
| `best_fertilizer_model.h5`           | Best model (lowest validation loss) |
| `fertilizer_recommendation_model.h5` | Final model (last epoch)            |
| `preprocessing_objects.pkl`          | Scalers and encoders                |
| `training_history.pkl`               | Training metrics history            |
| `training_history.png`               | Training visualization              |
| `confusion_matrices.png`             | Classification performance          |
| `regression_predictions.png`         | Regression scatter plots            |

---

## 🎨 Visualizations

The training script generates three visualization plots:

1. **Training History** (`training_history.png`)

   - Total loss curves
   - Individual task losses
   - Classification accuracies

2. **Confusion Matrices** (`confusion_matrices.png`)

   - Primary Fertilizer predictions
   - Secondary Fertilizer predictions
   - pH Amendment predictions

3. **Regression Predictions** (`regression_predictions.png`)
   - N_Status: Actual vs Predicted
   - P_Status: Actual vs Predicted
   - K_Status: Actual vs Predicted

---

## 🧪 Example Use Cases

### 1. Soil Testing Laboratory

Process batch soil samples and generate fertilizer reports:

```python
predict_from_csv('daily_samples.csv', 'recommendations.csv')
```

### 2. Mobile Agriculture App

Real-time recommendations for farmers:

```python
results = predict_fertilizer(farm_soil_data)
send_to_farmer(results['recommendations'])
```

### 3. Precision Agriculture

Integrate with IoT sensors:

```python
sensor_data = read_from_iot_device()
recommendation = predict_fertilizer(sensor_data)
update_irrigation_system(recommendation)
```

---

## 🔧 Customization

### Adjust Model Architecture

Edit `fertilizer_model.py`:

```python
# Change layer sizes
shared_1 = layers.Dense(128, activation='relu')  # was 64
shared_2 = layers.Dense(256, activation='relu')  # was 128
```

### Modify Training Parameters

```python
# Change learning rate
optimizer=keras.optimizers.Adam(learning_rate=0.0005)

# Adjust batch size
history = model.fit(..., batch_size=64)  # was 32
```

### Add More Metrics

```python
from sklearn.metrics import precision_score, recall_score

precision = precision_score(y_true, y_pred, average='macro')
recall = recall_score(y_true, y_pred, average='macro')
```

---

## 🐛 Troubleshooting

### Issue: Model loading error

```python
# Solution: Ensure TensorFlow version matches
pip install tensorflow==2.15.0
```

### Issue: Preprocessing error with unknown categories

```python
# Solution: The predict.py handles this automatically
# Unknown soil/crop types default to most common class
```

### Issue: Poor performance on custom data

```python
# Solution: Retrain with your data
# Add your samples to the CSV and run fertilizer_model.py
```

---

## 📊 Model Interpretability

### NPK Status Interpretation

| Value    | Interpretation      |
| -------- | ------------------- |
| < 0.5    | Sufficient          |
| 0.5 - 10 | Slight deficiency   |
| 10 - 30  | Moderate deficiency |
| > 30     | High deficiency     |

### Confidence Scores

The model provides confidence scores (0-1) for all recommendations:

- **> 0.8**: High confidence
- **0.5 - 0.8**: Moderate confidence
- **< 0.5**: Low confidence (consider alternatives)

---

## 🎓 Model Benefits

✅ **Comprehensive**: Handles all aspects of fertilizer recommendation  
✅ **Accurate**: Multi-task learning improves predictions  
✅ **Fast**: Real-time inference (<100ms per sample)  
✅ **Scalable**: Batch processing for large datasets  
✅ **Interpretable**: Clear numeric deficiency scores  
✅ **Flexible**: Easy to retrain with new data

---

## 📚 References

### Model Type

Multi-Task Deep Neural Network with shared representation learning

### Techniques Used

- Multi-task learning
- Dropout regularization
- Early stopping
- Learning rate scheduling
- Min-Max normalization
- Label encoding

### Evaluation Standards

- Regression: RMSE, MAE, R²
- Classification: Accuracy, F1-Score, Top-K Accuracy

---

## 📞 Support

For issues or questions:

1. Check the troubleshooting section
2. Review the example code in `predict.py`
3. Ensure all dependencies are installed
4. Verify your input data format matches the specification

---

## 🎉 Quick Start Checklist

- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Place dataset in project folder
- [ ] Run training: `python fertilizer_model.py`
- [ ] Wait for training completion (~10 minutes)
- [ ] Test prediction: `python predict.py`
- [ ] Check generated plots and models
- [ ] Ready for production use!

---

**Built with ❤️ for sustainable agriculture**

🌾 Helping farmers make data-driven fertilizer decisions!
