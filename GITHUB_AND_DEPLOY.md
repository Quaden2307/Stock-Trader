# 🚀 GitHub Push & Render.com Deployment Guide

## Step 1: Push All Files to GitHub

Your repository is already connected to: `https://github.com/Quaden2307/Stock-Trader.git`

### Commands to Run:

```bash
# 1. Add all files (including new ones)
git add .

# 2. Commit with a message
git commit -m "Add Docker setup and production deployment configuration"

# 3. Push to GitHub
git push origin main
```

**If you get authentication errors**, you may need to use a personal access token:
- Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate a new token with `repo` permissions
- Use the token as your password when pushing

**Alternative: Use SSH** (if you have SSH keys set up):
```bash
# Check if you have SSH remote
git remote set-url origin git@github.com:Quaden2307/Stock-Trader.git
git push origin main
```

---

## Step 2: Deploy to Render.com (Free!)

### Prerequisites
- ✅ Your code is pushed to GitHub
- ✅ You have a GitHub account (Quaden2307)

### Deployment Steps:

#### 1. Sign Up / Log In to Render
- Go to [render.com](https://render.com)
- Click **"Get Started for Free"**
- Sign up with your **GitHub account** (recommended - one click!)

#### 2. Create a New Web Service

1. Once logged in, click the **"New +"** button (top right)
2. Select **"Web Service"**

#### 3. Connect Your Repository

1. Click **"Connect account"** if you haven't connected GitHub yet
2. Authorize Render to access your repositories
3. Find and select **"Stock-Trader"** repository
4. Click **"Connect"**

#### 4. Configure the Service

Fill in the following settings:

- **Name**: `stock-trader` (or any name you like)
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)
- **Branch**: `main` (or `master` if that's your default)
- **Root Directory**: Leave empty (or `.`)
- **Environment**: Select **`Docker`** ⭐ (This is important!)
- **Dockerfile Path**: `Dockerfile` (should auto-detect)
- **Docker Context**: `.` (root directory)

#### 5. Environment Variables (Optional)

You can add these if needed (usually not required):
- `PORT`: `8000` (Render sets this automatically)
- `PYTHONUNBUFFERED`: `1` (for better logging)

#### 6. Deploy!

1. Scroll down and click **"Create Web Service"**
2. Render will start building your Docker image
3. **Wait 5-10 minutes** for the first build (it's building both frontend and backend)
4. You'll see build logs in real-time

#### 7. Get Your Live URL

Once deployment completes:
- You'll see a green "Live" status
- Your app URL will be: `https://stock-trader.onrender.com` (or similar)
- **Copy this URL** - this is what you'll share with employers!

---

## Step 3: Test Your Deployment

1. Visit your Render URL (e.g., `https://stock-trader.onrender.com`)
2. Try searching for a stock (e.g., `AAPL`)
3. Test the portfolio features
4. Check the API docs at: `https://stock-trader.onrender.com/docs`

---

## Step 4: Update Your README

Update your README.md with the live URL:

```markdown
## 🌐 Live Demo

🔗 **[View Live Application](https://stock-trader.onrender.com)**

No installation required! Just click the link above to try it out.
```

---

## Troubleshooting

### Build Fails on Render

**Error: "Dockerfile not found"**
- Make sure `Dockerfile` is in the root directory
- Check that you pushed it to GitHub

**Error: "npm install fails"**
- Check that `frontend/package.json` exists
- Verify all dependencies are listed

**Error: "Port already in use"**
- The Dockerfile should use `${PORT:-8000}` (already configured)

### App Works But API Calls Fail

**CORS Errors:**
- The backend already handles CORS
- If issues persist, add your Render URL to `CORS_ORIGINS` environment variable in Render dashboard

### App Spins Down (Takes 30 seconds to load)

- This is **normal** on Render's free tier
- The app spins down after 15 minutes of inactivity
- First request takes ~30 seconds to wake up, then it's fast
- This is free, so it's expected behavior!

---

## Quick Reference Commands

```bash
# Push to GitHub
git add .
git commit -m "Your commit message"
git push origin main

# Test Docker locally (before deploying)
docker build -t stock-trader .
docker run -p 8000:8000 stock-trader

# View logs on Render
# Go to Render dashboard → Your service → Logs tab
```

---

## What Happens After Deployment?

✅ Your app is live at a public URL  
✅ Anyone can access it (no login required)  
✅ Free SSL certificate (HTTPS)  
✅ Auto-deploys when you push to GitHub (optional)  
✅ Professional URL for your portfolio  

**Next Steps:**
1. ✅ Push code to GitHub
2. ✅ Deploy to Render
3. ✅ Test the live app
4. ✅ Add URL to your README
5. ✅ Share with employers! 🎉

---

## Need Help?

- **Render Docs**: https://render.com/docs
- **Render Support**: support@render.com
- **Your Repo**: https://github.com/Quaden2307/Stock-Trader
