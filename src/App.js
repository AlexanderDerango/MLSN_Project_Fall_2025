import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import PredictionForm from './components/PredictionForm';
import ResultsDisplay from './components/ResultsDisplay';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post('http://localhost:5000/api/predict', formData);
      setResult(response.data);
    } catch (err) {
      setError(
        err.response?.data?.error ||
        'Error making prediction. Please ensure the backend server is running.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Bankruptcy Risk Predictor</h1>
        <p className="subtitle">Analyze company financial metrics to predict bankruptcy risk</p>
      </header>

      <main className="app-main">
        <div className="container">
          {!result ? (
            <>
              <PredictionForm onSubmit={handleSubmit} isLoading={loading} />
              {error && <div className="error-message">{error}</div>}
            </>
          ) : (
            <>
              <ResultsDisplay result={result} />
              <button className="btn-primary" onClick={handleReset}>
                Analyze Another Company
              </button>
            </>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>&copy; 2025 Machine Learning and Systems for Network. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
