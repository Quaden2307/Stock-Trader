# 🚀 Deployment Guide

This guide will help you deploy the Stock Trader application so employers can access it without installing anything.

## Quick Deploy Options

### Option 1: Deploy to Railway (Recommended - Easiest)

Railway is a great option that can host both frontend and backend, or just the backend.

#### Deploy Backend to Railway:

1. **Sign up** at [railway.app](https://railway.app) (free tier available)
2. **Create a new project**
3. **Deploy from GitHub**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will auto-detect Python and deploy
4. **Set environment variables** (if needed):
   - Go to Variables tab
   - Add any required env vars
5. **Get your backend URL**: Railway will provide a URL like `https://your-app.railway.app`

#### Deploy Frontend to Vercel/Netlify:

1. **Vercel** (Recommended):
   - Sign up at [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Set root directory to `frontend`
   - Build command: `npm run build`
   - Output directory: `dist`
   - Add environment variable: `VITE_API_URL=https://your-backend-url.railway.app`

2. **Netlify**:
   - Sign up at [netlify.com](https://netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub
   - Set build settings:
     - Base directory: `frontend`
     - Build command: `npm run build`
     - Publish directory: `frontend/dist`
   - Add environment variable: `VITE_API_URL=https://your-backend-url.railway.app`

### Option 2: Deploy with Docker (One Command)

If you have Docker installed, you can run everything locally with one command:

```bash
docker-compose up
```

This will start both backend and frontend. Access at `http://localhost:5173`

### Option 3: Render.com (Free Tier)

#### Backend on Render:

1. Sign up at [render.com](https://render.com)
2. Create a new "Web Service"
3. Connect your GitHub repository
4. Settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3
5. Deploy!

#### Frontend on Render:

1. Create a new "Static Site"
2. Connect your GitHub repository
3. Settings:
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/dist`

## Step-by-Step: Full Deployment (Railway + Vercel)

### 1. Prepare Your Code

Make sure your `frontend/src/services/api.ts` uses environment variables:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';
```

### 2. Deploy Backend to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Python
5. Add a start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
6. Deploy!
7. Copy your backend URL (e.g., `https://stock-trader-backend.railway.app`)

### 3. Update CORS in Backend

Update `backend/main.py` to allow your frontend domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://your-frontend.vercel.app",  # Add your frontend URL
        "https://your-frontend.netlify.app",  # Add your frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Add Environment Variable:
   - Key: `VITE_API_URL`
   - Value: `https://your-backend-url.railway.app`
6. Deploy!

### 5. Update Frontend API URL

After deployment, update your frontend to use the production API:

The environment variable `VITE_API_URL` will automatically be used if set.

### 6. Test Your Deployment

1. Visit your Vercel URL (e.g., `https://stock-trader.vercel.app`)
2. Try searching for a stock (e.g., AAPL)
3. Test portfolio features

## Alternative: Single Platform Deployment

### Render.com (Full Stack)

Render can host both:

1. **Backend**: Create a Web Service
2. **Frontend**: Create a Static Site
3. Both from the same GitHub repo

### Fly.io

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Run `fly launch` in project root
3. Follow prompts
4. Deploy with `fly deploy`

## Environment Variables

### Backend (Railway/Render)
- `PORT` (automatically set)
- `CORS_ORIGINS` (optional, for production)

### Frontend (Vercel/Netlify)
- `VITE_API_URL` - Your backend URL (required)

## Updating Your README

Add a "Live Demo" section at the top of your README:

```markdown
## 🌐 Live Demo

🔗 **[View Live Application](https://your-app.vercel.app)**

No installation required! Just click the link above to try it out.
```

## Troubleshooting Deployment

### CORS Errors
- Make sure your backend CORS settings include your frontend URL
- Check that `VITE_API_URL` is set correctly

### Build Failures
- Check build logs in your hosting platform
- Ensure all dependencies are in `package.json` and `requirements.txt`

### API Not Connecting
- Verify `VITE_API_URL` environment variable is set
- Check backend logs for errors
- Test backend URL directly: `https://your-backend.railway.app/docs`

## Free Hosting Options Summary

| Platform | Backend | Frontend | Free Tier | Ease of Use |
|----------|---------|----------|-----------|-------------|
| Railway | ✅ | ❌ | ✅ | ⭐⭐⭐⭐⭐ |
| Vercel | ❌ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| Netlify | ❌ | ✅ | ✅ | ⭐⭐⭐⭐ |
| Render | ✅ | ✅ | ✅ | ⭐⭐⭐⭐ |
| Fly.io | ✅ | ✅ | ✅ | ⭐⭐⭐ |

## Quick Start Commands

```bash
# Deploy backend to Railway (via GitHub)
# Just push to GitHub and connect in Railway dashboard

# Deploy frontend to Vercel (via GitHub)
# Just push to GitHub and connect in Vercel dashboard

# Local Docker deployment
docker-compose up
```

## Next Steps

1. Deploy backend to Railway
2. Deploy frontend to Vercel
3. Update README with live demo link
4. Share the link with employers! 🎉
