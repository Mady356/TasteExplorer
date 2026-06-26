# TasteExplorer Deployment Guide

Complete guide to deploying TasteExplorer to production.

**Stack:**
- Frontend: Next.js on **Vercel**
- Backend: FastAPI on **Render** or **Railway**
- Database: PostgreSQL on **Supabase** or **Railway**

---

## 📋 Prerequisites

1. **GitHub Repository** - Push your code to GitHub
2. **Spotify Developer Account** - https://developer.spotify.com/dashboard
3. **Vercel Account** - https://vercel.com (free tier available)
4. **Render Account** - https://render.com (free tier available)
   - OR **Railway Account** - https://railway.app (free trial available)

---

## 🚀 Deployment Steps

### Step 1: Set Up Spotify App

1. Go to https://developer.spotify.com/dashboard
2. Click "Create App"
3. Fill in:
   - App name: `TasteExplorer`
   - App description: `Music discovery platform`
   - Redirect URI: `https://your-api-domain.com/auth/spotify/callback` (update later)
   - Check "Web API"
4. Save and note:
   - **Client ID**
   - **Client Secret**

---

### Step 2: Deploy Backend (Option A: Render)

#### 2.1 Create PostgreSQL Database

1. Go to https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Configure:
   - Name: `tasteexplorer-db`
   - Database: `tasteexplorer`
   - User: `tasteexplorer`
   - Region: Choose closest to you
   - Plan: Free (or Starter for production)
4. Click "Create Database"
5. Wait for database to provision (~2 minutes)
6. Copy **Internal Database URL** (starts with `postgresql://`)

#### 2.2 Deploy API Service

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** `tasteexplorer-api`
   - **Region:** Same as database
   - **Branch:** `main`
   - **Root Directory:** Leave empty
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r apps/api/requirements.txt`
   - **Start Command:** `cd apps/api && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click "Advanced" and add environment variables:

```bash
# Database (from Step 2.1)
DATABASE_URL=postgresql://user:pass@host/db

# Spotify (from Step 1)
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=https://tasteexplorer-api.onrender.com/auth/spotify/callback

# CORS (update after deploying frontend)
CORS_ORIGINS=https://your-app.vercel.app

# Frontend URL (update after deploying frontend)
FRONTEND_URL=https://your-app.vercel.app

# Environment
ENVIRONMENT=production
```

6. Click "Create Web Service"
7. Wait for deployment (~5 minutes)
8. Copy your API URL: `https://tasteexplorer-api.onrender.com`

#### 2.3 Update Spotify Redirect URI

1. Go back to Spotify Developer Dashboard
2. Edit your app
3. Update Redirect URI to: `https://tasteexplorer-api.onrender.com/auth/spotify/callback`
4. Save

---

### Step 2: Deploy Backend (Option B: Railway)

#### 2.1 Create Project

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository

#### 2.2 Add PostgreSQL Database

1. Click "New" → "Database" → "Add PostgreSQL"
2. Railway automatically creates database and sets `DATABASE_URL`

#### 2.3 Configure Service

1. Click on your service
2. Go to "Settings"
3. Set:
   - **Root Directory:** Leave empty
   - **Build Command:** `pip install -r apps/api/requirements.txt`
   - **Start Command:** `cd apps/api && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Go to "Variables" tab
5. Add environment variables (same as Render above)
6. Deploy!
7. Copy your API URL from "Settings" → "Domains"

---

### Step 3: Deploy Frontend (Vercel)

#### 3.1 Import Project

1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset:** Next.js
   - **Root Directory:** `apps/web`
   - **Build Command:** `npm run build` (auto-detected)
   - **Output Directory:** `.next` (auto-detected)

#### 3.2 Set Environment Variables

Click "Environment Variables" and add:

```bash
# API URL (from Step 2)
NEXT_PUBLIC_API_URL=https://tasteexplorer-api.onrender.com
```

Or if using Railway:
```bash
NEXT_PUBLIC_API_URL=https://tasteexplorer-api.up.railway.app
```

#### 3.3 Deploy

1. Click "Deploy"
2. Wait for build (~2 minutes)
3. Copy your frontend URL: `https://your-app.vercel.app`

---

### Step 4: Update Backend CORS

Now that you have your frontend URL, update the backend:

#### If using Render:
1. Go to Render Dashboard → Your API Service
2. Go to "Environment"
3. Update:
   - `CORS_ORIGINS` = `https://your-app.vercel.app`
   - `FRONTEND_URL` = `https://your-app.vercel.app`
4. Save (triggers automatic redeploy)

#### If using Railway:
1. Go to Railway Dashboard → Your Service
2. Go to "Variables"
3. Update same variables
4. Redeploy

---

### Step 5: Test Deployment

1. Visit your frontend: `https://your-app.vercel.app`
2. Check API health: `https://tasteexplorer-api.onrender.com/health`
   - Should return: `{"status": "healthy", "service": "tasteexplorer-api", ...}`
3. Test Spotify login flow
4. Verify recommendations work

---

## 🔧 Environment Variables Reference

