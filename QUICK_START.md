# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)

```bash
# Install Python packages
pip install -r requirements.txt

# Install Node packages
npm install
```

### Step 2: Start the Backend (1 minute)

**Open a terminal/PowerShell and run:**
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 3: Start the Frontend (1 minute)

**Open another terminal/PowerShell and run:**
```bash
npm start
```

The browser will automatically open at `http://localhost:3000`

## That's It! 🎉

You now have:
- ✅ Flask backend running on port 5000
- ✅ React frontend running on port 3000
- ✅ Ready to make predictions

## First Prediction Test

1. Fill in any financial data values
2. Click "Predict Bankruptcy Risk"
3. See the results!

## Need Help?

- **Backend won't start?** Make sure you ran `pip install -r requirements.txt`
- **Frontend won't start?** Make sure you ran `npm install`
- **Connection error?** Make sure both servers are running
- **Model not found?** You need to train it first with `python train_model.py` (requires training data)

## Production Deployment

### Backend (Flask)

For production, use Gunicorn instead of Flask's built-in server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend (React)

Build the production bundle:

```bash
npm run build
```

This creates an optimized build in the `build/` folder.

## Troubleshooting Checklist

- [ ] Both terminals are open and running
- [ ] Backend shows "Running on http://127.0.0.1:5000"
- [ ] Frontend shows "compiled successfully"
- [ ] Browser is on http://localhost:3000
- [ ] All 18 form fields have numeric values
- [ ] Flask CORS is working (no cross-origin errors in browser console)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   React Frontend (Port 3000)             │
│                  (Beautiful UI, Form, Results)           │
└────────────────────────┬────────────────────────────────┘
                         │
                    HTTP/CORS
                         │
┌────────────────────────▼────────────────────────────────┐
│                  Flask Backend (Port 5000)               │
│     (Loads Model, Makes Predictions, Returns Results)   │
└─────────────────────────────────────────────────────────┘
                         │
                         │
┌────────────────────────▼────────────────────────────────┐
│              Trained ML Model (model.pkl)                │
│        (Gradient Boosting, 93% Accuracy)                │
└─────────────────────────────────────────────────────────┘
```

## File Overview

| File | Purpose |
|------|---------|
| `app.py` | Flask REST API server |
| `train_model.py` | Script to train and save the model |
| `requirements.txt` | Python dependencies |
| `package.json` | React dependencies |
| `src/App.js` | Main React component |
| `src/components/PredictionForm.js` | Input form component |
| `src/components/ResultsDisplay.js` | Results visualization |
| `src/*.css` | Styling |

Enjoy! 🚀
