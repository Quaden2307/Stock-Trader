import { useState } from 'react';
import { motion } from 'framer-motion';
import StockScreener from './components/StockScreener';
import Portfolio from './components/Portfolio';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState<'stock' | 'portfolio'>('stock');

  return (
    <div className="app">
      <motion.header 
        className="app-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="header-content">
          <h1 className="app-title">
            <span className="title-icon">📈</span>
            Stock Trader
          </h1>
          <div className="tab-switcher">
            <button
              className={`tab-button ${activeTab === 'stock' ? 'active' : ''}`}
              onClick={() => setActiveTab('stock')}
            >
              Stock Screener
            </button>
            <button
              className={`tab-button ${activeTab === 'portfolio' ? 'active' : ''}`}
              onClick={() => setActiveTab('portfolio')}
            >
              Portfolio
            </button>
          </div>
        </div>
      </motion.header>

      <main className="app-main">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.3 }}
        >
          {activeTab === 'stock' ? <StockScreener /> : <Portfolio />}
        </motion.div>
      </main>
    </div>
  );
}

export default App;
