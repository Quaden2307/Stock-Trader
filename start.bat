@echo off
REM Start script for Stock Trader application (Windows)

echo 🚀 Starting Stock Trader Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is not installed. Please install Python 3.8+ to continue.
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ to continue.
    exit /b 1
)

REM Check if dependencies are installed
if not exist "frontend\node_modules" (
    echo 📦 Installing frontend dependencies...
    cd frontend
    call npm install
    cd ..
)

echo ✅ Dependencies checked
echo.
echo Starting servers...
echo Backend will run on http://localhost:8000
echo Frontend will run on http://localhost:5173
echo.
echo Press Ctrl+C to stop both servers
echo.

REM Start backend in background
echo 🔧 Starting backend server...
start "Stock Trader Backend" cmd /k "uvicorn backend.main:app --reload --port 8000"

REM Wait a moment for backend to start
timeout /t 2 /nobreak >nul

REM Start frontend
echo ⚛️  Starting frontend server...
cd frontend
start "Stock Trader Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ✅ Both servers are starting!
echo Open http://localhost:5173 in your browser
echo.
pause
