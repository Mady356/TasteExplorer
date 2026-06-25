# TasteExplorer Setup Guide

Complete step-by-step setup instructions for TasteExplorer.

---

## Prerequisites

Before starting, ensure you have:

- **Docker Desktop** installed ([download](https://www.docker.com/products/docker-desktop))
- **Git** installed
- **Spotify Developer Account** (free at [developer.spotify.com](https://developer.spotify.com))

---

## Step 1: Spotify App Setup

### 1.1 Create Spotify App

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click "Create app"
3. Fill in details:
   - **App name**: TasteExplorer
   - **App description**: Music discovery platform
   - **Redirect URI**: `http://localhost:8000/auth/spotify/callback`
   - **API**: Select "Web API"
4. Accept terms and click "Save"

### 1.2 Get Credentials

1. On your app page, click "Settings"
2. Copy **Client ID**
3. Click "View client secret" and copy **Client Secret**
4. Keep these safe - you'll need them in Step 3

---

## Step 2: Clone and Navigate

```bash
cd /Users/maadhavangupta/Downloads/CS/Projects/tasteexplorer
```

---

## Step 3: Configure Environment

### 3.1 Create Environment File

```bash
cp .env.example .env
```

### 3.2 Edit .env File

Open `.env` in your text editor and add your Spotify credentials:

```env
SPOTIFY_CLIENT_ID=your_client_id_from_step_1
SPOTIFY_CLIENT_SECRET=your_client_secret_from_step_1
SPOTIFY_REDIRECT_URI=http://localhost:8000/auth/spotify/callback
FRONTEND_URL=http://localhost:3000
```

Save the file.

---

## Step 4: Start Services

### 4.1 Start with Docker Compose

```bash
docker-compose up -d
```

This will:
1. Download required Docker images
2. Start PostgreSQL database
3. Start Redis cache
4. Build and start FastAPI backend
5. Build and start Next.js frontend

**First run takes 3-5 minutes to download and build everything.**

### 4.2 Verify Services

Check that all services are running:

```bash
docker-compose ps
```

You should see:
- `tasteexplorer_postgres` (healthy)
- `tasteexplorer_redis` (healthy)
- `tasteexplorer_api` (running)
- `tasteexplorer_web` (running)

### 4.3 View Logs (Optional)

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f web
```

Press `Ctrl+C` to stop viewing logs.

---

## Step 5: Access Application

Once services are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

---

## Step 6: First Login

1. Go to http://localhost:3000
2. Click "Connect Spotify"
3. Log in with your Spotify account
4. Authorize TasteExplorer
5. You'll be redirected to the dashboard

---

## Step 7: Sync Your Music

1. On the dashboard, click the "Sync" button
2. Wait for data sync to complete (30-60 seconds)
3. Your top artists and tracks will appear

---

## Troubleshooting

### Services Won't Start

```bash
# Stop everything
docker-compose down

# Remove volumes and restart
docker-compose down -v
docker-compose up -d
```

### "Connection Refused" Errors

**Wait 30-60 seconds** - services need time to start.

Check logs:
```bash
docker-compose logs api
docker-compose logs web
```

### Spotify Auth Fails

1. Verify `.env` has correct credentials
2. Check Redirect URI in Spotify Dashboard matches exactly:
   `http://localhost:8000/auth/spotify/callback`
3. Restart services:
   ```bash
   docker-compose restart api
   ```

### Database Issues

Reset database:
```bash
docker-compose down -v
docker-compose up -d
```

### Port Already in Use

If ports 3000, 5432, 6379, or 8000 are in use:

1. Stop conflicting services
2. OR edit `docker-compose.yml` to use different ports

### Can't Build Frontend

Make sure Docker has enough resources:
- Open Docker Desktop
- Go to Settings > Resources
- Allocate at least:
  - **4 GB RAM**
  - **2 CPUs**

---

## Alternative: Local Development (Without Docker)

### Backend Only

```bash
cd apps/api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL manually (brew, apt, etc.)
# Update DATABASE_URL in .env

# Run server
python main.py
```

### Frontend Only

```bash
cd apps/web

# Install dependencies
npm install

# Create .env.local
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run dev server
npm run dev
```

---

## Next Steps

1. ✅ Services running
2. ✅ Logged in via Spotify
3. ✅ Data synced

Now you can:

- **Explore Dashboard** - View your top artists and tracks
- **Visit Discovery** - See mock recommendations (real engine TBD)
- **Check Graph** - View taste graph visualization shell

---

## Stopping Services

```bash
# Stop services (data persists)
docker-compose down

# Stop and remove all data
docker-compose down -v
```

---

## Updating Code

After making code changes:

```bash
# Rebuild and restart
docker-compose up -d --build

# Or restart specific service
docker-compose restart api
docker-compose restart web
```

---

## Useful Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Restart service
docker-compose restart api

# Rebuild service
docker-compose up -d --build api

# Access database
docker exec -it tasteexplorer_postgres psql -U tasteexplorer

# Access Redis
docker exec -it tasteexplorer_redis redis-cli

# Remove everything
docker-compose down -v
```

---

## Getting Help

1. Check logs: `docker-compose logs -f`
2. Review README.md
3. Check API docs: http://localhost:8000/docs
4. Verify environment variables in `.env`

---

## Production Deployment (Future)

For production deployment:

1. Set `ENVIRONMENT=production` in `.env`
2. Use strong database passwords
3. Set up SSL/TLS
4. Configure proper CORS origins
5. Set up monitoring and logging
6. Use managed database (not Docker)
7. Deploy to cloud platform (AWS, GCP, Vercel, Railway)

---

**You're all set! 🎉**

Explore your music taste with TasteExplorer.
