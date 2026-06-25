# TasteExplorer - Quick Start (5 Minutes)

Get TasteExplorer running in 5 minutes.

---

## 1. Create Spotify App (2 min)

1. Go to: https://developer.spotify.com/dashboard
2. Click **"Create app"**
3. Fill in:
   - **App name:** TasteExplorer
   - **Redirect URI:** `http://localhost:8000/auth/spotify/callback`
4. Click **"Save"**
5. Copy **Client ID** and **Client Secret**

---

## 2. Configure Credentials (1 min)

```bash
cd /path/to/tasteexplorer

# Edit .env file
nano .env
```

Replace these lines:
```env
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
```

With your actual credentials:
```env
SPOTIFY_CLIENT_ID=a1b2c3d4e5f6g7h8i9j0  # Your actual Client ID
SPOTIFY_CLIENT_SECRET=z9y8x7w6v5u4t3s2r1q0  # Your actual Client Secret
```

Save and exit (Ctrl+X, then Y, then Enter).

---

## 3. Start Application (2 min)

```bash
# Start all services
docker-compose up -d

# Wait 30 seconds for services to start
sleep 30

# Check status
docker-compose ps
```

All services should show "Up" or "healthy".

---

## 4. Use TasteExplorer

Open: http://localhost:3000

1. Click **"Connect Spotify"**
2. Log in and authorize
3. Click **"Sync"** to import your data
4. Explore your music profile!

---

## Troubleshooting

**Services won't start?**
```bash
docker-compose logs -f
```

**Credentials not working?**
```bash
./setup_spotify.sh
```

**Need to reset?**
```bash
docker-compose down -v
docker-compose up -d
```

---

**Full documentation:** [SPOTIFY_SETUP.md](SPOTIFY_SETUP.md)
