import { OptionChain } from '../types';
import './OptionsPanel.css';

interface OptionsPanelProps {
  optionChain: OptionChain;
}

function OptionsPanel({ optionChain }: OptionsPanelProps) {
  const formatNumber = (num: number) => {
    if (typeof num !== 'number' || isNaN(num)) return 'N/A';
    return num.toFixed(2);
  };

  return (
    <div className="options-panel">
      <div className="options-grid">
        <div className="options-section">
          <h3 className="options-title">
            Call Options for {optionChain.ticker} expiring on {optionChain.expiration_date}
          </h3>
          <div className="options-table-wrapper">
            <table className="options-table">
              <thead>
                <tr>
                  <th>Strike</th>
                  <th>Last Price</th>
                  <th>Bid</th>
                  <th>Ask</th>
                  <th>Volume</th>
                  <th>Open Interest</th>
                </tr>
              </thead>
              <tbody>
                {optionChain.calls.slice(0, 20).map((call, index) => (
                  <tr key={index}>
                    <td>${formatNumber(call.strike)}</td>
                    <td>${formatNumber(call.lastPrice)}</td>
                    <td>${formatNumber(call.bid)}</td>
                    <td>${formatNumber(call.ask)}</td>
                    <td>{call.volume?.toLocaleString() || 'N/A'}</td>
                    <td>{call.openInterest?.toLocaleString() || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="options-section">
          <h3 className="options-title">
            Put Options for {optionChain.ticker} expiring on {optionChain.expiration_date}
          </h3>
          <div className="options-table-wrapper">
            <table className="options-table">
              <thead>
                <tr>
                  <th>Strike</th>
                  <th>Last Price</th>
                  <th>Bid</th>
                  <th>Ask</th>
                  <th>Volume</th>
                  <th>Open Interest</th>
                </tr>
              </thead>
              <tbody>
                {optionChain.puts.slice(0, 20).map((put, index) => (
                  <tr key={index}>
                    <td>${formatNumber(put.strike)}</td>
                    <td>${formatNumber(put.lastPrice)}</td>
                    <td>${formatNumber(put.bid)}</td>
                    <td>${formatNumber(put.ask)}</td>
                    <td>{put.volume?.toLocaleString() || 'N/A'}</td>
                    <td>{put.openInterest?.toLocaleString() || 'N/A'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default OptionsPanel;
