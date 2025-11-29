# train_soil_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
import joblib

# ======== CONFIG ========
DATA_PATH = "india_soil_dataset.csv"   # <- change to your file
MODEL_PATH = "soil_model_xgb.pkl"
LABEL_ENCODER_PATH = "soil_label_encoder.pkl"

# Columns (edit according to your dataset)
NUMERIC_FEATURES = [
    "lat", "lon",
    "elevation",
    "rainfall",
    "temperature",
    "aridity_index",
    "dist_river_km",
    "dist_coast_km",
    "ndvi"
]

CATEGORICAL_FEATURES = [
    "landcover",
    "geology"
]

TARGET_COL = "soil_type"
# ========================

def main():
    # 1. Load dataset
    df = pd.read_csv(DATA_PATH)

    # Optional: drop rows with missing critical values
    df = df.dropna(subset=NUMERIC_FEATURES + CATEGORICAL_FEATURES + [TARGET_COL])

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()
    y = df[TARGET_COL].copy()

    # 2. Encode target labels
    label_encoder = LabelEncoder()
    y_enc = label_encoder.fit_transform(y)

    print("Soil type classes:", list(label_encoder.classes_))

    # 3. Preprocessor: numeric passthrough, categorical OneHot
    numeric_transformer = "passthrough"
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )

    # 4. XGBoost classifier
    num_classes = len(label_encoder.classes_)

    xgb_clf = XGBClassifier(
        objective="multi:softprob",
        num_class=num_classes,
        n_estimators=400,
        learning_rate=0.05,
        max_depth=8,
        subsample=0.8,
        colsample_bytree=0.8,
        tree_method="hist",      # good speed
        eval_metric="mlogloss",
        n_jobs=-1,
        random_state=42,
    )

    # 5. Full pipeline
    model = Pipeline(
        steps=[
            ("preprocess", preprocessor),
            ("clf", xgb_clf),
        ]
    )

    # 6. Train/validation split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.2, random_state=42, stratify=y_enc
    )

    # 7. Fit model
    print("Training model...")
    model.fit(X_train, y_train)

    # 8. Evaluate
    print("Evaluating on test set...")
    y_pred = model.predict(X_test)

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_
    ))

    # 9. Save model + label encoder
    joblib.dump(model, MODEL_PATH)
    joblib.dump(label_encoder, LABEL_ENCODER_PATH)

    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Label encoder saved to: {LABEL_ENCODER_PATH}")

if __name__ == "__main__":
    main()
