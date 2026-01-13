"""
Stock Price Prediction Backend with PyTorch Neural Networks
Uses tensors and deep learning for advanced prediction
Integrates with yfinance for real-time data
"""

import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import warnings
warnings.filterwarnings('ignore')


class StockDataset(Dataset):
    """
    PyTorch Dataset for stock data
    """
    def __init__(self, features, targets):
        self.features = torch.FloatTensor(features)
        self.targets = torch.FloatTensor(targets)
    
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        return self.features[idx], self.targets[idx]


class LSTMModel(nn.Module):
    """
    LSTM Neural Network for sequential stock data
    """
    def __init__(self, input_size, hidden_size=64, num_layers=2, dropout=0.2):
        super(LSTMModel, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
            batch_first=True
        )
        
        self.fc1 = nn.Linear(hidden_size, 32)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)
        self.fc2 = nn.Linear(32, 1)
    
    def forward(self, x):
        # LSTM layer
        lstm_out, _ = self.lstm(x)
        
        # Take the last output
        out = lstm_out[:, -1, :]
        
        # Fully connected layers
        out = self.fc1(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)
        
        return out


class FeedForwardNN(nn.Module):
    """
    Deep Feedforward Neural Network
    """
    def __init__(self, input_size, hidden_sizes=[128, 64, 32], dropout=0.3):
        super(FeedForwardNN, self).__init__()
        
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.BatchNorm1d(hidden_size))
            layers.append(nn.Dropout(dropout))
            prev_size = hidden_size
        
        layers.append(nn.Linear(prev_size, 1))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x)


