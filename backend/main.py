from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import os

app = FastAPI(title="Stock Trader API")

# CORS middleware
# Get allowed origins from environment or use defaults
# In production (when frontend is served from same domain), allow all origins
cors_origins_env = os.getenv("CORS_ORIGINS", "")
if cors_origins_env:
    cors_origins = cors_origins_env.split(",")
else:
    # Default to localhost for development
    cors_origins = ["http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend) in production
# Check if frontend/dist exists (Docker production build)
frontend_dist_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(frontend_dist_path):
    # Mount static assets (JS, CSS, images)
    assets_path = os.path.join(frontend_dist_path, "assets")
    if os.path.exists(assets_path):
        app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
    
    # Serve index.html for root and all non-API routes (SPA routing)
    @app.get("/")
    async def serve_index():
        index_path = os.path.join(frontend_dist_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        raise HTTPException(status_code=404, detail="Frontend not found")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        # Don't serve frontend for API routes or docs
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi.json") or full_path.startswith("assets"):
            raise HTTPException(status_code=404, detail="Not found")
        
        # Serve index.html for all other routes (SPA routing)
        index_path = os.path.join(frontend_dist_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        raise HTTPException(status_code=404, detail="Frontend not found")

# In-memory storage for portfolio (in production, use a database)
portfolio_state = {
    "balance": 100000.0,
    "stock_balance": 0.0,
    "holdings": []
}

class FundRequest(BaseModel):
    amount: float
    action: str  # "add" or "withdraw"

class TradeRequest(BaseModel):
    stock_symbol: str
    quantity: int
    action: str  # "buy" or "sell"

class StockDataRequest(BaseModel):
    ticker: str
    period: str
    interval: str
    view_type: str  # "price", "volume", or "both"

@app.get("/")
def read_root():
    return {"message": "Stock Trader API"}

@app.post("/api/stock/data")
async def get_stock_data(request: StockDataRequest):
    try:
        ticker = request.ticker.upper()
        stock = yf.Ticker(ticker)
        
        # Download price data using yf.download (original working method)
        df = yf.download(ticker, period=request.period, interval=request.interval, progress=False, auto_adjust=True)
        
        if df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for {ticker}")
        
        # Handle MultiIndex if present
        if isinstance(df.index, pd.MultiIndex):
            df.index = df.index.droplevel(0)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        
        # Validate required columns exist
        required_columns = ['Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(status_code=500, detail=f"Missing required data columns: {', '.join(missing_columns)}")
        
        # Calculate price change
        new_price = float(df['Close'].iloc[-1])
        old_price = float(df['Close'].iloc[0])
        price_change = new_price - old_price
        percent_change = ((price_change / old_price) * 100) if old_price != 0 else 0
        
        # Format dates based on period/interval
        if request.period == "1d" and request.interval == "1h":
            dates = df.index.strftime('%H:%M').tolist()
        elif request.period == "5d" and request.interval == "4h":
            dates = df.index.strftime('%d %H:%M').tolist()
        elif request.period == "1mo" and request.interval == "1d":
            dates = df.index.strftime('%d %b').tolist()
        elif request.period == "6mo" and request.interval == "1wk":
            dates = df.index.strftime('%b %d').tolist()
        elif request.period == "ytd" and request.interval == "1wk":
            dates = df.index.strftime('%b %d').tolist()
        elif request.period == "1y" and request.interval == "1mo":
            dates = df.index.strftime('%Y %b').tolist()
        elif request.period == "5y" and request.interval == "3mo":
            dates = df.index.strftime('%Y-%b').tolist()
        else:
            dates = df.index.strftime('%Y-%m-%d').tolist()
        
        # Prepare price data - round to 2 decimal places
        close_prices = [round(float(x), 2) if pd.notna(x) else 0.0 for x in df['Close'].tolist()]
        
        # Prepare volume data
        volume_data = df['Volume'].tolist()
        max_volume = np.max(volume_data) if len(volume_data) > 0 else 1
        
        if max_volume > 1e9:
            volume_data = [v / 1e9 for v in volume_data]
            volume_label = "Volume (Billions)"
        elif max_volume > 1e6:
            volume_data = [v / 1e6 for v in volume_data]
            volume_label = "Volume (Millions)"
        elif max_volume > 1e3:
            volume_data = [v / 1e3 for v in volume_data]
            volume_label = "Volume (Thousands)"
        else:
            volume_label = "Volume"
        
        # Prepare table data - replace NaN with None for JSON serialization
        table_df = df.round(2)
        # Replace NaN values with None for JSON compatibility
        table_df = table_df.where(pd.notnull(table_df), None)
        table_data = table_df.to_dict('records')
        table_dates = df.index.strftime('%Y-%m-%d %H:%M:%S').tolist()
        
        return {
            "ticker": ticker,
            "current_price": round(new_price, 2),
            "price_change": round(price_change, 2),
            "percent_change": round(percent_change, 2),
            "dates": dates,
            "close_prices": close_prices,
            "volume_data": volume_data,
            "volume_label": volume_label,
            "table_data": table_data,
            "table_dates": table_dates,
            "view_type": request.view_type
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/options/{ticker}")
async def get_stock_options(ticker: str):
    try:
        stock = yf.Ticker(ticker.upper())
        options_dates = stock.options
        
        if not options_dates:
            return {"ticker": ticker.upper(), "options_dates": [], "message": "No options data available"}
        
        return {
            "ticker": ticker.upper(),
            "options_dates": list(options_dates)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stock/options/{ticker}/{date}")
async def get_option_chain(ticker: str, date: str):
    try:
        stock = yf.Ticker(ticker.upper())
        option_chain = stock.option_chain(date)
        
        # Replace NaN values with None for JSON serialization
        # Convert to dict first, then clean NaN values
        calls_dict = option_chain.calls.to_dict('records')
        puts_dict = option_chain.puts.to_dict('records')
        
        # Clean NaN values from dictionaries
        def clean_nan(obj):
            if isinstance(obj, dict):
                return {k: clean_nan(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_nan(item) for item in obj]
            elif isinstance(obj, (float, np.floating)):
                if pd.isna(obj) or np.isnan(obj) or pd.isnull(obj):
                    return None
                return obj
            return obj
        
        calls = clean_nan(calls_dict)
        puts = clean_nan(puts_dict)
        
        return {
            "ticker": ticker.upper(),
            "expiration_date": date,
            "calls": calls,
            "puts": puts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/portfolio")
async def get_portfolio():
    return portfolio_state

@app.post("/api/portfolio/funds")
async def manage_funds(request: FundRequest):
    if request.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    
    if request.action == "add":
        portfolio_state["balance"] += request.amount
    elif request.action == "withdraw":
        if request.amount > portfolio_state["balance"]:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        portfolio_state["balance"] -= request.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'add' or 'withdraw'")
    
    return {"message": f"Funds {request.action}ed successfully", "portfolio": portfolio_state}

@app.post("/api/portfolio/trade")
async def execute_trade(request: TradeRequest):
    try:
        stock_symbol = request.stock_symbol.upper()
        stock = yf.Ticker(stock_symbol)
        
        # Get current price (original working method)
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        
        total_cost = current_price * request.quantity
        
        if request.action == "buy":
            if total_cost > portfolio_state["balance"]:
                raise HTTPException(status_code=400, detail="Insufficient balance to complete the purchase")
            
            portfolio_state["balance"] -= total_cost
            portfolio_state["stock_balance"] += total_cost
            
            # Update holdings
            holding_exists = False
            for holding in portfolio_state["holdings"]:
                if holding["stock"] == stock_symbol:
                    holding["shares"] += request.quantity
                    holding["total_cost"] += total_cost
                    holding_exists = True
                    break
            
            if not holding_exists:
                portfolio_state["holdings"].append({
                    "stock": stock_symbol,
                    "shares": request.quantity,
                    "total_cost": total_cost
                })
            
            return {
                "message": f"Bought {request.quantity} shares of {stock_symbol} at ${current_price:.2f} each",
                "portfolio": portfolio_state
            }
        
        elif request.action == "sell":
            # Find holding
            holding = None
            for h in portfolio_state["holdings"]:
                if h["stock"] == stock_symbol:
                    holding = h
                    break
            
            if not holding:
                raise HTTPException(status_code=400, detail=f"You don't own any shares of {stock_symbol}")
            
            if request.quantity > holding["shares"]:
                raise HTTPException(status_code=400, detail=f"You only own {holding['shares']} shares of {stock_symbol}")
            
            portfolio_state["balance"] += total_cost
            portfolio_state["stock_balance"] -= total_cost
            
            # Update holding
            holding["shares"] -= request.quantity
            holding["total_cost"] -= total_cost
            
            # Remove if no shares left
            if holding["shares"] == 0:
                portfolio_state["holdings"].remove(holding)
            
            return {
                "message": f"Sold {request.quantity} shares of {stock_symbol} at ${current_price:.2f} each",
                "portfolio": portfolio_state
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid action. Use 'buy' or 'sell'")
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/portfolio/reset")
async def reset_portfolio():
    portfolio_state["balance"] = 100000.0
    portfolio_state["stock_balance"] = 0.0
    portfolio_state["holdings"] = []
    return {"message": "Portfolio reset successfully", "portfolio": portfolio_state}
