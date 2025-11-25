from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import joblib
from config import CONFIG

app = Flask(__name__)
app.config.from_object(CONFIG)
CORS(app, resources={r"/api/*": {"origins": CONFIG.CORS_ORIGINS}})

# Load the trained model and encoder
def _try_load_model(path='model.pkl'):
    try:
        m = joblib.load(path)
        print("Model loaded successfully from:", path)
        return m
    except Exception as e:
        print(f"Warning: Could not load model from '{path}': {e}")
        return None

def _try_load_encoder(path='encoder.pkl'):
    try:
        e = joblib.load(path)
        print("Encoder loaded successfully from:", path)
        return e
    except Exception as e:
        print(f"Warning: Could not load encoder from '{path}': {e}")
        return None

model = _try_load_model('model.pkl')
encoder = _try_load_encoder('encoder.pkl')

# Feature names in the correct order (excluding status_label, company_name, year)
FEATURE_NAMES = [
    'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10',
    'X11', 'X12', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18'
]

# Categorical features that need encoding (should match training data)
CATEGORICAL_FEATURES = ['X2', 'X9', 'X10', 'X15']  # Adjust based on your actual categorical features

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Ensure model and encoder are loaded
        if model is None:
            return jsonify({
                'error': 'Model not loaded. Create a model by running `python train_model.py` or place a valid `model.pkl` in the project root.'
            }), 503
        if encoder is None:
            return jsonify({
                'error': 'Encoder not loaded. Encoder file is required for this model.'
            }), 503
        
        data = request.json
        
        # Extract features in the correct order
        features = []
        for feature_name in FEATURE_NAMES:
            if feature_name not in data:
                return jsonify({'error': f'Missing feature: {feature_name}'}), 400
            try:
                features.append(float(data[feature_name]))
            except (ValueError, TypeError):
                return jsonify({'error': f'Invalid numeric value for {feature_name}'}), 400
        
        # Separate categorical and numeric features
        categorical_values = []
        numeric_values = []
        
        for i, feature_name in enumerate(FEATURE_NAMES):
            if feature_name in CATEGORICAL_FEATURES:
                categorical_values.append([data[feature_name]])
            else:
                numeric_values.append(features[i])
        
        # Encode categorical features
        if categorical_values:
            cat_encoded = encoder.transform(categorical_values)
        else:
            cat_encoded = np.array([]).reshape(1, -1)
        
        # Combine encoded categorical + numeric features
        X = np.hstack([cat_encoded, np.array(numeric_values).reshape(1, -1)])
        
        # Make prediction
        raw_prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0]
        
        # Get model classes
        classes = list(model.classes_)
        
        # Determine bankruptcy probability (assuming class 1 is bankruptcy/failed)
        bankruptcy_index = 1 if len(classes) > 1 else 0
        bankruptcy_prob = float(probability[bankruptcy_index]) * 100
        healthy_prob = 100.0 - bankruptcy_prob
        
        # Interpret prediction
        is_bankrupt = (raw_prediction == 1)
        
        result = {
            'prediction': 'Bankrupt' if is_bankrupt else 'Healthy',
            'bankruptcy_risk': round(bankruptcy_prob, 2),
            'healthy_probability': round(healthy_prob, 2),
            'confidence': round(max(bankruptcy_prob, healthy_prob), 2),
            'raw_prediction': str(raw_prediction),
            'model_classes': classes
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'Prediction failed. See server logs for details.'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model_loaded': model is not None, 'encoder_loaded': encoder is not None}), 200

if __name__ == '__main__':
    # Running on port 5001 to avoid conflict with port 5000 from previous session
    app.run(debug=True, port=5001)
