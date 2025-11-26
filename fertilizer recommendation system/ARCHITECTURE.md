# System Architecture Diagram

## 📊 Complete System Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         INPUT DATA (Dataset.csv)                     │
│                              10,002 samples                          │
│  • Temperature, Humidity, Moisture, Soil_Type, Crop                 │
│  • Nitrogen, Phosphorus, Potassium, pH, EC                          │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DATA PREPROCESSING                                │
│  • Label Encode: Soil_Type, Crop                                    │
│  • Label Encode: All 6 target variables                             │
│  • Train-Test Split: 80% / 20% (Stratified)                        │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              TRAINING SET (8,001 samples)                            │
│                                                                       │
│              5-FOLD STRATIFIED CROSS-VALIDATION                      │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  FOLD 1  FOLD 2  FOLD 3  FOLD 4  FOLD 5                     │   │
│  │  ────────────────────────────────────────────────────────   │   │
│  │  Train  Train  Train  Train   VAL   ← Model predicts on VAL │   │
│  │  Train  Train  Train   VAL   Train  ← Model predicts on VAL │   │
│  │  Train  Train   VAL   Train  Train  ← Model predicts on VAL │   │
│  │  Train   VAL   Train  Train  Train  ← Model predicts on VAL │   │
│  │   VAL   Train  Train  Train  Train  ← Model predicts on VAL │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  Result: Out-of-Fold predictions covering ALL training samples      │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BASE MODEL 1: Random Forest                       │
│  • 200 trees, max_depth=15, balanced weights                        │
│  • Generates probability predictions for each fold                  │
│  • Output: [n_samples, n_classes] probabilities                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────────┐
│                    BASE MODEL 2: XGBoost                             │
│  • 200 estimators, max_depth=8, learning_rate=0.05                  │
│  • Gradient boosting with regularization                            │
│  • Output: [n_samples, n_classes] probabilities                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────────┐
│                    BASE MODEL 3: CatBoost                            │
│  • 200 iterations, depth=8, learning_rate=0.05                      │
│  • Optimized for categorical features                               │
│  • Output: [n_samples, n_classes] probabilities                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────────┐
│                    BASE MODEL 4: LightGBM                            │
│  • 200 estimators, max_depth=8, learning_rate=0.05                  │
│  • Fast gradient boosting framework                                 │
│  • Output: [n_samples, n_classes] probabilities                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌─────────────────────────────────────────────────────────────────────┐
│                    BASE MODEL 5: AutoGluon (Optional)                │
│  • Ensemble of multiple models                                      │
│  • Automatic model selection and tuning                             │
│  • Output: [n_samples, n_classes] probabilities                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              CONCATENATE OOF PREDICTIONS                             │
│                                                                       │
│  For each target (N_Status, P_Status, K_Status, etc.):             │
│                                                                       │
│  [Model1_Proba | Model2_Proba | Model3_Proba | Model4_Proba | M5]  │
│  [n_samples, n_classes*4] or [n_samples, n_classes*5]              │
│                                                                       │
│  Example for 3-class problem with 5 models:                         │
│  [n_samples, 15] feature matrix for meta-learner                    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    META-LEARNER (LightGBM)                           │
│                                                                       │
│  Input: Concatenated OOF probability predictions                    │
│  • 100 estimators, max_depth=5, learning_rate=0.05                  │
│  • Learns optimal combination of base model predictions             │
│                                                                       │
│  Trained for EACH of the 6 targets:                                 │
│  1. N_Status meta-learner                                           │
│  2. P_Status meta-learner                                           │
│  3. K_Status meta-learner                                           │
│  4. Primary_Fertilizer meta-learner                                 │
│  5. Secondary_Fertilizer meta-learner                               │
│  6. pH_Amendment meta-learner                                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    EVALUATION ON TEST SET (2,001 samples)            │
│                                                                       │
│  For each test sample:                                              │
│  1. Base models generate predictions (averaged across 5 folds)      │
│  2. Concatenate base model probabilities                            │
│  3. Meta-learner predicts final class                               │
│                                                                       │
│  Metrics per target:                                                │
│  • Accuracy                                                          │
│  • Macro F1-score                                                    │
│                                                                       │
│  Overall: Average accuracy across all 6 targets                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MODEL PERSISTENCE                                 │
│                                                                       │
│  Save to: stacked_model.pkl                                         │
│  Contains:                                                           │
│  • All label encoders (features + targets)                          │
│  • All base models (5 models × 5 folds × 6 targets = 150 models)   │
│  • All meta-learners (6 meta-learners)                             │
│  • Feature names and metadata                                       │
│                                                                       │
│  File size: ~150-300 MB                                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Prediction Flow (Inference)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         NEW INPUT DATA                               │
│  • Temperature, Humidity, Moisture, etc.                            │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    LOAD TRAINED MODEL                                │
│  model = MultiOutputOOFStacker.load('stacked_model.pkl')           │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ENCODE FEATURES                                   │
│  • Apply saved label encoders to Soil_Type, Crop                    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│            GENERATE BASE MODEL PREDICTIONS                           │
│                                                                       │
│  For each target:                                                    │
│    For each base model:                                             │
│      Average predictions across 5 trained folds                     │
│                                                                       │
│  RandomForest  → Avg of 5 fold models → [n_samples, n_classes]     │
│  XGBoost       → Avg of 5 fold models → [n_samples, n_classes]     │
│  CatBoost      → Avg of 5 fold models → [n_samples, n_classes]     │
│  LightGBM      → Avg of 5 fold models → [n_samples, n_classes]     │
│  AutoGluon     → Avg of 5 fold models → [n_samples, n_classes]     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│            CONCATENATE BASE PREDICTIONS                              │
│  Meta-features = [Model1 | Model2 | Model3 | Model4 | Model5]      │
│  Shape: [n_samples, n_classes × n_models]                           │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│            META-LEARNER PREDICTION                                   │
│  For each target, apply corresponding meta-learner                   │
│  Final prediction = meta_learner.predict(meta_features)             │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│            DECODE PREDICTIONS                                        │
│  • Apply inverse label encoding to get original labels              │
│  • Return dictionary: {target_name: predictions}                    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         OUTPUT                                       │
│  {                                                                   │
│    'N_Status': ['Optimal'],                                         │
│    'P_Status': ['High'],                                            │
│    'K_Status': ['Low'],                                             │
│    'Primary_Fertilizer': ['Urea'],                                  │
│    'Secondary_Fertilizer': ['Zinc Sulphate'],                       │
│    'pH_Amendment': ['None']                                         │
│  }                                                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📈 Why This Architecture Works

