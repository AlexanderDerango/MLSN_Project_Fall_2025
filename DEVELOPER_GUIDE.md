# Developer Guide

## Project Architecture

### Directory Structure

```
MLSN_Project_Fall_2025/
│
├── Backend (Python/Flask)
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration management
│   ├── train_model.py      # Model training script
│   ├── requirements.txt    # Python dependencies
│   └── model.pkl          # Trained model (generated)
│
├── Frontend (React/JavaScript)
│   ├── public/
│   │   └── index.html     # HTML template
│   ├── src/
│   │   ├── index.js       # React entry point
│   │   ├── index.css      # Global styles
│   │   ├── App.js         # Root component
│   │   ├── App.css        # App styles
│   │   └── components/
│   │       ├── PredictionForm.js
│   │       ├── PredictionForm.css
│   │       ├── ResultsDisplay.js
│   │       └── ResultsDisplay.css
│   ├── package.json       # NPM dependencies
│   └── .env              # Environment variables (optional)
│
└── Documentation
    ├── README.md          # Main documentation
    ├── QUICK_START.md     # Quick setup guide
    ├── DEPLOYMENT.md      # Deployment guide
    ├── PROJECT_COMPLETION.md  # Completion summary
    └── DEVELOPER_GUIDE.md # This file
```

## Backend Development

### Flask Application (app.py)

**Key Components:**

1. **Imports & Configuration**
   ```python
   from flask import Flask, request, jsonify
   from flask_cors import CORS
   import joblib
   from config import CONFIG
   ```

2. **Model Loading**
   - Loads pre-trained model from `model.pkl`
   - Gracefully handles missing model with warning

3. **API Endpoints**
   - `POST /api/predict` - Makes predictions
   - `GET /api/health` - Health check endpoint

4. **CORS Configuration**
   - Configured to allow requests from frontend
   - Configurable via CONFIG object

### Configuration (config.py)

Three configurations available:
- **DevelopmentConfig**: Debug enabled, all CORS origins
- **ProductionConfig**: Debug disabled, restricted CORS
- **TestingConfig**: Testing mode with relaxed settings

Set via environment variable:
```bash
export FLASK_ENV=production  # or development/testing
```

### Model Training (train_model.py)

**Process:**
1. Load training/validation/test data
2. Preprocess categorical features
3. Train Gradient Boosting Classifier
4. Evaluate on validation and test sets
5. Save model to `model.pkl` using joblib

**Usage:**
```bash
python train_model.py
```

**Requirements:**
- `train.csv`, `validation.csv`, `test.csv` in project root
- Columns: `status_label` (target), `company_name`, `year`, X1-X18 (features)

## Frontend Development

### React Structure

**App.js** - Root component that:
- Manages form submission and results state
- Handles API calls via Axios
- Renders either form or results
- Manages error states

**PredictionForm.js** - Input form that:
- Displays 18 input fields in responsive grid
- Provides expandable field descriptions
- Validates input data
- Submits data to backend

**ResultsDisplay.js** - Results component that:
- Shows prediction result (Bankrupt/Healthy)
- Displays risk level classification
- Visualizes probabilities with bar charts
- Provides interpretation and recommendations

### Styling Approach

- **CSS Grid & Flexbox** for layout
- **Responsive Design**: Mobile-first approach
- **Animations**: Smooth transitions and fade-ins
- **Color Scheme**: Purple/blue gradient
- **Media Queries**: Breakpoints at 768px

### Component Communication

```
App.js
├── state: result, loading, error
├── handlers: handleSubmit, handleReset
│
├─→ PredictionForm.js (when no result)
│   └─ calls: onSubmit(formData)
│
└─→ ResultsDisplay.js (when result exists)
    └─ displays: result data
```

## API Specification

### Prediction Endpoint

**URL:** `POST /api/predict`

**Request Body:**
```json
{
  "X1": 1000000,
  "X2": 500000,
  "X3": 50000,
  "X4": 100000,
  "X5": 200000,
  "X6": 50000,
  "X7": 150000,
  "X8": 5000000,
  "X9": 2000000,
  "X10": 5000000,
  "X11": 500000,
  "X12": 150000,
  "X13": 600000,
  "X14": 300000,
  "X15": 800000,
  "X16": 3000000,
  "X17": 1500000,
  "X18": 500000
}
```

