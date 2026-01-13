import { useState } from 'react';
import { motion } from 'framer-motion';
import { stockAPI } from '../services/api';
import { StockData, OptionChain } from '../types';
import StockChart from './StockChart';
import StockTable from './StockTable';
import OptionsPanel from './OptionsPanel';
import './StockScreener.css';

const PERIOD_OPTIONS = {
  '1d': { period: '1d', interval: '1h' },
  '5d': { period: '5d', interval: '4h' },
  '1mo': { period: '1mo', interval: '1d' },
  '6mo': { period: '6mo', interval: '1wk' },
  'YTD': { period: 'ytd', interval: '1wk' },
  '1y': { period: '1y', interval: '1mo' },
  '5y': { period: '5y', interval: '3mo' },
  'Max': { period: 'max', interval: '3mo' },
};

const VIEW_TYPES = {
  'Price': 'price',
  'Volume': 'volume',
  'Both': 'both',
};

function StockScreener() {
  const [ticker, setTicker] = useState('');
  const [selectedPeriod, setSelectedPeriod] = useState<keyof typeof PERIOD_OPTIONS>('1mo');
  const [selectedView, setSelectedView] = useState<keyof typeof VIEW_TYPES>('Price');
  const [stockData, setStockData] = useState<StockData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [optionsDates, setOptionsDates] = useState<string[]>([]);
  const [selectedOptionDate, setSelectedOptionDate] = useState<string>('');
  const [optionChain, setOptionChain] = useState<OptionChain | null>(null);

  const handleGetData = async () => {
    if (!ticker.trim()) {
      setError('Please enter a stock ticker symbol.');
      return;
    }

    setLoading(true);
    setError(null);
    setStockData(null);
    setOptionsDates([]);
    setOptionChain(null);
    setSelectedOptionDate('');

    try {
      const periodConfig = PERIOD_OPTIONS[selectedPeriod];
      const data = await stockAPI.getStockData(
        ticker.toUpperCase(),
        periodConfig.period,
        periodConfig.interval,
        VIEW_TYPES[selectedView]
      );
      setStockData(data);

      // Fetch options dates
      try {
        const dates = await stockAPI.getOptionsDates(ticker.toUpperCase());
        setOptionsDates(dates);
      } catch (err) {
        // Options not available for all stocks
        console.log('Options not available');
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error retrieving stock data. Please check the ticker symbol.');
    } finally {
      setLoading(false);
    }
  };

  const handleOptionDateChange = async (date: string) => {
    setSelectedOptionDate(date);
    setLoading(true);
    try {
      const chain = await stockAPI.getOptionChain(ticker.toUpperCase(), date);
      setOptionChain(chain);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error retrieving options data.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="stock-screener">
      <motion.div
        className="screener-controls"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="controls-grid">
          <div className="control-group">
            <label>Price/Volume</label>
            <select
              value={selectedView}
              onChange={(e) => setSelectedView(e.target.value as keyof typeof VIEW_TYPES)}
              className="control-select"
            >
              {Object.keys(VIEW_TYPES).map((key) => (
                <option key={key} value={key}>
                  {key}
                </option>
              ))}
            </select>
          </div>

          <div className="control-group">
            <label>Period</label>
            <select
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(e.target.value as keyof typeof PERIOD_OPTIONS)}
              className="control-select"
            >
              {Object.keys(PERIOD_OPTIONS).map((key) => (
                <option key={key} value={key}>
                  {key}
                </option>
              ))}
            </select>
          </div>

          <div className="control-group ticker-input-group">
            <label>Stock Ticker</label>
            <input
              type="text"
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              placeholder="e.g., AAPL, TSLA"
              className="control-input"
              onKeyPress={(e) => e.key === 'Enter' && handleGetData()}
            />
          </div>

          <button
            onClick={handleGetData}
            disabled={loading}
            className="get-data-button"
          >
            {loading ? 'Loading...' : 'Get Stock Data'}
          </button>
        </div>
      </motion.div>

      {error && (
        <motion.div
          className="error-message"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
        >
          ⚠️ {error}
        </motion.div>
      )}

      {stockData && (
        <motion.div
          className="stock-results"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="price-display">
            <h2>
              {stockData.ticker}: ${stockData.current_price.toFixed(2)}
            </h2>
            <span
              className={`price-change ${
                stockData.price_change >= 0 ? 'positive' : 'negative'
              }`}
            >
              {stockData.price_change >= 0 ? '↑' : '↓'}
              {Math.abs(stockData.percent_change).toFixed(2)}%
            </span>
          </div>

          <div className="results-grid">
            <div className="chart-container">
              <StockChart data={stockData} />
            </div>
            <div className="table-container">
              <StockTable data={stockData} />
            </div>
          </div>
        </motion.div>
      )}

      {stockData && (
        <motion.div
          className="options-section"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
        >
          <h2 className="section-title">Stock Options</h2>
          {optionsDates.length > 0 ? (
            <div className="options-controls">
              <select
                value={selectedOptionDate}
                onChange={(e) => handleOptionDateChange(e.target.value)}
                className="control-select"
              >
                <option value="">Select expiration date</option>
                {optionsDates.map((date) => (
                  <option key={date} value={date}>
                    {date}
                  </option>
                ))}
              </select>
            </div>
          ) : (
            <p className="info-message">No options data available for {stockData.ticker}.</p>
          )}

          {optionChain && <OptionsPanel optionChain={optionChain} />}
        </motion.div>
      )}
    </div>
  );
}

export default StockScreener;
