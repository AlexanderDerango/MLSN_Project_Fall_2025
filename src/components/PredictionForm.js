import React, { useState } from 'react';
import './PredictionForm.css';

const PredictionForm = ({ onSubmit, isLoading }) => {
  const [formData, setFormData] = useState({
    X1: '',
    X2: '',
    X3: '',
    X4: '',
    X5: '',
    X6: '',
    X7: '',
    X8: '',
    X9: '',
    X10: '',
    X11: '',
    X12: '',
    X13: '',
    X14: '',
    X15: '',
    X16: '',
    X17: '',
    X18: ''
  });

  const [expandedField, setExpandedField] = useState(null);

  const fieldDescriptions = {
    X1: {
      name: 'Current Assets',
      description: 'All the assets of a company that are expected to be sold or used as a result of standard business operations over the next year'
    },
    X2: {
      name: 'Cost of Goods Sold',
      description: 'The total amount a company paid as a cost directly related to the sale of products'
    },
    X3: {
      name: 'Depreciation & Amortization',
      description: 'Depreciation refers to the loss of value of a tangible fixed asset over time (such as property, machinery, buildings, and plant). Amortization refers to the loss of value of intangible assets over time.'
    },
    X4: {
      name: 'EBITDA',
      description: 'Earnings before interest, taxes, depreciation, and amortization. A measure of a company\'s overall financial performance alternative to net income'
    },
    X5: {
      name: 'Inventory',
      description: 'The accounting of items and raw materials that a company either uses in production or sells'
    },
    X6: {
      name: 'Net Income',
      description: 'The overall profitability of a company after all expenses and costs have been deducted from total revenue'
    },
    X7: {
      name: 'Total Receivables',
      description: 'The balance of money due to a firm for goods or services delivered or used but not yet paid for by customers'
    },
    X8: {
      name: 'Market Value',
      description: 'The price of an asset in a marketplace. In our dataset, it refers to the market capitalization since companies are publicly traded in the stock market'
    },
    X9: {
      name: 'Net Sales',
      description: 'The sum of a company\'s gross sales minus its returns, allowances, and discounts'
    },
    X10: {
      name: 'Total Assets',
      description: 'All the assets, or items of value, a business owns'
    },
    X11: {
      name: 'Total Long-term Debt',
      description: 'A company\'s loans and other liabilities that will not become due within one year of the balance sheet date'
    },
    X12: {
      name: 'EBIT',
      description: 'Earnings before interest and taxes'
    },
    X13: {
      name: 'Gross Profit',
      description: 'The profit a business makes after subtracting all the costs that are related to manufacturing and selling its products or services'
    },
    X14: {
      name: 'Total Current Liabilities',
      description: 'The sum of accounts payable, accrued liabilities, and taxes such as bonds payable at the end of the year, salaries, and commissions remaining'
    },
    X15: {
      name: 'Retained Earnings',
      description: 'The amount of profit a company has left over after paying all its direct costs, indirect costs, income taxes, and dividends to shareholders'
    },
    X16: {
      name: 'Total Revenue',
      description: 'The amount of income that a business has made from all sales before subtracting expenses. It may include interest and dividends from investments'
    },
    X17: {
      name: 'Total Liabilities',
      description: 'The combined debts and obligations that the company owes to outside parties'
    },
    X18: {
      name: 'Total Operating Expenses',
      description: 'The expense a business incurs through its normal business operations'
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validate all fields are filled
    const allFilled = Object.values(formData).every(val => val !== '');
    if (!allFilled) {
      alert('Please fill in all fields');
      return;
    }

    // Convert to numbers
    const numericData = {};
    Object.keys(formData).forEach(key => {
      numericData[key] = parseFloat(formData[key]);
    });

    onSubmit(numericData);
  };

  const handleReset = () => {
    setFormData({
      X1: '',
      X2: '',
      X3: '',
      X4: '',
      X5: '',
      X6: '',
      X7: '',
      X8: '',
      X9: '',
      X10: '',
      X11: '',
      X12: '',
      X13: '',
      X14: '',
      X15: '',
      X16: '',
      X17: '',
      X18: ''
    });
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} className="prediction-form">
        <div className="form-intro">
          <h2>Enter Company Financial Data</h2>
          <p>Please provide the following financial metrics to assess bankruptcy risk</p>
        </div>

        <div className="form-grid">
          {Object.keys(fieldDescriptions).map((fieldKey) => (
            <div key={fieldKey} className="form-field">
              <div className="field-input-wrapper">
                <label htmlFor={fieldKey}>
                  <span className="field-code">{fieldKey}</span>
                  <span className="field-name">{fieldDescriptions[fieldKey].name}</span>
                  <span 
                    className="info-icon"
                    onClick={() => setExpandedField(expandedField === fieldKey ? null : fieldKey)}
                  >
                    ⓘ
                  </span>
                </label>
                <input
                  type="number"
                  id={fieldKey}
                  name={fieldKey}
                  value={formData[fieldKey]}
                  onChange={handleChange}
                  placeholder="Enter value"
                  step="any"
                  required
                  className="field-input"
                />
              </div>
              {expandedField === fieldKey && (
                <div className="field-description">
                  {fieldDescriptions[fieldKey].description}
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="form-actions">
          <button
            type="submit"
            className="btn-primary"
            disabled={isLoading}
          >
            {isLoading ? 'Analyzing...' : 'Predict Bankruptcy Risk'}
          </button>
          <button
            type="button"
            className="btn-secondary"
            onClick={handleReset}
            disabled={isLoading}
          >
            Clear All
          </button>
        </div>
      </form>
    </div>
  );
};

export default PredictionForm;