**Response (200 OK):**
```json
{
  "prediction": "Healthy",
  "bankruptcy_risk": 15.23,
  "healthy_probability": 84.77,
  "confidence": 84.77
}
```

**Error Response (400/500):**
```json
{
  "error": "Missing feature: X1"
}
```

### Health Check Endpoint

**URL:** `GET /api/health`

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true
}
```

## Development Workflow

### Setup Development Environment

```bash
# Backend
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
npm install
```

### Running Locally

```bash
# Terminal 1: Backend
python app.py
# Opens: http://localhost:5000

# Terminal 2: Frontend
npm start
# Opens: http://localhost:3000
```

### Making Changes

**Backend Changes:**
1. Edit `app.py` or related files
2. Flask will auto-reload in debug mode
3. Test via `curl` or frontend UI

**Frontend Changes:**
1. Edit React components in `src/`
2. React dev server auto-reloads
3. Changes visible immediately in browser

### Testing Workflow

**Manual Testing:**
1. Start both servers
2. Use frontend UI to submit predictions
3. Check browser console (F12) for errors
4. Check terminal output for backend logs

**API Testing with curl:**
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "X1": 1000000,
    "X2": 500000,
    ...
  }'
```

## Common Tasks

### Adding a New Feature

**Example: Add prediction confidence indicator**

1. **Backend** (`app.py`):
   ```python
   # Already returns confidence in result
   ```

2. **Frontend** (`ResultsDisplay.js`):
   ```jsx
   <div className="confidence-indicator">
     {result.confidence}%
   </div>
   ```

3. **Styling** (`ResultsDisplay.css`):
   ```css
   .confidence-indicator {
     /* styles */
   }
   ```

### Modifying Validation

**Change required field validation:**

In `PredictionForm.js`:
```javascript
// Add validation before submit
if (numericValue < 0) {
  alert('Values must be positive');
  return;
}
```

### Updating Dependencies

**Backend:**
```bash
pip install --upgrade package-name
pip freeze > requirements.txt
```

**Frontend:**
```bash
npm install package-name
# Updates package.json automatically
```

## Debugging Tips

### Backend Debugging

```python
# Add print statements
print(f"Received data: {data}")

# Use Flask debug mode (automatic with DEBUG=True)
# Detailed error messages in console

# Check logs
# All requests printed to terminal
```

### Frontend Debugging

```javascript
// Browser console (F12)
console.log('Form data:', formData);
console.error('API error:', error);

// React DevTools
// Install React DevTools browser extension

// Network tab (F12)
// Check API requests and responses
```

### Common Issues

**CORS Error:** Backend and frontend on different ports?
- Solution: Ensure CORS is enabled in `app.py`

**Model not loading:** `model.pkl` missing?
- Solution: Run `python train_model.py` first

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

## Performance Optimization

### Backend
- Use production WSGI server (Gunicorn)
- Implement caching for model predictions
- Add request rate limiting
- Optimize numpy operations

### Frontend
- Lazy load components
- Memoize expensive computations
- Optimize CSS (minimize animations)
- Use production build for deployment

## Security Considerations

1. **Input Validation**: All fields validated
2. **CORS**: Restricted to known origins in production
3. **Error Handling**: No sensitive info in errors
4. **Model**: Keep `model.pkl` secure
5. **Environment**: Use `.env` for sensitive data

## Deployment Checklist

- [ ] Model trained and tested (93% accuracy)
- [ ] All dependencies in `requirements.txt`
- [ ] All npm packages in `package.json`
- [ ] Frontend built: `npm run build`
- [ ] Environment variables configured
- [ ] CORS origins updated for production
- [ ] Error logging configured
- [ ] Performance optimized
- [ ] Documentation updated
- [ ] Git repository clean

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Axios Documentation](https://axios-http.com/)

## Contributing Guidelines

1. Create feature branch: `git checkout -b feature/feature-name`
2. Make changes with clear commits
3. Test thoroughly
4. Update documentation
5. Create pull request with description

---

**Happy developing!** 🚀
