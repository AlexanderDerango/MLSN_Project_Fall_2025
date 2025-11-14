import React from 'react';
import './ResultsDisplay.css';

const ResultsDisplay = ({ result }) => {
  const isBankrupt = result.prediction === 'Bankrupt';
  const riskLevel = result.bankruptcy_risk > 70 ? 'High' : result.bankruptcy_risk > 40 ? 'Medium' : 'Low';

  return (
    <div className="results-container">
      <div className={`results-card ${isBankrupt ? 'bankrupt' : 'healthy'}`}>
        <div className="results-header">
          <h2>Prediction Result</h2>
        </div>

        <div className="prediction-status">
          <div className={`status-indicator ${isBankrupt ? 'bankrupt' : 'healthy'}`}>
            {isBankrupt ? '⚠' : '✓'}
          </div>
          <div className="status-text">
            <h3>{result.prediction}</h3>
            <p className={`risk-level ${riskLevel.toLowerCase()}`}>
              Risk Level: <strong>{riskLevel}</strong>
            </p>
          </div>
        </div>

        <div className="results-details">
          <div className="detail-item">
            <span className="detail-label">Bankruptcy Risk:</span>
            <span className="detail-value">{result.bankruptcy_risk}%</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Healthy Probability:</span>
            <span className="detail-value">{result.healthy_probability}%</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Prediction Confidence:</span>
            <span className="detail-value">{result.confidence}%</span>
          </div>
        </div>

        <div className="probability-chart">
          <div className="chart-label">Probability Distribution</div>
          <div className="bar-container">
            <div className="bar-item">
              <div className="bar-label">Healthy</div>
              <div className="bar-wrapper">
                <div 
                  className="bar healthy-bar" 
                  style={{ width: `${result.healthy_probability}%` }}
                >
                  <span className="bar-value">{result.healthy_probability}%</span>
                </div>
              </div>
            </div>
            <div className="bar-item">
              <div className="bar-label">Bankrupt</div>
              <div className="bar-wrapper">
                <div 
                  className="bar bankrupt-bar" 
                  style={{ width: `${result.bankruptcy_risk}%` }}
                >
                  <span className="bar-value">{result.bankruptcy_risk}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className={`interpretation ${isBankrupt ? 'alert' : 'success'}`}>
          {isBankrupt ? (
            <>
              <h4>⚠️ Warning</h4>
              <p>
                This company shows signs of potential financial distress. 
                A thorough financial review and expert analysis is recommended 
                before making any investment or business decisions.
              </p>
            </>
          ) : (
            <>
              <h4>✓ Positive Outlook</h4>
              <p>
                Based on the financial metrics provided, this company appears 
                to be in a healthier financial position. However, continued 
                monitoring of financial performance is always recommended.
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;
