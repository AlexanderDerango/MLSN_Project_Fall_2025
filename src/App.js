import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import PredictionForm from './components/PredictionForm';
import ResultsDisplay from './components/ResultsDisplay';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    const stored = localStorage.getItem('bp_theme');
    if (stored) setTheme(stored);
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('bp_theme', theme);
  }, [theme]);

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
        <div className="header-row">
          <div>
            <h1>Bankruptcy Risk Predictor</h1>
            <p className="subtitle">Analyze company financial metrics to predict bankruptcy risk</p>
          </div>
          <div className="header-controls">
            <button
              className="theme-toggle"
              onClick={() => setTheme(prev => (prev === 'light' ? 'dark' : 'light'))}
              aria-label="Toggle theme"
            >
              {theme === 'light' ? '🌙 Dark' : '☀️ Light'}
            </button>
          </div>
        </div>
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
    </div>
  );
}

export default App;