### 1. **Diversity Through Multiple Models**

- RandomForest: Ensemble of trees
- XGBoost: Gradient boosting
- CatBoost: Categorical optimization
- LightGBM: Fast boosting
- AutoGluon: AutoML ensemble

Each model has different strengths and captures different patterns.

### 2. **OOF Prevents Overfitting**

```
Traditional Stacking Problem:
  Train base models on data
  Predict on SAME data
  Meta-learner sees overly optimistic predictions
  → Overfitting

OOF Solution:
  Train base models on 4 folds
  Predict on 1 held-out fold
  Meta-learner sees realistic predictions
  → Better generalization
```

### 3. **Probability-Based Stacking**

```
Instead of:
  [0, 1, 0]  (one-hot encoded class)

Use:
  [0.15, 0.72, 0.13]  (probability distribution)

More information = Better meta-learning
```

### 4. **Multi-Output Efficiency**

```
Instead of:
  6 independent systems (expensive)

Use:
  Shared base models + 6 meta-learners
  Base models trained once
  Meta-learners are lightweight
```

---

## 🎯 Performance Expectations

```
Dataset Characteristics:
├─ Size: 10,002 samples
├─ Features: 10 (8 numeric, 2 categorical)
├─ Targets: 6 (multi-output)
├─ Classes per target: 2-30 (varies)
└─ Data quality: Good

Expected Results:
├─ Simple Model (Random Forest): 70-75%
├─ Single GBM: 75-80%
├─ Traditional Stacking: 80-85%
└─ OOF Stacking (This System): 85-95% ✅

Why the improvement?
├─ Ensemble diversity: +5-8%
├─ OOF methodology: +3-5%
├─ Probability stacking: +2-4%
└─ Hyperparameter tuning: +2-3%
```

---

## 🔧 Key Design Decisions

| Decision                   | Rationale                                            |
| -------------------------- | ---------------------------------------------------- |
| **5 base models**          | Balance between diversity and computational cost     |
| **5-fold CV**              | Standard practice, good bias-variance tradeoff       |
| **LightGBM meta-learner**  | Fast, accurate, handles high-dimensional features    |
| **Stratified splits**      | Maintains class balance, crucial for imbalanced data |
| **Probability stacking**   | More information than hard predictions               |
| **Separate meta-learners** | Each target has unique optimal combination           |
| **Pickle persistence**     | Simple, reliable, includes all components            |

---

## 📚 References & Further Reading

### Academic Papers

- Wolpert, D. H. (1992). "Stacked generalization"
- Breiman, L. (2001). "Random Forests"
- Chen, T. & Guestrin, C. (2016). "XGBoost"
- Ke, G. et al. (2017). "LightGBM"

### Ensemble Learning

- Zhou, Z. H. (2012). "Ensemble Methods: Foundations and Algorithms"
- Polikar, R. (2006). "Ensemble based systems in decision making"

### Agricultural ML

- Agricultural data mining and machine learning applications
- Precision agriculture with AI/ML
- Crop and fertilizer recommendation systems

---

**System Designed for Maximum Accuracy and Production Readiness**
