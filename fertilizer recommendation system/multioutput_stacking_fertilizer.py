"""
Multi-Output Classification System with OOF Stacking for Fertilizer Recommendation
===================================================================================

This script implements a sophisticated ensemble learning approach using:
- 5 base models (RandomForest, XGBoost, CatBoost, LightGBM, AutoGluon)
- Out-of-Fold (OOF) stacking for optimal generalization
- Multi-output classification for 6 target variables
- Proper data preprocessing and encoding
- Comprehensive evaluation metrics

Author: AI ML Engineer
Date: November 2025
"""

import pandas as pd
import numpy as np
import pickle
import warnings
from pathlib import Path

# Core ML libraries
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report

# Gradient boosting libraries
import xgboost as xgb
import catboost as cb
import lightgbm as lgb

# AutoML library
try:
    from autogluon.tabular import TabularPredictor
    AUTOGLUON_AVAILABLE = True
except ImportError:
    print("Warning: AutoGluon not available. Will use 4 base models only.")
    AUTOGLUON_AVAILABLE = False

warnings.filterwarnings('ignore')
np.random.seed(42)

class MultiOutputOOFStacker:
    """
    Multi-output classification system with Out-of-Fold stacking.
    
    This class handles:
    - Data preprocessing and encoding
    - OOF prediction generation from base models
    - Meta-learner training on OOF features
    - Multi-output prediction for 6 target variables
    """
    
    def __init__(self, n_folds=5, use_autogluon=True):
        """
        Initialize the stacking system.
        
        Args:
            n_folds: Number of folds for cross-validation
            use_autogluon: Whether to use AutoGluon as 5th base model
        """
        self.n_folds = n_folds
        self.use_autogluon = use_autogluon and AUTOGLUON_AVAILABLE
        
        # Label encoders for categorical features
        self.feature_encoders = {}
        
        # Label encoders for target variables
        self.target_encoders = {}
        
        # Store target column names
        self.target_columns = [
            'N_Status', 'P_Status', 'K_Status',
            'Primary_Fertilizer', 'Secondary_Fertilizer', 'pH_Amendment'
        ]
        
        # Store base models for each target
        self.base_models = {}
        
        # Store meta-learners for each target
        self.meta_learners = {}
        
        # Store feature names
        self.feature_columns = None
        
    def _get_base_models(self):
        """
        Define base models for the ensemble.
        
        Returns:
            Dictionary of base model instances
        """
        models = {
            'random_forest': RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1,
                class_weight='balanced'
            ),
            'xgboost': xgb.XGBClassifier(
                n_estimators=200,
                max_depth=8,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                n_jobs=-1,
                eval_metric='mlogloss'
            ),
            'catboost': cb.CatBoostClassifier(
                iterations=200,
                depth=8,
                learning_rate=0.05,
                random_state=42,
                verbose=0,
                thread_count=-1
            ),
            'lightgbm': lgb.LGBMClassifier(
                n_estimators=200,
                max_depth=8,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=42,
                n_jobs=-1,
                verbose=-1
            )
        }
        
        return models
    
    def _encode_features(self, df, fit=True):
        """
        Encode categorical features.
        
        Args:
            df: Input dataframe
            fit: Whether to fit encoders or just transform
            
        Returns:
            DataFrame with encoded features
        """
        df_encoded = df.copy()
        categorical_cols = ['Soil_Type', 'Crop']
        
        for col in categorical_cols:
            if col in df_encoded.columns:
                if fit:
                    # Fit and transform
                    self.feature_encoders[col] = LabelEncoder()
                    df_encoded[col] = self.feature_encoders[col].fit_transform(df_encoded[col].astype(str))
                else:
                    # Transform only
                    df_encoded[col] = self.feature_encoders[col].transform(df_encoded[col].astype(str))
        
        return df_encoded
    
    def _encode_targets(self, y, target_col, fit=True):
        """
        Encode target variable.
        
        Args:
            y: Target array
            target_col: Target column name
            fit: Whether to fit encoder or just transform
            
        Returns:
            Encoded target array
        """
        if fit:
            self.target_encoders[target_col] = LabelEncoder()
            return self.target_encoders[target_col].fit_transform(y.astype(str))
        else:
            return self.target_encoders[target_col].transform(y.astype(str))
    
    def _generate_oof_predictions(self, X, y, target_col):
        """
        Generate Out-of-Fold predictions for a single target.
        
        Args:
            X: Feature matrix
            y: Target array (encoded)
            target_col: Target column name
            
        Returns:
            OOF predictions array and trained models
        """
        n_classes = len(np.unique(y))
        n_samples = X.shape[0]
        
        # Initialize base models
        base_models_dict = self._get_base_models()
        n_base_models = len(base_models_dict)
        
        # OOF predictions array: [n_samples, n_base_models * n_classes]
        oof_predictions = np.zeros((n_samples, n_base_models * n_classes))
        
        # Store trained models for each fold
        trained_models = {name: [] for name in base_models_dict.keys()}
        
        # Stratified K-Fold split
        skf = StratifiedKFold(n_splits=self.n_folds, shuffle=True, random_state=42)
        
        print(f"\n{'='*70}")
        print(f"Generating OOF predictions for: {target_col}")
        print(f"{'='*70}")
        
        for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
            print(f"\nFold {fold + 1}/{self.n_folds}")
            print("-" * 50)
            
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]
            
            # Train each base model
            for model_idx, (model_name, model) in enumerate(base_models_dict.items()):
                print(f"  Training {model_name}...", end=" ")
                
                # Clone model for this fold
                if model_name == 'random_forest':
                    fold_model = RandomForestClassifier(**model.get_params())
                elif model_name == 'xgboost':
                    fold_model = xgb.XGBClassifier(**model.get_params())
                elif model_name == 'catboost':
                    fold_model = cb.CatBoostClassifier(**model.get_params())
                elif model_name == 'lightgbm':
                    fold_model = lgb.LGBMClassifier(**model.get_params())
                
                # Train model
                fold_model.fit(X_train, y_train)
                
                # Get probability predictions for validation set
                val_proba = fold_model.predict_proba(X_val)
                
                # Store OOF predictions
                start_col = model_idx * n_classes
                end_col = start_col + n_classes
                oof_predictions[val_idx, start_col:end_col] = val_proba
                
                # Calculate validation accuracy
                val_pred = np.argmax(val_proba, axis=1)
                val_acc = accuracy_score(y_val, val_pred)
                print(f"Accuracy: {val_acc:.4f}")
                
                # Store trained model
                trained_models[model_name].append(fold_model)
        
        # Handle AutoGluon separately (if available)
        if self.use_autogluon:
            print(f"\n{'='*70}")
            print(f"Training AutoGluon for: {target_col}")
            print(f"{'='*70}")
            
            # Prepare data for AutoGluon
            ag_train_data = X.copy()
            ag_train_data['target'] = y
            
            # AutoGluon OOF predictions
            ag_oof_predictions = np.zeros((n_samples, n_classes))
            trained_models['autogluon'] = []
            
            for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
                print(f"\nAutoGluon Fold {fold + 1}/{self.n_folds}")
                
                ag_train = ag_train_data.iloc[train_idx]
                ag_val = ag_train_data.iloc[val_idx]
                
                # Create predictor
                predictor = TabularPredictor(
                    label='target',
                    problem_type='multiclass',
                    eval_metric='accuracy',
                    verbosity=0
                ).fit(
                    train_data=ag_train,
                    time_limit=120,  # 2 minutes per fold
                    presets='medium_quality'
                )
                
                # Get predictions
                val_proba = predictor.predict_proba(ag_val.drop('target', axis=1))
                ag_oof_predictions[val_idx] = val_proba.values
                
                val_acc = accuracy_score(ag_val['target'], predictor.predict(ag_val.drop('target', axis=1)))
                print(f"  AutoGluon Accuracy: {val_acc:.4f}")
                
                trained_models['autogluon'].append(predictor)
            
            # Concatenate AutoGluon predictions
            oof_predictions = np.hstack([oof_predictions, ag_oof_predictions])
        
        return oof_predictions, trained_models
    
    def fit(self, X, y_dict):
        """
        Fit the multi-output stacking system.
        
        Args:
            X: Feature dataframe
            y_dict: Dictionary of target arrays {target_name: array}
        """
        print("\n" + "="*70)
        print("MULTI-OUTPUT OOF STACKING SYSTEM")
        print("="*70)
        
        # Encode features
        print("\nEncoding categorical features...")
        X_encoded = self._encode_features(X, fit=True)
        self.feature_columns = X_encoded.columns.tolist()
        
        # For each target, generate OOF predictions and train meta-learner
        for target_col in self.target_columns:
            if target_col not in y_dict:
                print(f"Warning: Target {target_col} not found in training data")
                continue
            
            # Encode target
            y_encoded = self._encode_targets(y_dict[target_col], target_col, fit=True)
            
            # Generate OOF predictions from base models
            oof_pred, trained_models = self._generate_oof_predictions(
                X_encoded, y_encoded, target_col
            )
            
            # Store base models
            self.base_models[target_col] = trained_models
            
            # Train meta-learner on OOF predictions
            print(f"\nTraining meta-learner for {target_col}...")
            meta_learner = lgb.LGBMClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.05,
                random_state=42,
                n_jobs=-1,
                verbose=-1
            )
            meta_learner.fit(oof_pred, y_encoded)
            self.meta_learners[target_col] = meta_learner
            
            # Evaluate on training data (OOF predictions)
            oof_pred_labels = meta_learner.predict(oof_pred)
            oof_accuracy = accuracy_score(y_encoded, oof_pred_labels)
            print(f"OOF Meta-learner Accuracy: {oof_accuracy:.4f}")
        
        print("\n" + "="*70)
        print("Training completed!")
        print("="*70)
    
    def predict(self, X):
        """
        Predict all targets for new data.
        
        Args:
            X: Feature dataframe
            
        Returns:
            Dictionary of predictions {target_name: predictions}
        """
        # Encode features
        X_encoded = self._encode_features(X, fit=False)
        
        predictions = {}
        
        for target_col in self.target_columns:
            if target_col not in self.base_models:
                continue
            
            n_samples = X_encoded.shape[0]
            base_models_dict = self.base_models[target_col]
            
            # Get number of classes
            n_classes = len(self.target_encoders[target_col].classes_)
            
            # Initialize prediction storage
            n_base_models = len([k for k in base_models_dict.keys() if k != 'autogluon'])
            meta_features = np.zeros((n_samples, n_base_models * n_classes))
            
            # Get predictions from each base model (average across folds)
            model_idx = 0
            for model_name in ['random_forest', 'xgboost', 'catboost', 'lightgbm']:
                if model_name in base_models_dict:
                    fold_models = base_models_dict[model_name]
                    
                    # Average predictions across folds
                    fold_probas = []
                    for fold_model in fold_models:
                        fold_probas.append(fold_model.predict_proba(X_encoded))
                    avg_proba = np.mean(fold_probas, axis=0)
                    
                    start_col = model_idx * n_classes
                    end_col = start_col + n_classes
                    meta_features[:, start_col:end_col] = avg_proba
                    model_idx += 1
            
            # Handle AutoGluon if available
            if self.use_autogluon and 'autogluon' in base_models_dict:
                ag_models = base_models_dict['autogluon']
                ag_probas = []
                for ag_model in ag_models:
                    ag_probas.append(ag_model.predict_proba(X_encoded).values)
                avg_ag_proba = np.mean(ag_probas, axis=0)
                meta_features = np.hstack([meta_features, avg_ag_proba])
            
            # Get meta-learner predictions
            meta_pred = self.meta_learners[target_col].predict(meta_features)
            
            # Decode predictions
            predictions[target_col] = self.target_encoders[target_col].inverse_transform(meta_pred)
        
        return predictions
    
    def evaluate(self, X, y_dict):
        """
        Evaluate model performance on test data.
        
        Args:
            X: Feature dataframe
            y_dict: Dictionary of true target arrays
            
        Returns:
            Dictionary of metrics
        """
        predictions = self.predict(X)
        
        metrics = {}
        
        print("\n" + "="*70)
        print("EVALUATION RESULTS")
        print("="*70)
        
        accuracies = []
        
        for target_col in self.target_columns:
            if target_col not in predictions or target_col not in y_dict:
                continue
            
            y_true = y_dict[target_col].astype(str)
            y_pred = predictions[target_col].astype(str) if hasattr(predictions[target_col], 'astype') else np.array(predictions[target_col]).astype(str)
            
            accuracy = accuracy_score(y_true, y_pred)
            f1_macro = f1_score(y_true, y_pred, average='macro', zero_division=0)
            
            accuracies.append(accuracy)
            
            metrics[target_col] = {
                'accuracy': accuracy,
                'f1_macro': f1_macro
            }
            
            print(f"\n{target_col}:")
            print(f"  Accuracy: {accuracy:.4f}")
            print(f"  Macro F1: {f1_macro:.4f}")
        
        # Overall average accuracy
        avg_accuracy = np.mean(accuracies)
        print(f"\n{'='*70}")
        print(f"OVERALL AVERAGE ACCURACY: {avg_accuracy:.4f}")
        print(f"{'='*70}")
        
        metrics['overall_accuracy'] = avg_accuracy
        
        return metrics
    
    def save(self, filepath):
        """
        Save the trained model to a file.
        
        Args:
            filepath: Path to save the model
        """
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
        print(f"\nModel saved to: {filepath}")
    
    @staticmethod
    def load(filepath):
        """
        Load a trained model from a file.
        
        Args:
            filepath: Path to the saved model
            
        Returns:
            Loaded MultiOutputOOFStacker instance
        """
        with open(filepath, 'rb') as f:
            model = pickle.load(f)
        print(f"Model loaded from: {filepath}")
        return model


