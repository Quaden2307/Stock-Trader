import { useMemo } from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ComposedChart,
} from 'recharts';
import { StockData } from '../types';
import './StockChart.css';

interface StockChartProps {
  data: StockData;
}

function StockChart({ data }: StockChartProps) {
  const chartData = useMemo(() => {
    return data.dates.map((date, index) => ({
      date,
      price: data.close_prices[index],
      volume: data.volume_data[index],
    }));
  }, [data]);

  if (data.view_type === 'both') {
    return (
      <div className="stock-chart">
        <h3 className="chart-title">{data.ticker} Price + Volume</h3>
        <ResponsiveContainer width="100%" height={500}>
          <ComposedChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 212, 255, 0.1)" />
            <XAxis
              dataKey="date"
              angle={-45}
              textAnchor="end"
              height={80}
              stroke="#a0aec0"
              style={{ fontSize: '12px' }}
            />
            <YAxis
              yAxisId="price"
              orientation="left"
              stroke="#00d4ff"
              style={{ fontSize: '12px' }}
            />
            <YAxis
              yAxisId="volume"
              orientation="right"
              stroke="#ec4899"
              style={{ fontSize: '12px' }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#141b2d',
                border: '1px solid rgba(0, 212, 255, 0.3)',
                borderRadius: '8px',
                color: '#ffffff',
              }}
            />
            <Legend />
            <Line
              yAxisId="price"
              type="monotone"
              dataKey="price"
              stroke="#00d4ff"
              strokeWidth={2}
              dot={false}
              name="Price ($)"
            />
            <Bar
              yAxisId="volume"
              dataKey="volume"
              fill="#ec4899"
              name={data.volume_label}
              opacity={0.7}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>
    );
  }

  if (data.view_type === 'price') {
    return (
      <div className="stock-chart">
        <h3 className="chart-title">{data.ticker} Stock Price</h3>
        <ResponsiveContainer width="100%" height={500}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 212, 255, 0.1)" />
            <XAxis
              dataKey="date"
              angle={-45}
              textAnchor="end"
              height={80}
              stroke="#a0aec0"
              style={{ fontSize: '12px' }}
            />
            <YAxis stroke="#00d4ff" style={{ fontSize: '12px' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#141b2d',
                border: '1px solid rgba(0, 212, 255, 0.3)',
                borderRadius: '8px',
                color: '#ffffff',
              }}
            />
            <Line
              type="monotone"
              dataKey="price"
              stroke="#00d4ff"
              strokeWidth={3}
              dot={false}
              name="Price ($)"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  }

  return (
    <div className="stock-chart">
      <h3 className="chart-title">{data.ticker} Trading Volume</h3>
      <ResponsiveContainer width="100%" height={500}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(0, 212, 255, 0.1)" />
          <XAxis
            dataKey="date"
            angle={-45}
            textAnchor="end"
            height={80}
            stroke="#a0aec0"
            style={{ fontSize: '12px' }}
          />
          <YAxis stroke="#ec4899" style={{ fontSize: '12px' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#141b2d',
              border: '1px solid rgba(236, 72, 153, 0.3)',
              borderRadius: '8px',
              color: '#ffffff',
            }}
          />
          <Bar dataKey="volume" fill="#ec4899" name={data.volume_label} opacity={0.7} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export default StockChart;
