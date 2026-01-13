import { useMemo } from 'react';
import { StockData } from '../types';
import './StockTable.css';

interface StockTableProps {
  data: StockData;
}

function StockTable({ data }: StockTableProps) {
  const tableRows = useMemo(() => {
    return data.table_data.map((row, index) => ({
      date: data.table_dates[index],
      ...row,
    }));
  }, [data]);

  const formatNumber = (num: number) => {
    return typeof num === 'number' ? num.toFixed(2) : num;
  };

  return (
    <div className="stock-table-container">
      <h3 className="table-title">Price Data for {data.ticker}</h3>
      <div className="table-wrapper">
        <table className="stock-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Open</th>
              <th>High</th>
              <th>Low</th>
              <th>Close</th>
              <th>Volume</th>
            </tr>
          </thead>
          <tbody>
            {tableRows.map((row, index) => (
              <tr key={index}>
                <td>{new Date(row.date).toLocaleDateString()}</td>
                <td>${formatNumber(row.Open)}</td>
                <td>${formatNumber(row.High)}</td>
                <td>${formatNumber(row.Low)}</td>
                <td className="close-price">${formatNumber(row.Close)}</td>
                <td>{row.Volume?.toLocaleString() || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default StockTable;
