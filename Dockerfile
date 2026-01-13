# Multi-stage build for Stock Trader Application (Production Ready)

# Stage 1: Frontend Build
FROM node:18-alpine as frontend-builder

WORKDIR /app

# Copy frontend package files
COPY frontend/package*.json ./
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Build frontend for production
RUN npm run build

# Stage 2: Backend + Frontend Production
FROM python:3.11-slim

WORKDIR /app

# Install backend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from builder stage
COPY --from=frontend-builder /app/dist ./frontend/dist

# Expose port (can be overridden by environment variable)
EXPOSE 8000

# Use PORT environment variable if provided (for platforms like Render, Railway)
# Default to 8000 if PORT is not set
CMD sh -c "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"