### Backend (Render/Railway)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | ✅ | `postgresql://user:pass@host/db` | PostgreSQL connection string |
| `SPOTIFY_CLIENT_ID` | ✅ | `abc123...` | Spotify app client ID |
| `SPOTIFY_CLIENT_SECRET` | ✅ | `xyz789...` | Spotify app client secret |
| `SPOTIFY_REDIRECT_URI` | ✅ | `https://api.com/auth/spotify/callback` | OAuth callback URL |
| `CORS_ORIGINS` | ✅ | `https://app.vercel.app` | Frontend URL (comma-separated) |
| `FRONTEND_URL` | ✅ | `https://app.vercel.app` | Frontend URL for redirects |
| `ENVIRONMENT` | ✅ | `production` | Environment name |
| `REDIS_URL` | ⬜ | `redis://default:pass@host:6379` | Optional: Redis for caching |
| `SQL_ECHO` | ⬜ | `false` | Optional: Log SQL queries |

### Frontend (Vercel)

| Variable | Required | Example | Description |
|----------|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | ✅ | `https://api.onrender.com` | Backend API URL |

---

## 🔍 Troubleshooting

### Backend won't start

**Check logs:**
- Render: Dashboard → Service → Logs
- Railway: Dashboard → Service → Deployments → Click deployment → Logs

**Common issues:**
1. Missing environment variables → Add all required vars
2. Database connection failed → Check `DATABASE_URL` format
3. Port binding error → Make sure start command uses `--port $PORT`

### CORS errors in frontend

**Symptoms:** Browser console shows `CORS policy` errors

**Fix:**
1. Check `CORS_ORIGINS` in backend includes your frontend URL
2. Must be exact match: `https://app.vercel.app` (no trailing slash)
3. For multiple origins: `https://app1.com,https://app2.com`
4. Redeploy backend after changing

### Spotify login not working

**Check:**
1. Redirect URI in Spotify Dashboard matches backend URL exactly
2. Format: `https://your-api.onrender.com/auth/spotify/callback`
3. `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` are correct
4. `FRONTEND_URL` is set correctly for post-auth redirect

### Database connection issues

**Render:**
- Use **Internal Database URL** (starts with `postgresql://`)
- Don't use External URL in production

**Railway:**
- Use `${{Postgres.DATABASE_URL}}` variable reference
- Railway automatically injects it

### Frontend can't reach backend

**Check:**
1. `NEXT_PUBLIC_API_URL` in Vercel is correct
2. Backend health endpoint responds: `curl https://api.com/health`
3. No typos in URL (http vs https, trailing slashes)
4. Redeploy frontend after changing env vars

---

## 📊 Health Checks

### Backend Health Endpoint

```bash
curl https://tasteexplorer-api.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "tasteexplorer-api",
  "version": "0.1.0",
  "environment": "production"
}
```

### Check Database Connection

```bash
curl https://tasteexplorer-api.onrender.com/
```

Expected response:
```json
{
  "name": "TasteExplorer API",
  "version": "0.1.0",
  "status": "running"
}
```

If this works, database is connected (lifespan initializes DB).

---

## 🔄 Continuous Deployment

Both Render and Railway support automatic deployments:

1. Push to GitHub `main` branch
2. Backend redeploys automatically (~5 minutes)
3. Frontend redeploys automatically (~2 minutes)

**Disable auto-deploy:**
- Render: Service Settings → Build & Deploy → Auto-Deploy: Off
- Railway: Service Settings → Triggers → GitHub: Off

---

## 💰 Cost Estimates

### Free Tier (Good for Demo/Testing)

- **Render:** Free PostgreSQL + Free Web Service
  - ⚠️ Services sleep after 15 min inactivity (cold start ~30s)
  - ⚠️ 750 hours/month limit across all services
- **Railway:** $5/month credit (free trial)
  - No cold starts
  - Expires after trial
- **Vercel:** Free frontend hosting
  - 100 GB bandwidth/month
  - No cold starts

**Total:** $0/month (Render free tier)

### Production (Paid)

- **Render Starter:**
  - PostgreSQL: $7/month (1GB storage)
  - Web Service: $7/month (always on)
- **Railway:**
  - Pay per usage: ~$5-15/month (typical)
- **Vercel:** Free (or $20/month Pro for more features)

**Total:** ~$14-35/month

---

## 🎯 Production Checklist

Before going live:

- [ ] Set all required environment variables
- [ ] Update Spotify redirect URI to production URL
- [ ] Update CORS_ORIGINS to production frontend URL
- [ ] Test Spotify OAuth flow end-to-end
- [ ] Test recommendations generation
- [ ] Set up custom domain (optional)
- [ ] Enable HTTPS (automatic on Render/Vercel)
- [ ] Monitor logs for errors
- [ ] Set up database backups (Render: automatic, Railway: manual)

---

## 🔐 Security Notes

1. **Never commit `.env` files** - Already in `.gitignore`
2. **Use environment variables** for all secrets
3. **Rotate credentials** regularly (Spotify, database)
4. **Enable database SSL** (automatic on Render/Railway)
5. **Monitor access logs** for suspicious activity
6. **Keep dependencies updated** - `pip list --outdated`

---

## 🆘 Support

**Issues:**
- Check Render/Railway/Vercel status pages
- Review deployment logs
- Search error messages
- Open GitHub issue

**Useful Links:**
- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- Vercel Docs: https://vercel.com/docs
- Spotify API Docs: https://developer.spotify.com/documentation

---

## 🎉 Success!

If all steps completed successfully:

✅ Backend API running at `https://tasteexplorer-api.onrender.com`  
✅ Frontend app running at `https://your-app.vercel.app`  
✅ Database connected and initialized  
✅ Spotify OAuth working  
✅ CORS configured  
✅ Recommendations generating  

**Next steps:**
- Share your app!
- Monitor usage
- Gather feedback
- Iterate and improve

---

Built with 🎵 for transparent, explainable music recommendations.