class StockPredictor:
    """
    PyTorch-based stock price predictor
    """
    
    def __init__(self, ticker: str, device=None):
        self.ticker = ticker.upper()
        self.data = None
        self.device = device if device else torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.models = {}
        self.feature_columns = []
        self.scaler_mean = None
        self.scaler_std = None
        
        print(f"Using device: {self.device}")
    
    def fetch_data(self, period: str = "2y", interval: str = "1d") -> pd.DataFrame:
        """
        Fetch stock data using yfinance
        """
        try:
            stock = yf.Ticker(self.ticker)
            df = yf.download(self.ticker, period=period, interval=interval, progress=False)
            
            if df.empty:
                raise ValueError(f"No data found for {self.ticker}")
            
            # Handle MultiIndex if present
            if isinstance(df.index, pd.MultiIndex):
                df.index = df.index.droplevel(0)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.droplevel(1)
            
            self.data = df
            return df
            
        except Exception as e:
            raise Exception(f"Error fetching data for {self.ticker}: {str(e)}")
    
    def calculate_technical_indicators(self) -> pd.DataFrame:
        """
        Calculate technical indicators
        """
        df = self.data.copy()
        
        # Moving Averages
        df['SMA_5'] = df['Close'].rolling(window=5).mean()
        df['SMA_10'] = df['Close'].rolling(window=10).mean()
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        
        # Exponential Moving Averages
        df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        df['BB_Width'] = df['BB_Upper'] - df['BB_Lower']
        
        # Momentum
        df['Momentum'] = df['Close'] - df['Close'].shift(10)
        
        # Rate of Change
        df['ROC'] = ((df['Close'] - df['Close'].shift(10)) / df['Close'].shift(10)) * 100
        
        # Volume indicators
        df['Volume_SMA'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_SMA']
        
        # Price change percentage
        df['Price_Change'] = df['Close'].pct_change()
        
        # Volatility
        df['Volatility'] = df['Price_Change'].rolling(window=20).std()
        
        # Support/Resistance levels
        df['High_20'] = df['High'].rolling(window=20).max()
        df['Low_20'] = df['Low'].rolling(window=20).min()
        
        # Distance from highs/lows
        df['Distance_from_High'] = (df['High_20'] - df['Close']) / df['Close']
        df['Distance_from_Low'] = (df['Close'] - df['Low_20']) / df['Close']
        
        return df
    
    def prepare_features(self, forecast_days: int = 1) -> tuple:
        """
        Prepare feature tensors for PyTorch models
        """
        df = self.calculate_technical_indicators()
        df = df.dropna()
        
        # Create target variable
        df['Target'] = df['Close'].shift(-forecast_days)
        df = df.dropna()
        
        # Select features
        self.feature_columns = [
            'Open', 'High', 'Low', 'Volume',
            'SMA_5', 'SMA_10', 'SMA_20', 'SMA_50',
            'EMA_12', 'EMA_26', 'MACD', 'MACD_Signal',
            'RSI', 'BB_Width', 'Momentum', 'ROC',
            'Volume_Ratio', 'Volatility',
            'Distance_from_High', 'Distance_from_Low'
        ]
        
        X = df[self.feature_columns].values
        y = df['Target'].values
        
        return X, y, df
    
    def normalize_data(self, X_train, X_test):
        """
        Normalize features using PyTorch tensors
        """
        X_train_tensor = torch.FloatTensor(X_train)
        X_test_tensor = torch.FloatTensor(X_test)
        
        # Calculate mean and std from training data
        self.scaler_mean = X_train_tensor.mean(dim=0)
        self.scaler_std = X_train_tensor.std(dim=0) + 1e-7  # Avoid division by zero
        
        # Normalize
        X_train_normalized = (X_train_tensor - self.scaler_mean) / self.scaler_std
        X_test_normalized = (X_test_tensor - self.scaler_mean) / self.scaler_std
        
        return X_train_normalized.numpy(), X_test_normalized.numpy()
    
    def create_sequences(self, X, y, seq_length=10):
        """
        Create sequences for LSTM (time series windows)
        """
        X_seq, y_seq = [], []
        
        for i in range(len(X) - seq_length):
            X_seq.append(X[i:i+seq_length])
            y_seq.append(y[i+seq_length])
        
        return np.array(X_seq), np.array(y_seq)
    
    def train_feedforward_model(self, X_train, y_train, X_test, y_test, epochs=100, batch_size=32):
        """
        Train feedforward neural network
        """
        print("\nTraining Feedforward Neural Network...")
        
        # Create datasets
        train_dataset = StockDataset(X_train, y_train)
        test_dataset = StockDataset(X_test, y_test)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
        
        # Initialize model
        model = FeedForwardNN(input_size=X_train.shape[1]).to(self.device)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-5)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=10, factor=0.5)
        
        best_loss = float('inf')
        patience_counter = 0
        
        # Training loop
        for epoch in range(epochs):
            model.train()
            train_loss = 0.0
            
            for features, targets in train_loader:
                features, targets = features.to(self.device), targets.to(self.device)
                
                optimizer.zero_grad()
                outputs = model(features)
                loss = criterion(outputs.squeeze(), targets)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            # Validation
            model.eval()
            test_loss = 0.0
            with torch.no_grad():
                for features, targets in test_loader:
                    features, targets = features.to(self.device), targets.to(self.device)
                    outputs = model(features)
                    loss = criterion(outputs.squeeze(), targets)
                    test_loss += loss.item()
            
            avg_train_loss = train_loss / len(train_loader)
            avg_test_loss = test_loss / len(test_loader)
            
            scheduler.step(avg_test_loss)
            
            if (epoch + 1) % 20 == 0:
                print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {avg_train_loss:.4f}, Test Loss: {avg_test_loss:.4f}")
            
            # Early stopping
            if avg_test_loss < best_loss:
                best_loss = avg_test_loss
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= 20:
                    print(f"Early stopping at epoch {epoch+1}")
                    break
        
        self.models['feedforward'] = model
        return model
    
    def train_lstm_model(self, X_train, y_train, X_test, y_test, seq_length=10, epochs=100, batch_size=32):
        """
        Train LSTM neural network
        """
        print("\nTraining LSTM Neural Network...")
        
        # Create sequences
        X_train_seq, y_train_seq = self.create_sequences(X_train, y_train, seq_length)
        X_test_seq, y_test_seq = self.create_sequences(X_test, y_test, seq_length)
        
        # Create datasets
        train_dataset = StockDataset(X_train_seq, y_train_seq)
        test_dataset = StockDataset(X_test_seq, y_test_seq)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
        
        # Initialize model
        model = LSTMModel(input_size=X_train.shape[1]).to(self.device)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=10, factor=0.5)
        
        best_loss = float('inf')
        patience_counter = 0
        
        # Training loop
        for epoch in range(epochs):
            model.train()
            train_loss = 0.0
            
            for features, targets in train_loader:
                features, targets = features.to(self.device), targets.to(self.device)
                
                optimizer.zero_grad()
                outputs = model(features)
                loss = criterion(outputs.squeeze(), targets)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
            
            # Validation
            model.eval()
            test_loss = 0.0
            with torch.no_grad():
                for features, targets in test_loader:
                    features, targets = features.to(self.device), targets.to(self.device)
                    outputs = model(features)
                    loss = criterion(outputs.squeeze(), targets)
                    test_loss += loss.item()
            
            avg_train_loss = train_loss / len(train_loader)
            avg_test_loss = test_loss / len(test_loader)
            
            scheduler.step(avg_test_loss)
            
            if (epoch + 1) % 20 == 0:
                print(f"Epoch [{epoch+1}/{epochs}], Train Loss: {avg_train_loss:.4f}, Test Loss: {avg_test_loss:.4f}")
            
            # Early stopping
            if avg_test_loss < best_loss:
                best_loss = avg_test_loss
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= 20:
                    print(f"Early stopping at epoch {epoch+1}")
                    break
        
        self.models['lstm'] = model
        return model
    
    def train_models(self, test_size=0.2, epochs=100):
        """
        Train both neural network models
        """
        X, y, df = self.prepare_features()
        
        # Split data (time series - no shuffle)
        split_idx = int(len(X) * (1 - test_size))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        
        # Normalize
        X_train_norm, X_test_norm = self.normalize_data(X_train, X_test)
        
        # Train feedforward model
        self.train_feedforward_model(X_train_norm, y_train, X_test_norm, y_test, epochs=epochs)
        
        # Train LSTM model
        self.train_lstm_model(X_train_norm, y_train, X_test_norm, y_test, epochs=epochs)
        
        print("\n" + "="*50)
        print("All models trained successfully!")
    
    def predict_next_price(self, method='ensemble') -> dict:
        """
        Predict next day's price using trained models
        """
        if not self.models:
            raise ValueError("Models not trained. Call train_models() first.")
        
        # Get latest features
        df = self.calculate_technical_indicators()
        df = df.dropna()
        latest_features = df[self.feature_columns].iloc[-1:].values
        
        # Normalize
        latest_tensor = torch.FloatTensor(latest_features)
        latest_normalized = ((latest_tensor - self.scaler_mean) / self.scaler_std).to(self.device)
        
        current_price = df['Close'].iloc[-1]
        predictions = {}
        
        # Feedforward prediction
        if 'feedforward' in self.models:
            self.models['feedforward'].eval()
            with torch.no_grad():
                pred = self.models['feedforward'](latest_normalized)
                predictions['feedforward'] = pred.cpu().item()
        
        # LSTM prediction (needs sequence)
        if 'lstm' in self.models:
            seq_length = 10
            recent_features = df[self.feature_columns].iloc[-seq_length:].values
            recent_tensor = torch.FloatTensor(recent_features)
            recent_normalized = ((recent_tensor - self.scaler_mean) / self.scaler_std)
            recent_seq = recent_normalized.unsqueeze(0).to(self.device)
            
            self.models['lstm'].eval()
            with torch.no_grad():
                pred = self.models['lstm'](recent_seq)
                predictions['lstm'] = pred.cpu().item()
        
        # Ensemble prediction
        if method == 'ensemble' and len(predictions) > 1:
            predicted_price = np.mean(list(predictions.values()))
        else:
            predicted_price = predictions.get(method, list(predictions.values())[0])
        
        # Calculate change
        price_change = predicted_price - current_price
        percent_change = (price_change / current_price) * 100
        
        return {
            'ticker': self.ticker,
            'current_price': round(current_price, 2),
            'predicted_price': round(predicted_price, 2),
            'price_change': round(price_change, 2),
            'percent_change': round(percent_change, 2),
            'direction': 'UP' if price_change > 0 else 'DOWN',
            'all_predictions': {k: round(v, 2) for k, v in predictions.items()},
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def save_models(self, path='models/'):
        """
        Save trained models
        """
        import os
        os.makedirs(path, exist_ok=True)
        
        for name, model in self.models.items():
            torch.save(model.state_dict(), f'{path}{self.ticker}_{name}.pth')
        
        # Save scaler parameters
        torch.save({
            'mean': self.scaler_mean,
            'std': self.scaler_std,
            'features': self.feature_columns
        }, f'{path}{self.ticker}_scaler.pth')
        
        print(f"Models saved to {path}")


def main():
    """
    Example usage
    """
    # Initialize predictor
    ticker = "AAPL"
    predictor = StockPredictor(ticker)
    
    # Fetch data
    print(f"Fetching data for {ticker}...")
    predictor.fetch_data(period="2y", interval="1d")
    
    # Train models
    predictor.train_models(epochs=100)
    
    # Make prediction
    print("\n" + "="*50)
    prediction = predictor.predict_next_price(method='ensemble')
    print(f"\nPrediction for {prediction['ticker']}:")
    print(f"Current Price: ${prediction['current_price']}")
    print(f"Predicted Price: ${prediction['predicted_price']}")
    print(f"Expected Change: ${prediction['price_change']} ({prediction['percent_change']}%)")
    print(f"Direction: {prediction['direction']}")
    
    print("\nIndividual Model Predictions:")
    for model, price in prediction['all_predictions'].items():
        print(f"  {model.upper()}: ${price}")
    
    # Save models
    predictor.save_models()


if __name__ == "__main__":
    main()