# Spotify Authentication Setup Guide

Complete guide to configure Spotify OAuth for TasteExplorer.

---

## Step 1: Create Spotify Developer App

### 1.1 Go to Spotify Developer Dashboard

Visit: https://developer.spotify.com/dashboard

### 1.2 Log In

Log in with your Spotify account (create one if needed).

### 1.3 Create New App

1. Click **"Create app"** button
2. Fill in the form:
   - **App name:** `TasteExplorer`
   - **App description:** `Music discovery platform using graph-based recommendations`
   - **Redirect URIs:** `http://localhost:8000/auth/spotify/callback`
   - **Which API/SDKs are you planning to use?** Check **Web API**
3. Accept terms and click **"Save"**

### 1.4 Get Credentials

1. Click on your newly created app
2. Click **"Settings"** in the top right
3. You'll see:
   - **Client ID** - Copy this
   - **Client Secret** - Click "View client secret" and copy

**Keep these credentials private!**

---

## Step 2: Configure Environment Variables

### 2.1 Edit .env File

```bash
cd /path/to/tasteexplorer
nano .env  # or use your preferred editor
```

### 2.2 Add Your Credentials

Replace the placeholder values:

```env
# Before
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here

# After (example - use YOUR credentials)
SPOTIFY_CLIENT_ID=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
SPOTIFY_CLIENT_SECRET=z9y8x7w6v5u4t3s2r1q0p9o8n7m6l5k4
```

**Important:** These are example values. Use your actual credentials from Spotify.

### 2.3 Verify Other Settings

Make sure these are set correctly:

```env
SPOTIFY_REDIRECT_URI=http://localhost:8000/auth/spotify/callback
FRONTEND_URL=http://localhost:3000
DATABASE_URL=postgresql://tasteexplorer:tasteexplorer@localhost:5432/tasteexplorer
```

---

## Step 3: Start the Application

### 3.1 Start Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- FastAPI backend (port 8000)
- Next.js frontend (port 3000)

### 3.2 Wait for Services

Wait 30-60 seconds for all services to start.

Check status:
```bash
docker-compose ps
```

All services should show "Up" or "healthy" status.

### 3.3 Check Logs (Optional)

```bash
# View all logs
docker-compose logs -f

# View API logs only
docker-compose logs -f api

# View frontend logs only
docker-compose logs -f web
```

Press `Ctrl+C` to stop viewing logs.

---

## Step 4: Test Authentication

### 4.1 Open Application

Open your browser and go to: http://localhost:3000

### 4.2 Click "Connect Spotify"

You should see a button that says "Connect Spotify". Click it.

### 4.3 Authorize with Spotify

You'll be redirected to Spotify's authorization page:

1. Log in with your Spotify account (if not already logged in)
2. Review the permissions requested:
   - Read your top artists and tracks
   - Read your saved tracks
   - Read your recently played tracks
   - Access your email address
3. Click **"Agree"** or **"Accept"**

### 4.4 Redirected to Dashboard

After authorization, you'll be redirected back to TasteExplorer dashboard.

You should see: `Dashboard · Last synced: Never`

### 4.5 Sync Your Data

Click the **"Sync"** button in the top right to import your Spotify data.

This will:
- Fetch your top 50 artists (3 time ranges)
- Fetch your top 50 tracks (3 time ranges)
- Fetch audio features for all tracks

Wait 30-60 seconds for sync to complete.

---

## Troubleshooting

### Error: "Invalid client"

**Cause:** Client ID or Client Secret is incorrect.

**Fix:**
1. Check your .env file
2. Verify credentials match Spotify Dashboard
3. Make sure there are no extra spaces or quotes
4. Restart API: `docker-compose restart api`

### Error: "Invalid redirect URI"

**Cause:** Redirect URI in Spotify Dashboard doesn't match.

**Fix:**
1. Go to Spotify Dashboard → Your App → Settings
2. Under "Redirect URIs", make sure you have exactly:
   ```
   http://localhost:8000/auth/spotify/callback
   ```
