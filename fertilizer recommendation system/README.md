# Multi-Output Classification System with OOF Stacking

A sophisticated ensemble learning system for fertilizer recommendation that predicts 6 target variables simultaneously using Out-of-Fold (OOF) stacking.

## Features

### 🎯 Multi-Output Classification

Predicts all 6 target variables from agricultural data:

- **N_Status** - Nitrogen status in soil
- **P_Status** - Phosphorus status in soil
- **K_Status** - Potassium status in soil
- **Primary_Fertilizer** - Main fertilizer recommendation
- **Secondary_Fertilizer** - Secondary fertilizer recommendation
- **pH_Amendment** - pH adjustment recommendation

### 🤖 Base Models (5)

1. **RandomForestClassifier** - Ensemble of decision trees
2. **XGBoostClassifier** - Gradient boosting with regularization
3. **CatBoostClassifier** - Categorical feature handling
4. **LightGBMClassifier** - Fast gradient boosting
5. **AutoGluon** - Automated machine learning (optional)

### 📊 OOF Stacking Methodology

- **Out-of-Fold predictions** ensure no data leakage
- **5-fold stratified cross-validation** for robust training
- **Meta-learner (LightGBM)** combines base model predictions
- **Probability-based stacking** for maximum information retention

### 🔧 Key Capabilities

- ✅ Automatic categorical encoding (Soil_Type, Crop)
- ✅ Automatic label encoding for all targets
- ✅ Stratified K-fold splitting
- ✅ Per-target and overall accuracy metrics
- ✅ Model persistence (save/load functionality)
- ✅ Production-ready implementation

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** AutoGluon installation may take longer and requires more disk space. If you encounter issues, the system will automatically fall back to 4 base models.

### Optional: Install AutoGluon separately

```bash
pip install autogluon
```

## Usage

### Basic Usage

Simply run the script:

```bash
python multioutput_stacking_fertilizer.py
```

### What Happens

1. **Data Loading**: Loads `Dataset.csv` from the same directory
2. **Preprocessing**: Encodes categorical features and targets
3. **Train-Test Split**: 80% training, 20% testing (stratified)
4. **OOF Training**:
   - 5-fold cross-validation for each base model
   - Generates out-of-fold predictions
   - Trains meta-learner on OOF features
5. **Evaluation**: Tests on held-out 20% data
6. **Model Saving**: Saves trained model to `stacked_model.pkl`

### Expected Output

```
==========================================
FERTILIZER RECOMMENDATION SYSTEM
Multi-Output Classification with OOF Stacking
==========================================

Loading dataset from: Dataset.csv
Dataset shape: (10002, 16)

Splitting data into train (80%) and test (20%) sets...
Training set size: 8001
Test set size: 2001

==========================================
TRAINING PHASE
==========================================
[Detailed training logs for each target...]

==========================================
TESTING PHASE
==========================================
N_Status: Accuracy: 0.XXXX
P_Status: Accuracy: 0.XXXX
K_Status: Accuracy: 0.XXXX
Primary_Fertilizer: Accuracy: 0.XXXX
Secondary_Fertilizer: Accuracy: 0.XXXX
pH_Amendment: Accuracy: 0.XXXX

Overall Average Accuracy: 0.XXXX

Model saved to: stacked_model.pkl
```

## Using the Trained Model

### Load and Predict

```python
from multioutput_stacking_fertilizer import MultiOutputOOFStacker
import pandas as pd

# Load trained model
model = MultiOutputOOFStacker.load('stacked_model.pkl')

# Prepare new data
new_data = pd.DataFrame({
    'Temperature': [30.5],
    'Humidity': [65.0],
    'Moisture': [45.0],
    'Soil_Type': ['Alluvial'],
    'Crop': ['rice'],
    'Nitrogen': [75],
    'Phosphorus': [50],
    'Potassium': [60],
    'pH': [6.8],
    'EC(mmhos/cm2)': [1.2]
})

# Get predictions
predictions = model.predict(new_data)

# Access individual predictions
print(f"N Status: {predictions['N_Status'][0]}")
print(f"P Status: {predictions['P_Status'][0]}")
print(f"K Status: {predictions['K_Status'][0]}")
print(f"Primary Fertilizer: {predictions['Primary_Fertilizer'][0]}")
print(f"Secondary Fertilizer: {predictions['Secondary_Fertilizer'][0]}")
print(f"pH Amendment: {predictions['pH_Amendment'][0]}")
```

## Model Architecture

```
Input Features (10)
    ↓
[Categorical Encoding]
    ↓
┌─────────────────────────────────────────┐
│     5-Fold Stratified Cross-Validation  │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  Base Model 1: RandomForest       │  │
│  │  Base Model 2: XGBoost            │  │
│  │  Base Model 3: CatBoost           │  │
│  │  Base Model 4: LightGBM           │  │
│  │  Base Model 5: AutoGluon          │  │
│  └──────────────────────────────────┘  │
│                                         │
│  → Out-of-Fold Predictions (Probabilities)
└─────────────────────────────────────────┘
    ↓
[Concatenate OOF Features]
    ↓
┌─────────────────────────────────────────┐
│     Meta-Learner (LightGBM)             │
└─────────────────────────────────────────┘
    ↓
Final Predictions (6 Targets)
```

## Performance Optimization

### For Faster Training

- Reduce `n_folds` from 5 to 3
- Disable AutoGluon by setting `use_autogluon=False`
- Reduce `n_estimators` in base models

### For Better Accuracy

- Increase `n_folds` to 10
- Enable AutoGluon with higher `time_limit`
- Increase `n_estimators` in base models
- Add more base models (e.g., ExtraTrees, GradientBoosting)

## File Structure

```
fertilizer recommendation system/
├── Dataset.csv                              # Input dataset
├── multioutput_stacking_fertilizer.py       # Main script
├── requirements.txt                         # Python dependencies
├── stacked_model.pkl                        # Trained model (generated)
└── README.md                                # This file
```

## Technical Details

### Why OOF Stacking?

Traditional stacking can suffer from overfitting because predictions are made on the same data used for training. **Out-of-Fold (OOF) stacking** solves this by:

1. Splitting data into K folds
2. For each fold:
   - Train base models on K-1 folds
   - Predict on the held-out fold
3. Concatenate all predictions (now covering 100% of data)
4. Train meta-learner on these OOF predictions

This ensures the meta-learner sees predictions that are "unseen" by the base models, preventing overfitting.

### Stratified K-Fold

Ensures each fold maintains the same class distribution as the original dataset, crucial for imbalanced classification problems.

### Probability-Based Meta-Features

Instead of using just class predictions, we use **probability distributions** from base models, providing richer information to the meta-learner.

## Troubleshooting

### AutoGluon Installation Issues

If AutoGluon installation fails, the system will automatically use 4 base models. This is still highly effective.

### Memory Issues

- Reduce `n_estimators` in base models
- Use smaller `time_limit` for AutoGluon
- Process targets one at a time instead of all at once

### Slow Training

- Disable AutoGluon
- Reduce `n_folds`
- Use fewer base models

## Citation

If you use this system in your research or production, please cite:

```
Multi-Output OOF Stacking System for Fertilizer Recommendation
Agricultural Machine Learning Framework
2025
```

## License

MIT License - Feel free to use and modify for your needs.

## Contact

For questions, issues, or improvements, please open an issue in the repository.

---

**Happy Farming! 🌾**
