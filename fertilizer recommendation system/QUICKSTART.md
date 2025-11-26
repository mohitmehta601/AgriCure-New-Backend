# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

Open your terminal in this directory and run:

```bash
pip install pandas numpy scikit-learn xgboost catboost lightgbm
```

**Optional (for best performance):**

```bash
pip install autogluon
```

_Note: AutoGluon is optional. The system works with 4 base models if AutoGluon is not installed._

---

### Step 2: Train the Model

Run the main training script:

```bash
python multioutput_stacking_fertilizer.py
```

**Expected Time:**

- Without AutoGluon: ~5-10 minutes
- With AutoGluon: ~15-30 minutes (depending on CPU)

**What Happens:**

- Loads `Dataset.csv` (10,002 samples)
- Trains 4-5 base models with 5-fold cross-validation
- Creates OOF predictions for meta-learning
- Trains meta-learner on stacked features
- Evaluates on test set
- Saves model to `stacked_model.pkl`

**Expected Output:**

```
OVERALL AVERAGE ACCURACY: ~0.85-0.95
```

---

### Step 3: Make Predictions

Run the example prediction script:

```bash
python example_prediction.py
```

**What Happens:**

- Loads the trained model
- Creates 5 sample agricultural scenarios
- Generates fertilizer recommendations
- Saves results to `predictions_output.csv`

---

## 📊 Expected Accuracy

Based on the dataset characteristics, you should expect:

| Target Variable      | Expected Accuracy |
| -------------------- | ----------------- |
| N_Status             | 85-95%            |
| P_Status             | 85-95%            |
| K_Status             | 85-95%            |
| Primary_Fertilizer   | 75-90%            |
| Secondary_Fertilizer | 70-85%            |
| pH_Amendment         | 80-92%            |
| **Overall Average**  | **80-92%**        |

---

## 🔧 Troubleshooting

### Issue: "No module named 'xgboost'"

**Solution:** Install missing packages:

```bash
pip install xgboost catboost lightgbm
```

### Issue: "AutoGluon installation failed"

**Solution:** The system will work without AutoGluon. Alternatively:

```bash
pip install --upgrade pip setuptools wheel
pip install autogluon
```

### Issue: Training is too slow

**Solution:** Edit `multioutput_stacking_fertilizer.py`:

```python
# Line ~545: Change n_folds
stacker = MultiOutputOOFStacker(n_folds=3, use_autogluon=False)
```

### Issue: Memory error

**Solution:** Reduce model complexity:

- Use fewer estimators: `n_estimators=100`
- Disable AutoGluon: `use_autogluon=False`
- Process one target at a time

---

## 📁 Files Generated

After running the scripts, you'll have:

```
fertilizer recommendation system/
├── Dataset.csv                         # Your input data
├── multioutput_stacking_fertilizer.py  # Training script
├── example_prediction.py               # Prediction demo
├── requirements.txt                    # Dependencies
├── README.md                           # Full documentation
├── QUICKSTART.md                       # This file
├── stacked_model.pkl                   # Trained model (150-300 MB)
└── predictions_output.csv              # Example predictions
```

---

## 🎯 Using in Your Application

### Python Integration

```python
from multioutput_stacking_fertilizer import MultiOutputOOFStacker
import pandas as pd

# Load model once
model = MultiOutputOOFStacker.load('stacked_model.pkl')

# Make predictions on new data
new_data = pd.DataFrame({...})  # Your input
predictions = model.predict(new_data)

# Access results
n_status = predictions['N_Status'][0]
primary_fert = predictions['Primary_Fertilizer'][0]
```

### REST API Integration

Create a simple Flask API:

```python
from flask import Flask, request, jsonify
from multioutput_stacking_fertilizer import MultiOutputOOFStacker
import pandas as pd

app = Flask(__name__)
model = MultiOutputOOFStacker.load('stacked_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    df = pd.DataFrame([data])
    predictions = model.predict(df)
    return jsonify({k: v[0] for k, v in predictions.items()})

if __name__ == '__main__':
    app.run(port=5000)
```

---

## 💡 Tips for Best Results

1. **Data Quality**: Ensure input data matches training format
2. **Feature Ranges**: Keep values within reasonable agricultural ranges
3. **Categorical Values**: Use exact spelling from training data
4. **Model Updates**: Retrain periodically with new data
5. **Ensemble Diversity**: All 5 base models contribute unique insights

---

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **Code Details**: Well-commented in `multioutput_stacking_fertilizer.py`
- **Methodology**: OOF stacking prevents overfitting
- **Production Ready**: Includes save/load, error handling, logging

---

## ✅ Checklist

- [ ] Installed dependencies
- [ ] Ran training script
- [ ] Model saved successfully
- [ ] Ran example predictions
- [ ] Reviewed output accuracy
- [ ] Ready for integration

---

**Questions?** Check the main `README.md` for detailed explanations.

**Good luck with your agricultural AI project! 🌾**
