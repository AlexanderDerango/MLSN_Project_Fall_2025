from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
import joblib
from config import CONFIG

app = Flask(__name__)
app.config.from_object(CONFIG)
CORS(app, resources={r"/api/*": {"origins": CONFIG.CORS_ORIGINS}})

# Load the trained model
def _try_load_model(path='model.pkl'):
    try:
        m = joblib.load(path)
        print("Model loaded successfully from:", path)
        return m
    except Exception as e:
        # Print exception details to help debugging when model fails to load
        print(f"Warning: Could not load model from '{path}': {e}")
        return None

model = _try_load_model('model.pkl')

# Feature names in the correct order
FEATURE_NAMES = [
    'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10',
    'X11', 'X12', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18'
]

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Ensure model is loaded before attempting to predict
        if model is None:
            return jsonify({
                'error': 'Model not loaded. Create a model by running `python train_model.py` or place a valid `model.pkl` in the project root.'
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
        
        # Convert to numpy array and reshape for prediction
        X = np.array(features).reshape(1, -1)
        
        # Make prediction
        raw_prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0]

        # Determine which class index corresponds to 'bankrupt'/failed label
        # Handle common label encodings (numeric 0/1 or strings like 'failed')
        bankruptcy_index = None
        try:
            classes = list(model.classes_)
        except Exception:
            classes = []

        candidates = [1, 'failed', 'Failed', 'FAILED', 'bankrupt', 'Bankrupt', 'BANKRUPT']
        for idx, cls in enumerate(classes):
            if cls in candidates:
                bankruptcy_index = idx
                break

        # Fallbacks: if not found, try numeric mapping (assume 1 means bankrupt)
        if bankruptcy_index is None:
            try:
                # find index where class == 1
                bankruptcy_index = int(np.where(np.array(classes) == 1)[0])
            except Exception:
                # default to index 1 if there are two classes
                bankruptcy_index = 1 if len(classes) > 1 else 0

        # Now compute probabilities using the discovered index
        bankruptcy_prob = float(probability[bankruptcy_index]) * 100
        healthy_prob = 100.0 - bankruptcy_prob

        # Interpret raw prediction using the discovered class mapping
        predicted_label = raw_prediction
        is_bankrupt = False
        try:
            is_bankrupt = (predicted_label == classes[bankruptcy_index])
        except Exception:
            # If classes mapping isn't available, fall back to numeric check
            try:
                is_bankrupt = (int(predicted_label) == 1)
            except Exception:
                is_bankrupt = False

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
        # Return a helpful error message and log exception
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'Prediction failed. See server logs for details.'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model_loaded': model is not None}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
