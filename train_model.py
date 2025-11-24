"""
Script to train and save the Gradient Boosting model
Run this after preparing your training data (train.csv should exist)
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
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
    X_train = train.drop(columns=drop_cols)
    y_train = train[target_col]
    
    X_val = val.drop(columns=drop_cols)
    y_val = val[target_col]
    
    X_test = test.drop(columns=drop_cols)
    y_test = test[target_col]
    
    # Identify categorical and numeric columns
    categorical_features = X_train.select_dtypes(include=['object', 'category']).columns
    
    # Create preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough'
    )
    
    # Create and train model with SMOTE for class imbalance
    gb_clf = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.2,
        max_depth=2,
        random_state=42,
        verbose=1  # Show progress
    )
    
    # Use imbalanced-learn Pipeline to apply SMOTE before classifier
    # This balances the training data by oversampling the minority class
    smote = SMOTE(random_state=42, k_neighbors=5)
    
    pipeline = ImbPipeline(steps=[
        ('preprocessor', preprocessor),
        ('smote', smote),
        ('classifier', gb_clf)
    ])
    
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    val_preds = pipeline.predict(X_val)
    test_preds = pipeline.predict(X_test)
    
    val_accuracy = accuracy_score(y_val, val_preds)
    test_accuracy = accuracy_score(y_test, test_preds)
    
    print(f"\nValidation Accuracy: {val_accuracy:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print("\nClassification Report (Test):")
    print(classification_report(y_test, test_preds))
    print("\nConfusion Matrix (Test):")
    print(confusion_matrix(y_test, test_preds))
    
    # Save model
    joblib.dump(pipeline, 'model.pkl')
    print("\nModel saved to model.pkl")

if __name__ == "__main__":
    train_model()
