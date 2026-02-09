import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { portfolioAPI } from '../services/api';
import { Portfolio as PortfolioType, Holding } from '../types';
import './Portfolio.css';

function Portfolio() {
  const [portfolio, setPortfolio] = useState<PortfolioType | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [fundAmount, setFundAmount] = useState('');
  const [fundAction, setFundAction] = useState<'add' | 'withdraw'>('add');
  const [tradeStock, setTradeStock] = useState('');
  const [tradeQuantity, setTradeQuantity] = useState(1);
  const [tradeAction, setTradeAction] = useState<'buy' | 'sell'>('buy');

  useEffect(() => {
    loadPortfolio();
  }, []);

  const loadPortfolio = async () => {
    try {
      const data = await portfolioAPI.getPortfolio();
      setPortfolio(data);
    } catch (err: any) {
      setError('Failed to load portfolio');
    }
  };

  const handleManageFunds = async () => {
    const amount = parseFloat(fundAmount);
    if (isNaN(amount) || amount <= 0) {
      setError('Please enter a valid amount greater than 0');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      await portfolioAPI.manageFunds(amount, fundAction);
      setSuccess(`Funds ${fundAction === 'add' ? 'added' : 'withdrawn'} successfully!`);
      setFundAmount('');
      await loadPortfolio();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to manage funds');
    } finally {
      setLoading(false);
    }
  };

  const handleExecuteTrade = async () => {
    if (!tradeStock.trim()) {
      setError('Please enter a stock ticker symbol');
      return;
    }

    if (tradeQuantity < 1) {
      setError('Quantity must be at least 1');
      return;
    }

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
      await portfolioAPI.executeTrade(tradeStock.toUpperCase(), tradeQuantity, tradeAction);
      setSuccess(`Trade executed successfully!`);
      setTradeStock('');
      setTradeQuantity(1);
      await loadPortfolio();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to execute trade');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    if (!confirm('Are you sure you want to reset your portfolio? This cannot be undone.')) {
      return;
    }

    setLoading(true);
    try {
      await portfolioAPI.resetPortfolio();
      setSuccess('Portfolio reset successfully!');
      await loadPortfolio();
    } catch (err: any) {
      setError('Failed to reset portfolio');
    } finally {
      setLoading(false);
    }
  };

  if (!portfolio && !error) {
    return <div className="loading">Loading portfolio...</div>;
  }

  if (!portfolio && error) {
    return <div className="loading">{error}</div>;
  }

  return (
    <div className="portfolio">
      <motion.div
        className="portfolio-header"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="header-content">
          <h1 className="portfolio-title">Portfolio Management</h1>
          <div className="balance-display">
            <div className="balance-item">
              <span className="balance-label">Current Balance</span>
              <span className="balance-value">${portfolio.balance.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
            </div>
            <div className="balance-item">
              <span className="balance-label">Stock Balance</span>
              <span className="balance-value">${portfolio.stock_balance.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
            </div>
          </div>
          <button onClick={handleReset} className="reset-button" disabled={loading}>
            Reset
          </button>
        </div>
      </motion.div>

      {error && (
        <motion.div
          className="message error"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          ⚠️ {error}
        </motion.div>
      )}

      {success && (
        <motion.div
          className="message success"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          ✓ {success}
        </motion.div>
      )}

      <div className="portfolio-sections">
        <motion.section
          className="funds-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <h2 className="section-title">Manage Funds</h2>
          <div className="funds-controls">
            <select
              value={fundAction}
              onChange={(e) => setFundAction(e.target.value as 'add' | 'withdraw')}
              className="control-select"
            >
              <option value="add">Add Funds</option>
              <option value="withdraw">Withdraw Funds</option>
            </select>
            <input
              type="number"
              value={fundAmount}
              onChange={(e) => setFundAmount(e.target.value)}
              placeholder="Amount"
              className="control-input"
              min="0"
              step="0.01"
            />
            <button
              onClick={handleManageFunds}
              disabled={loading}
              className="action-button"
            >
              Submit
            </button>
          </div>
        </motion.section>

        <motion.section
          className="trading-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <h2 className="section-title">Buy/Sell Stocks</h2>
          <div className="trading-controls">
            <input
              type="text"
              value={tradeStock}
              onChange={(e) => setTradeStock(e.target.value.toUpperCase())}
              placeholder="Stock Ticker Symbol"
              className="control-input"
            />
            <input
              type="number"
              value={tradeQuantity}
              onChange={(e) => setTradeQuantity(parseInt(e.target.value) || 1)}
              placeholder="Shares"
              className="control-input"
              min="1"
            />
            <select
              value={tradeAction}
              onChange={(e) => setTradeAction(e.target.value as 'buy' | 'sell')}
              className="control-select"
            >
              <option value="buy">Buy</option>
              <option value="sell">Sell</option>
            </select>
            <button
              onClick={handleExecuteTrade}
              disabled={loading}
              className={`action-button ${tradeAction === 'buy' ? 'buy-button' : 'sell-button'}`}
            >
              Execute Trade
            </button>
          </div>
        </motion.section>

        {portfolio.holdings.length > 0 && (
          <motion.section
            className="holdings-section"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <h2 className="section-title">Current Holdings</h2>
            <div className="holdings-table-wrapper">
              <table className="holdings-table">
                <thead>
                  <tr>
                    <th>Stock</th>
                    <th>Shares</th>
                    <th>Total Cost</th>
                    <th>Avg Price</th>
                  </tr>
                </thead>
                <tbody>
                  {portfolio.holdings.map((holding: Holding, index: number) => (
                    <tr key={index}>
                      <td className="stock-symbol">{holding.stock}</td>
                      <td>{holding.shares}</td>
                      <td>${holding.total_cost.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                      <td>${(holding.total_cost / holding.shares).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </motion.section>
        )}
      </div>
    </div>
  );
}

export default Portfolio;
