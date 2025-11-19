"""create_stub_model.py

Creates a small dummy sklearn model and saves it as `model.pkl` so the API
can be run for UI/integration testing without the real training data.

The dummy model will accept 18 numeric features and return a probability
vector for two classes (healthy=0, bankrupt=1).

Usage:
    python create_stub_model.py
"""
import numpy as np
from sklearn.dummy import DummyClassifier
import joblib

# Build a dummy classifier that predicts class 0 (Healthy) most of the time
clf = DummyClassifier(strategy='constant', constant=0)

# Fit the classifier on tiny synthetic data with 18 features
X_train = np.array([
    [0.0]*18,
    [1.0]*18
])
y_train = np.array([0, 1])

clf.fit(X_train, y_train)

# Save the model
joblib.dump(clf, 'model.pkl')
print('Saved stub model to model.pkl')
