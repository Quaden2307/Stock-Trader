# 📈 Stock Trader - Futuristic Stock Screener

A modern, futuristic stock screener and portfolio management application built with React, TypeScript, and FastAPI. Features real-time stock data visualization, interactive charts, and portfolio management capabilities.

![Stock Trader](https://img.shields.io/badge/React-18.2.0-blue) ![TypeScript](https://img.shields.io/badge/TypeScript-5.3.3-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.120.3-green) ![Python](https://img.shields.io/badge/Python-3.8+-green)

## 🌐 Live Demo

🔗 **[View Live Application](https://stock-trader-deploy.onrender.com/)** *(Update this with your deployed URL)*

**No installation required!** Just click the link above to try it out. Perfect for employers and recruiters to see your work instantly.

> 💡 **For Employers**: This application is fully deployed and ready to use. No setup needed - just click the link above!

## ✨ Features

- **📊 Stock Screener**: Real-time stock data visualization with interactive charts
- **💼 Portfolio Management**: Buy/sell stocks and manage your portfolio
- **📈 Options Data**: View call and put options for stocks
- **🎨 Modern UI**: Futuristic design with smooth animations and gradients
- **📱 Responsive**: Works seamlessly on desktop and mobile devices
- **⚡ Fast**: Built with Vite for lightning-fast development and production builds

## 🛠 Tech Stack

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Recharts** - Data visualization
- **Framer Motion** - Animations
- **Axios** - HTTP client

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.8+** - Programming language
- **yfinance** - Stock data API
- **pandas & numpy** - Data processing

## 🚀 Quick Start

### 🌐 Try It Online (No Installation)

**For employers and quick demos**: The application is deployed and ready to use!

- **Live Demo**: [View Live Application](https://your-app.vercel.app) *(Update with your URL)*
- **No setup required** - just click and use!

### 💻 Local Development Setup

### Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18+ and npm ([Download](https://nodejs.org/))
- **Python** 3.8+ and pip ([Download](https://www.python.org/downloads/))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stock-trader.git
   cd stock-trader
   ```

2. **Install Backend Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running the Application

You need to run both the backend and frontend servers. Open **two separate terminal windows/tabs**.

#### Option 1: Manual Start (Recommended for Development)

**Terminal 1 - Backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

#### Option 2: Using the Startup Script (macOS/Linux)

```bash
chmod +x start.sh
./start.sh
```

This will start both servers automatically.

### Access the Application

Once both servers are running:

- **Frontend**: Open [http://localhost:5173](http://localhost:5173) in your browser
- **Backend API**: Available at [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)

## 📖 Usage Guide

### Stock Screener Tab

1. Enter a stock ticker symbol (e.g., `AAPL`, `TSLA`, `MSFT`)
2. Select a time period (1d, 5d, 1mo, 6mo, YTD, 1y, 5y, Max)
3. Choose view type (Price, Volume, or Both)
4. Click "Get Stock Data"
5. View interactive charts and detailed price data
6. Scroll down to view stock options (if available)

### Portfolio Tab

1. **Manage Funds**: Add or withdraw funds from your account
2. **Buy Stocks**: Enter ticker, quantity, and click "Execute Trade"
3. **Sell Stocks**: Select stocks you own and sell them
4. **View Holdings**: See your current portfolio holdings

## 🏗 Project Structure

```
stock-trader/
├── backend/
│   ├── main.py              # FastAPI backend server
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── StockScreener.tsx
│   │   │   ├── Portfolio.tsx
│   │   │   ├── StockChart.tsx
│   │   │   └── ...
│   │   ├── services/        # API service layer
│   │   ├── types.ts         # TypeScript types
│   │   └── App.tsx          # Main app component
│   ├── package.json
│   └── vite.config.ts
├── requirements.txt         # Python dependencies (root)
├── start.sh                 # Startup script
└── README.md
```

## 🔧 API Endpoints

The backend provides the following REST API endpoints:

### Stock Data
- `POST /api/stock/data` - Get stock price and volume data
- `GET /api/stock/options/{ticker}` - Get available options expiration dates
- `GET /api/stock/options/{ticker}/{date}` - Get option chain for a specific date

### Portfolio
- `GET /api/portfolio` - Get current portfolio state
- `POST /api/portfolio/funds` - Add or withdraw funds
- `POST /api/portfolio/trade` - Execute buy/sell trades
- `POST /api/portfolio/reset` - Reset portfolio to default state

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🎯 Example Usage

### View Stock Data
```bash
curl -X POST "http://localhost:8000/api/stock/data" \
  -H "Content-Type: application/json" \
  -d '{
    "ticker": "AAPL",
    "period": "1mo",
    "interval": "1d",
    "view_type": "both"
  }'
```

### Get Portfolio
```bash
curl http://localhost:8000/api/portfolio
```

## 🐛 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
```

**Python dependencies not installing:**
```bash
# Try using pip3 instead
pip3 install -r requirements.txt

# Or use a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Issues

**Port 5173 already in use:**
```bash
# Find and kill the process
lsof -ti:5173 | xargs kill -9
```

**Node modules issues:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Build errors:**
```bash
cd frontend
npm run build
```

### Common Errors

**"Must specify a fill 'value' or 'method'"**
- This has been fixed in the latest version. Make sure you're using the latest code.

**"Out of range float values are not JSON compliant: nan"**
- This has been fixed. NaN values are now properly handled.

**CORS errors:**
- Make sure the backend is running on port 8000
- Check that the frontend proxy is configured correctly in `vite.config.ts`

## 🚢 Production Deployment

Want to deploy this yourself? See [FREE_DEPLOYMENT.md](FREE_DEPLOYMENT.md) for **free deployment options** (no credit card required)!

**Quick Deploy Options (All Free):**
- **Render.com** - ⭐ Recommended! One-click Docker deployment, 100% free
- **Fly.io** - Always-on free tier, great for Docker
- **Railway** - Easy setup, $5/month free credit
- **Docker** - One command: `docker-compose --profile prod up`

**For detailed instructions, see [FREE_DEPLOYMENT.md](FREE_DEPLOYMENT.md)**

### Quick Deploy Steps

1. **Deploy Backend to Railway**:
   - Sign up at [railway.app](https://railway.app)
   - Connect GitHub repo
   - Railway auto-detects and deploys
   - Copy your backend URL

2. **Deploy Frontend to Vercel**:
   - Sign up at [vercel.com](https://vercel.com)
   - Import GitHub repo
   - Set root directory to `frontend`
   - Add env var: `VITE_API_URL=your-backend-url`
   - Deploy!

3. **Update README** with your live URL

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete instructions.

## 🚢 Production Deployment (Detailed)

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`. Serve these with a static file server or deploy to platforms like:
- Vercel
- Netlify
- GitHub Pages

**Backend:**
```bash
# Use a production ASGI server
pip install gunicorn uvicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

Or deploy to platforms like:
- Heroku
- Railway
- Render
- AWS/DigitalOcean

### Environment Variables

For production, consider setting:
- `CORS_ORIGINS` - Allowed frontend origins
- `API_KEY` - If you add authentication later

## 📝 Development

### Running in Development Mode

Both servers support hot-reload:
- **Backend**: Automatically reloads on Python file changes (via `--reload`)
- **Frontend**: Hot Module Replacement (HMR) for instant updates

### Code Style

- **Python**: Follow PEP 8
- **TypeScript/React**: Use ESLint and Prettier (if configured)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [yfinance](https://github.com/ranaroussi/yfinance) for stock data
- [Recharts](https://recharts.org/) for beautiful charts
- [Framer Motion](https://www.framer.com/motion/) for animations

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Made with ❤️ using React, TypeScript, and FastAPI**