def main():
    """
    Main execution function.
    """
    print("\n" + "="*70)
    print("FERTILIZER RECOMMENDATION SYSTEM")
    print("Multi-Output Classification with OOF Stacking")
    print("="*70)
    
    # Load dataset
    data_path = Path(__file__).parent / "Dataset.csv"
    print(f"\nLoading dataset from: {data_path}")
    df = pd.read_csv(data_path)
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Define features and targets
    feature_columns = [
        'Temperature', 'Humidity', 'Moisture', 'Soil_Type', 'Crop',
        'Nitrogen', 'Phosphorus', 'Potassium', 'pH', 'EC(mmhos/cm2)'
    ]
    
    target_columns = [
        'N_Status', 'P_Status', 'K_Status',
        'Primary_Fertilizer', 'Secondary_Fertilizer', 'pH_Amendment'
    ]
    
    # Separate features and targets
    X = df[feature_columns].copy()
    y_dict = {col: df[col].values for col in target_columns}
    
    # Train-test split (stratified on first target for simplicity)
    print("\nSplitting data into train (80%) and test (20%) sets...")
    X_train, X_test, y_train_first, y_test_first = train_test_split(
        X, y_dict['N_Status'],
        test_size=0.2,
        random_state=42,
        stratify=y_dict['N_Status']
    )
    
    # Get indices for splitting all targets
    train_indices = X_train.index
    test_indices = X_test.index
    
    # Create train and test dictionaries for all targets
    y_train_dict = {col: y_dict[col][train_indices] for col in target_columns}
    y_test_dict = {col: y_dict[col][test_indices] for col in target_columns}
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Initialize and train the stacking system
    stacker = MultiOutputOOFStacker(n_folds=5, use_autogluon=AUTOGLUON_AVAILABLE)
    
    print("\n" + "="*70)
    print("TRAINING PHASE")
    print("="*70)
    stacker.fit(X_train, y_train_dict)
    
    # Evaluate on test set
    print("\n" + "="*70)
    print("TESTING PHASE")
    print("="*70)
    metrics = stacker.evaluate(X_test, y_test_dict)
    
    # Save the model
    model_path = Path(__file__).parent / "stacked_model.pkl"
    stacker.save(model_path)
    
    # Display final summary
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print(f"Base Models Used: 4 (RF, XGBoost, CatBoost, LightGBM)")
    if AUTOGLUON_AVAILABLE:
        print("               + AutoGluon (AutoML)")
    print(f"Meta-Learner: LightGBM Classifier")
    print(f"Stacking Method: Out-of-Fold (OOF) Predictions")
    print(f"Number of Folds: 5")
    print(f"Target Variables: {len(target_columns)}")
    print(f"\nTest Set Performance:")
    for target_col in target_columns:
        if target_col in metrics:
            print(f"  {target_col}: {metrics[target_col]['accuracy']:.4f}")
    print(f"\nOverall Average Accuracy: {metrics['overall_accuracy']:.4f}")
    print("\n" + "="*70)
    print("Process completed successfully!")
    print("="*70)


if __name__ == "__main__":
    main()
