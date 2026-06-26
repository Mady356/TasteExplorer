# TasteExplorer Deployment Checklist

Quick reference for deploying TasteExplorer to production.

---

## ✅ Pre-Deployment

- [ ] Code pushed to GitHub
- [ ] Spotify Developer app created
- [ ] Spotify Client ID and Secret obtained
- [ ] Vercel account created
- [ ] Render or Railway account created

---

## 🗄️ Database Setup

### Render
- [ ] PostgreSQL database created
- [ ] Internal Database URL copied
- [ ] Database region noted

### Railway
- [ ] PostgreSQL database added to project
- [ ] `DATABASE_URL` automatically set

---

## 🔧 Backend Deployment

### Render
- [ ] Web service created from GitHub repo
- [ ] Build command: `pip install -r apps/api/requirements.txt`
- [ ] Start command: `cd apps/api && uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Python version: 3.12
- [ ] Region matches database

### Railway
- [ ] Project created from GitHub repo
- [ ] Build command configured
- [ ] Start command configured
- [ ] Auto-deploys enabled

### Environment Variables (Both)
- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `SPOTIFY_CLIENT_ID` - From Spotify Dashboard
- [ ] `SPOTIFY_CLIENT_SECRET` - From Spotify Dashboard
- [ ] `SPOTIFY_REDIRECT_URI` - `https://your-api.com/auth/spotify/callback`
- [ ] `CORS_ORIGINS` - Frontend URL (update after frontend deployed)
- [ ] `FRONTEND_URL` - Frontend URL (update after frontend deployed)
- [ ] `ENVIRONMENT` - `production`

### After Deployment
- [ ] Backend URL copied (e.g., `https://tasteexplorer-api.onrender.com`)
- [ ] Health check tested: `https://your-api.com/health`
- [ ] Spotify Redirect URI updated in Spotify Dashboard

---

## 🎨 Frontend Deployment (Vercel)

- [ ] Project imported from GitHub
- [ ] Framework: Next.js (auto-detected)
- [ ] Root directory: `apps/web`
- [ ] Build command: `npm run build` (auto-detected)
- [ ] Environment variable added:
  - [ ] `NEXT_PUBLIC_API_URL` - Backend URL from above
- [ ] Deployed successfully
- [ ] Frontend URL copied (e.g., `https://your-app.vercel.app`)

---

## 🔗 Post-Deployment Updates

### Update Backend Environment Variables
- [ ] Set `CORS_ORIGINS` to frontend URL
- [ ] Set `FRONTEND_URL` to frontend URL
- [ ] Trigger redeploy (automatic on save in Render)

### Update Spotify Dashboard
- [ ] Redirect URI matches: `https://your-api.com/auth/spotify/callback`
- [ ] No typos in URL

---

## 🧪 Testing

- [ ] Visit frontend: `https://your-app.vercel.app`
- [ ] Check API health: `curl https://your-api.com/health`
  - Expected: `{"status": "healthy", ...}`
- [ ] Test Spotify login flow
- [ ] Authorize with Spotify account
- [ ] Verify redirect back to frontend works
- [ ] Check user dashboard loads
- [ ] Generate recommendations
- [ ] Verify tracks/artists display

---

## 🐛 Common Issues & Fixes

### Issue: CORS errors in browser console
**Fix:**
- Check `CORS_ORIGINS` in backend includes frontend URL exactly
- No trailing slash: `https://app.vercel.app` ✅ not `https://app.vercel.app/` ❌
- Redeploy backend after changing

### Issue: Spotify login fails
**Fix:**
- Verify Redirect URI in Spotify Dashboard matches backend URL
- Format: `https://your-api.onrender.com/auth/spotify/callback`
- Check `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` are correct

### Issue: Backend returns 500 errors
**Fix:**
- Check Render/Railway logs for errors
- Verify `DATABASE_URL` is correct
- Ensure all environment variables are set
- Check database is running

### Issue: Frontend shows "Failed to fetch"
**Fix:**
- Verify `NEXT_PUBLIC_API_URL` in Vercel is correct
- Check backend health endpoint responds
- Ensure CORS is configured
- Check network tab for actual error

### Issue: Cold starts (Render free tier)
**Info:**
- Free tier services sleep after 15 min inactivity
- First request after sleep takes ~30s
- Upgrade to Starter plan ($7/month) for always-on

---

## 📊 Verification Commands

```bash
# Check backend health
curl https://your-api.onrender.com/health

# Check API root
curl https://your-api.onrender.com/

# Check frontend loads
curl -I https://your-app.vercel.app

# Check CORS headers
curl -I -X OPTIONS https://your-api.onrender.com/health \
  -H "Origin: https://your-app.vercel.app" \
  -H "Access-Control-Request-Method: GET"
```

---

## 🎯 Success Criteria

✅ **Backend:**
- Health endpoint returns `{"status": "healthy"}`
- Root endpoint returns API info
- Logs show "Database initialized"
- No error logs on startup

✅ **Frontend:**
- Homepage loads in browser
- No console errors (except dev warnings)
- API requests succeed (check Network tab)

✅ **Integration:**
- Spotify login button works
- OAuth flow completes successfully
- User redirected back to app
- Dashboard shows user data
- Recommendations generate

---

## 📝 Environment Variables Summary

### Backend (Render/Railway)
```bash
DATABASE_URL=postgresql://user:pass@host:5432/db
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=https://your-api.onrender.com/auth/spotify/callback
CORS_ORIGINS=https://your-app.vercel.app
FRONTEND_URL=https://your-app.vercel.app
ENVIRONMENT=production
```

### Frontend (Vercel)
```bash
NEXT_PUBLIC_API_URL=https://your-api.onrender.com
```

---

## 🔄 Redeployment

**When to redeploy:**
- Code changes pushed to main branch (automatic)
- Environment variables changed (automatic on Render)
- Database schema changes (manual migration needed)

**Manual redeploy:**
- Render: Dashboard → Service → Manual Deploy → Deploy latest commit
- Railway: Dashboard → Service → Deployments → Redeploy
- Vercel: Dashboard → Project → Deployments → Redeploy

---

## 💡 Tips

1. **Use Internal Database URL** on Render (faster, private network)
2. **Set all env vars before first deploy** to avoid redeploys
3. **Test locally first** with production-like env vars
4. **Monitor logs** during first deploy for errors
5. **Keep Spotify Dashboard open** for easy redirect URI updates
6. **Save all URLs** (API, frontend, database) in a safe place

---

## 📞 Help

**Stuck?** See full deployment guide: [`DEPLOYMENT.md`](./DEPLOYMENT.md)

**Still stuck?** Check:
- Render/Railway/Vercel status pages
- Service logs for error messages
- GitHub Issues for similar problems

---

Built with 🎵 for transparent, explainable music recommendations.
