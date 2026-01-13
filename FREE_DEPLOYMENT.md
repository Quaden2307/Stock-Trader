# 🆓 Free Deployment Guide - No Credit Card Required

This guide shows you how to deploy your Stock Trader app **completely free** so employers can access it easily. All options below have generous free tiers that don't require a credit card.

## 🎯 Best Free Options (Ranked by Ease)

### Option 1: Render.com (Recommended - Easiest & Most Reliable)

**Why Render?**
- ✅ **100% free tier** (no credit card needed)
- ✅ Supports Docker deployments
- ✅ Auto-deploys from GitHub
- ✅ Free SSL certificate
- ✅ Spins down after 15 min inactivity (but free!)

**Steps:**

1. **Sign up** at [render.com](https://render.com) (use GitHub login)

2. **Create a New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your `stock-trader` repo

3. **Configure the service:**
   - **Name**: `stock-trader` (or any name)
   - **Environment**: `Docker`
   - **Region**: Choose closest to you
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (or `.`)

4. **Deploy!**
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - Wait 5-10 minutes for first build

5. **Get your URL:**
   - Once deployed, you'll get a URL like: `https://stock-trader.onrender.com`
   - Share this with employers!

**Note:** The app spins down after 15 minutes of inactivity. First request after spin-down takes ~30 seconds, then it's fast.

---

### Option 2: Fly.io (Best for Always-On)

**Why Fly.io?**
- ✅ **Free tier** with 3 shared VMs
- ✅ Always-on (doesn't spin down)
- ✅ Great for Docker
- ✅ Global edge network

**Steps:**

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Sign up:**
   ```bash
   fly auth signup
   ```

3. **Create a Fly app:**
   ```bash
   cd /path/to/stock-trader
   fly launch
   ```
   - Follow prompts
   - Choose a region
   - Don't deploy a database (we don't need one)

4. **Create `fly.toml`** (if not auto-generated):
   ```toml
   app = "your-app-name"
   primary_region = "iad"

   [build]

   [http_service]
     internal_port = 8000
     force_https = true
     auto_stop_machines = false
     auto_start_machines = true
     min_machines_running = 1

   [[vm]]
     memory_mb = 256
   ```

5. **Deploy:**
   ```bash
   fly deploy
   ```

6. **Get your URL:**
   - Your app will be at: `https://your-app-name.fly.dev`

---

### Option 3: Railway (Simple but Limited Free Tier)

**Why Railway?**
- ✅ Very easy setup
- ✅ Auto-detects Docker
- ⚠️ Free tier gives $5 credit/month (usually enough for small apps)

**Steps:**

1. **Sign up** at [railway.app](https://railway.app) (GitHub login)

2. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Railway auto-detects:**
   - It will detect your Dockerfile
   - Click "Deploy Now"

4. **Get your URL:**
   - Railway provides a URL like: `https://stock-trader-production.up.railway.app`

**Note:** Railway's free tier gives $5/month credit. Your app will use ~$0.50-1/month, so you get ~5 months free.

---

### Option 4: Google Cloud Run (Most Generous Free Tier)

**Why Cloud Run?**
- ✅ **2 million requests/month free**
- ✅ **400,000 GB-seconds compute free**
- ✅ Pay only for what you use beyond free tier
- ✅ Auto-scales to zero when not in use

**Steps:**

1. **Install Google Cloud SDK:**
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Sign up** at [cloud.google.com](https://cloud.google.com) (free $300 credit for new users)

3. **Create a project:**
   ```bash
   gcloud init
   gcloud projects create stock-trader-app
   gcloud config set project stock-trader-app
   ```

4. **Enable Cloud Run:**
   ```bash
   gcloud services enable run.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   ```

5. **Deploy:**
   ```bash
   gcloud run deploy stock-trader \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8000
   ```

6. **Get your URL:**
   - Cloud Run provides a URL like: `https://stock-trader-xxxxx-uc.a.run.app`

---

## 🐳 Docker Deployment (Any Platform)

All the platforms above support Docker. Your app is already configured with a production-ready `Dockerfile`.

### Local Testing

Test your Docker build locally:

```bash
# Build the image
docker build -t stock-trader .

# Run it
docker run -p 8000:8000 stock-trader

# Visit http://localhost:8000
```

### Using docker-compose (Production)

```bash
# Production mode
docker-compose --profile prod up -d

# Access at http://localhost:8000
```

---

## 📝 Quick Comparison

| Platform | Free Tier | Always-On | Ease | Best For |
|----------|-----------|-----------|------|----------|
| **Render** | ✅ Yes | ❌ Spins down | ⭐⭐⭐⭐⭐ | Quick demos |
| **Fly.io** | ✅ Yes | ✅ Yes | ⭐⭐⭐⭐ | Always available |
| **Railway** | ⚠️ $5/month | ✅ Yes | ⭐⭐⭐⭐⭐ | Easiest setup |
| **Cloud Run** | ✅ Generous | ❌ Scales to zero | ⭐⭐⭐ | Enterprise-ready |

---

## 🚀 Recommended: Render.com (5 minutes setup)

**Why Render is best for employers:**
1. ✅ **No credit card needed**
2. ✅ **One-click deploy from GitHub**
3. ✅ **Free SSL (HTTPS)**
4. ✅ **Professional URL** (your-app.onrender.com)
5. ✅ **Works immediately** after deployment

**Quick Render Setup:**
1. Push your code to GitHub
2. Sign up at render.com with GitHub
3. Click "New Web Service" → Select repo → Choose "Docker"
4. Click "Create Web Service"
5. Wait 5-10 minutes
6. Share the URL with employers! 🎉

---

## 🔧 Troubleshooting

### Render: App spins down
- **Solution**: This is normal! First request takes ~30 seconds, then it's fast.
- **Tip**: Add a health check endpoint to keep it warm (optional)

### Fly.io: Build fails
- **Solution**: Make sure your Dockerfile is in the root directory
- **Check**: Run `docker build -t test .` locally first

### Railway: Out of credits
- **Solution**: Railway gives $5/month free. Your app uses ~$0.50/month.
- **Tip**: Monitor usage in Railway dashboard

### CORS errors
- **Solution**: The backend already handles CORS. If you get errors, check that your frontend URL is in `CORS_ORIGINS` environment variable.

---

## 📧 Sharing with Employers

Once deployed, update your README:

```markdown
## 🌐 Live Demo

🔗 **[View Live Application](https://your-app.onrender.com)**

No installation required! Just click the link above to try it out.
```

---

## 🎉 You're Done!

Your app is now live and accessible to anyone with the URL. No installation needed for employers - they just click and use!

**Next Steps:**
1. Deploy to Render (recommended) or another platform
2. Update your README with the live URL
3. Add the URL to your resume/portfolio
4. Share with employers! 🚀
