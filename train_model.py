"""
Script to train and save the Random Forest model
Run this after preparing your training data (train.csv should exist)
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, balanced_accuracy_score
import joblib

def train_model():
    # Load training data
    try:
        train = pd.read_csv("train.csv")
        val = pd.read_csv("validation.csv")
        test = pd.read_csv("test.csv")
    except FileNotFoundError:
        print("Error: train.csv, validation.csv, or test.csv not found!")
        print("Please ensure you have run the data preparation notebook first.")
        return
    
    target_col = 'status_label'
    
    # Drop target + irrelevant columns
    drop_cols = [target_col, 'company_name', 'year']
    x_tr = train.drop(columns=drop_cols)
    y_tr = train[target_col]
    
    x_va = val.drop(columns=drop_cols)
    y_va = val[target_col]
    
    x_te = test.drop(columns=drop_cols)
    y_te = test[target_col]
    
    # One-hot encode categorical features
    categorical_features = x_tr.select_dtypes(include=['object', 'category']).columns.tolist()
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    
    # Fit encoder on training data
    x_tr_encoded = encoder.fit_transform(x_tr[categorical_features])
    x_va_encoded = encoder.transform(x_va[categorical_features])
    x_te_encoded = encoder.transform(x_te[categorical_features])
    
    # Get numeric features
    numeric_features = x_tr.select_dtypes(include=[np.number]).columns.tolist()
    
    # Combine encoded categorical + numeric features
    x_tr = np.hstack([x_tr_encoded, x_tr[numeric_features].values])
    x_va = np.hstack([x_va_encoded, x_va[numeric_features].values])
    x_te = np.hstack([x_te_encoded, x_te[numeric_features].values])
    
    # Train Random Forest model
    rf = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=20,
        min_samples_leaf=10,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    
    print("Training model...")
    rf.fit(x_tr, y_tr)
    
    # Get predictions and probabilities
    proba_va = rf.predict_proba(x_va)[:, 1]
    proba_te = rf.predict_proba(x_te)[:, 1]
    
    val_preds = rf.predict(x_va)
    test_preds = rf.predict(x_te)
    
    # Evaluate
    val_accuracy = accuracy_score(y_va, val_preds)
    test_accuracy = accuracy_score(y_te, test_preds)
    
    print(f"\nModel Training (n=200):")
    print(f"Validation ROC AUC: {roc_auc_score(y_va, proba_va):.4f}")
    print(f"Validation Accuracy: {val_accuracy:.4f}")
    print(f"Validation Balanced Accuracy: {balanced_accuracy_score(y_va, val_preds):.4f}")
    
    print(f"\nTest ROC AUC: {roc_auc_score(y_te, proba_te):.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Test Balanced Accuracy: {balanced_accuracy_score(y_te, test_preds):.4f}")
    
    print("\nClassification Report (Test):")
    print(classification_report(y_te, test_preds))
    print("\nConfusion Matrix (Test):")
    print(confusion_matrix(y_te, test_preds))
    
    # Save model and encoder
    joblib.dump(rf, 'model.pkl')
    joblib.dump(encoder, 'encoder.pkl')
    print("\nModel saved to model.pkl")
    print("Encoder saved to encoder.pkl")

if __name__ == "__main__":
    train_model()
