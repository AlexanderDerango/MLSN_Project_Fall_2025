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
try:
    model = joblib.load('model.pkl')
    print("Model loaded successfully")
except:
    print("Warning: Model not found. Please train and save the model first.")
    model = None

# Feature names in the correct order
FEATURE_NAMES = [
    'X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10',
    'X11', 'X12', 'X13', 'X14', 'X15', 'X16', 'X17', 'X18'
]

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Extract features in the correct order
        features = []
        for feature_name in FEATURE_NAMES:
            if feature_name not in data:
                return jsonify({'error': f'Missing feature: {feature_name}'}), 400
            try:
                features.append(float(data[feature_name]))
            except ValueError:
                return jsonify({'error': f'Invalid value for {feature_name}'}), 400
        
        # Convert to numpy array and reshape for prediction
        X = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(X)[0]
        probability = model.predict_proba(X)[0]
        
        # Interpret results
        bankruptcy_prob = probability[1] * 100  # Probability of bankruptcy
        healthy_prob = probability[0] * 100      # Probability of being healthy
        
        result = {
            'prediction': 'Bankrupt' if prediction == 1 else 'Healthy',
            'bankruptcy_risk': round(bankruptcy_prob, 2),
            'healthy_probability': round(healthy_prob, 2),
            'confidence': round(max(bankruptcy_prob, healthy_prob), 2)
        }
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model_loaded': model is not None}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
