"""
Evaluate the saved model (model.pkl) on test.csv and print diagnostics.

Outputs:
 - Class distribution in test labels
 - Classification report + confusion matrix
 - Mean predicted probability for each class
 - Example predictions
 - If available: top feature importances (indices)

Usage:
    python evaluate_model.py
"""
import pandas as pd
import numpy as np
import joblib
import sys
from sklearn.metrics import classification_report, confusion_matrix

MODEL_PATH = 'model.pkl'
TEST_PATH = 'test.csv'
TARGET_COL = 'status_label'


def load_model(path):
    try:
        m = joblib.load(path)
        print(f"Loaded model from {path}")
        return m
    except Exception as e:
        print(f"Error loading model from {path}: {e}")
        return None


def load_test(path):
    try:
        df = pd.read_csv(path)
        print(f"Loaded test data from {path} ({len(df)} rows)")
        return df
    except Exception as e:
        print(f"Error loading test data from {path}: {e}")
        return None


def main():
    model = load_model(MODEL_PATH)
    if model is None:
        print('Model not available. Run train_model.py or place model.pkl in project root.')
        sys.exit(1)

    df = load_test(TEST_PATH)
    if df is None:
        print('Test data not available. Create test.csv using create_splits.py')
        sys.exit(1)

    if TARGET_COL not in df.columns:
        print(f"Target column '{TARGET_COL}' not found in test data columns: {df.columns.tolist()}")
        # Try to infer target column
        sys.exit(1)

    drop_cols = [TARGET_COL, 'company_name', 'year']
    X_test = df.drop(columns=[c for c in drop_cols if c in df.columns])
    y_test = df[TARGET_COL]

    # Basic class distribution
    print('\nClass distribution in test set:')
    print(y_test.value_counts(dropna=False))

    # Predictions
    try:
        preds = model.predict(X_test)
    except Exception as e:
        print(f"Error during model.predict: {e}")
        # Try to transform using pipeline separately
        sys.exit(1)

    # Predict proba if available
    proba = None
    if hasattr(model, 'predict_proba'):
        try:
            proba = model.predict_proba(X_test)
        except Exception as e:
            print(f"Model has predict_proba but failed: {e}")
            proba = None

    print('\nClassification report:')
    print(classification_report(y_test, preds))

    print('Confusion matrix:')
    print(confusion_matrix(y_test, preds))

    if proba is not None:
        # assume binary classification with columns [P(class0), P(class1)]
        if proba.shape[1] >= 2:
            p0 = proba[:, 0].mean() * 100
            p1 = proba[:, 1].mean() * 100
            print(f"\nMean predicted probability - class 0: {p0:.2f}%, class 1: {p1:.2f}%")
            # Show distribution
            print('\nPredicted probability percentiles for class 1:')
            print(np.percentile(proba[:, 1], [0, 10, 25, 50, 75, 90, 100]))

    # Show some example rows where model predicted healthy but true is bankrupt
    try:
        df_examples = df.copy()
        df_examples['pred'] = preds
        if proba is not None and proba.shape[1] >= 2:
            df_examples['prob_bankrupt'] = proba[:, 1]
        else:
            df_examples['prob_bankrupt'] = np.nan

        mismatch = df_examples[df_examples['pred'] == 0][df_examples[TARGET_COL] == 1]
        print(f"\nNumber of false negatives (predicted healthy but actually bankrupt): {len(mismatch)}")
        if len(mismatch) > 0:
            print('Show up to 5 false negative examples (first columns):')
            print(mismatch.head(5).iloc[:, :8].to_string(index=False))
    except Exception as e:
        print(f"Error while inspecting examples: {e}")

    # Feature importances if available
    try:
        # If pipeline: try to access classifier
        classifier = None
        if hasattr(model, 'named_steps'):
            # common pipeline name
            if 'classifier' in model.named_steps:
                classifier = model.named_steps['classifier']
            else:
                # try last step
                classifier = list(model.named_steps.values())[-1]
        else:
            classifier = model

        if hasattr(classifier, 'feature_importances_'):
            importances = classifier.feature_importances_
            # Report top 10 indices
            sorted_idx = np.argsort(importances)[::-1]
            topk = min(10, len(importances))
            print(f"\nTop {topk} feature importance indices (index:importance):")
            for i in range(topk):
                idx = sorted_idx[i]
                print(f"  {idx}: {importances[idx]:.6f}")
        else:
            print('\nModel does not expose feature_importances_. Skipping importance check.')
    except Exception as e:
        print(f"Error while computing feature importances: {e}")

    print('\nEvaluation script finished.')


if __name__ == '__main__':
    main()
