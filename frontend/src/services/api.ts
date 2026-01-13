import axios from 'axios';
import { StockData, Portfolio, OptionChain } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api` 
  : '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const stockAPI = {
  getStockData: async (
    ticker: string,
    period: string,
    interval: string,
    viewType: string
  ): Promise<StockData> => {
    const response = await api.post('/stock/data', {
      ticker,
      period,
      interval,
      view_type: viewType,
    });
    return response.data;
  },

  getOptionsDates: async (ticker: string): Promise<string[]> => {
    const response = await api.get(`/stock/options/${ticker}`);
    return response.data.options_dates || [];
  },

  getOptionChain: async (ticker: string, date: string): Promise<OptionChain> => {
    const response = await api.get(`/stock/options/${ticker}/${date}`);
    return response.data;
  },
};

export const portfolioAPI = {
  getPortfolio: async (): Promise<Portfolio> => {
    const response = await api.get('/portfolio');
    return response.data;
  },

  manageFunds: async (amount: number, action: 'add' | 'withdraw'): Promise<Portfolio | null> => {
    const response = await api.post('/portfolio/funds', { amount, action });
    return response.data.portfolio || null;
  },

  executeTrade: async (
    stockSymbol: string,
    quantity: number,
    action: 'buy' | 'sell'
  ): Promise<Portfolio> => {
    const response = await api.post('/portfolio/trade', {
      stock_symbol: stockSymbol,
      quantity,
      action,
    });
    return response.data.portfolio;
  },

  resetPortfolio: async (): Promise<Portfolio> => {
    const response = await api.post('/portfolio/reset');
    return response.data.portfolio;
  },
};