3. Click "Save"
4. Try authenticating again

### Error: "Cannot connect to API"

**Cause:** API service not running or wrong URL.

**Fix:**
```bash
# Check if API is running
curl http://localhost:8000/health

# Should return: {"status":"healthy"}

# If not, check logs
docker-compose logs api

# Restart API
docker-compose restart api
```

### Error: "Database connection failed"

**Cause:** PostgreSQL not running or wrong credentials.

**Fix:**
```bash
# Check PostgreSQL status
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres

# Restart PostgreSQL
docker-compose restart postgres

# Recreate all services if needed
docker-compose down
docker-compose up -d
```

### Stuck on "Syncing..."

**Cause:** Spotify API rate limit or network issue.

**Fix:**
1. Wait 2 minutes
2. Refresh the page
3. Check API logs: `docker-compose logs api | grep -i error`
4. Try syncing again

### Authentication works but no data appears

**Cause:** Data not synced yet or sync failed.

**Fix:**
1. Click "Sync" button on dashboard
2. Wait for completion
3. Refresh page
4. Check API logs for errors

---

## Verification Checklist

Use this checklist to verify everything is working:

- [ ] .env file exists with Spotify credentials
- [ ] Spotify app created in developer dashboard
- [ ] Redirect URI matches exactly: `http://localhost:8000/auth/spotify/callback`
- [ ] All services running: `docker-compose ps` shows 4 services
- [ ] Frontend accessible: http://localhost:3000 loads
- [ ] API accessible: http://localhost:8000/health returns `{"status":"healthy"}`
- [ ] Can click "Connect Spotify" and see Spotify auth page
- [ ] After authorization, redirected to dashboard
- [ ] Can click "Sync" and data imports successfully
- [ ] Top tracks and artists appear on dashboard

---

## Quick Setup Script

Run the automated setup checker:

```bash
./setup_spotify.sh
```

This will check:
- If .env file exists
- If Spotify credentials are configured
- Provide next steps

---

## Security Notes

### For Development

The current setup is for local development only:
- Uses `http://localhost` (not HTTPS)
- Stores tokens in database
- No additional encryption

### For Production

If deploying to production, you must:

1. **Use HTTPS** everywhere
2. **Update redirect URI** in Spotify Dashboard to your production domain
3. **Update .env** with production URLs:
   ```env
   SPOTIFY_REDIRECT_URI=https://yourdomain.com/auth/spotify/callback
   FRONTEND_URL=https://yourdomain.com
   ```
4. **Encrypt tokens** at rest (database encryption)
5. **Use secrets management** (AWS Secrets Manager, etc.)
6. **Add rate limiting**
7. **Add proper CORS configuration**

---

## Need Help?

### Check Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f web
docker-compose logs -f postgres
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart api
docker-compose restart web
```

### Reset Everything

If things are completely broken:

```bash
# Stop and remove everything
docker-compose down -v

# Remove .env (optional - you'll need to reconfigure)
# rm .env

# Start fresh
cp .env.example .env
# Edit .env with your credentials
docker-compose up -d
```

### Still Having Issues?

1. Check you're using valid Spotify credentials
2. Try with a different Spotify account
3. Make sure no other services are using ports 3000, 5432, 6379, or 8000
4. Check Docker has enough resources (4GB RAM, 2 CPU cores)

---

## Success Indicators

You know it's working when:

✅ All 4 services show "Up" in `docker-compose ps`
✅ http://localhost:3000 shows TasteExplorer landing page
✅ http://localhost:8000/health returns `{"status":"healthy"}`
✅ Clicking "Connect Spotify" redirects to Spotify
✅ After authorizing, you land on TasteExplorer dashboard
✅ Clicking "Sync" imports your data
✅ Dashboard shows your top tracks and artists

**You're ready to use TasteExplorer! 🎵**
