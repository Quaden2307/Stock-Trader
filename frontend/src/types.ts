export interface StockData {
  ticker: string;
  current_price: number;
  price_change: number;
  percent_change: number;
  dates: string[];
  close_prices: number[];
  volume_data: number[];
  volume_label: string;
  table_data: any[];
  table_dates: string[];
  view_type: string;
}

export interface Portfolio {
  balance: number;
  stock_balance: number;
  holdings: Holding[];
}

export interface Holding {
  stock: string;
  shares: number;
  total_cost: number;
}

export interface OptionChain {
  ticker: string;
  expiration_date: string;
  calls: any[];
  puts: any[];
}
