# TasteExplorer - Quick Start

Get TasteExplorer running in 5 minutes.

---

## Prerequisites

- Docker Desktop installed and running
- Spotify account

---

## Setup

### 1. Get Spotify Credentials (2 minutes)

1. Go to https://developer.spotify.com/dashboard
2. Click "Create app"
3. Fill in:
   - Name: `TasteExplorer`
   - Redirect URI: `http://localhost:8000/auth/spotify/callback`
4. Click "Save"
5. Copy **Client ID** and **Client Secret**

### 2. Configure Environment (1 minute)

```bash
cd /Users/maadhavangupta/Downloads/CS/Projects/tasteexplorer

# Copy environment file
cp .env.example .env

# Edit .env and add your credentials
# SPOTIFY_CLIENT_ID=your_client_id_here
# SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

### 3. Start Application (2 minutes)

```bash
docker-compose up -d
```

Wait 30-60 seconds for services to start.

---

## Access

- **Application**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## First Use

1. Go to http://localhost:3000
2. Click "Connect Spotify"
3. Log in and authorize
4. Click "Sync" to import your data
5. Explore your music profile!

---

## Stop

```bash
docker-compose down
```

---

## Troubleshooting

### Services not starting?
```bash
docker-compose logs -f
```

### Port conflicts?
Edit `docker-compose.yml` to use different ports.

### Auth not working?
1. Check `.env` has correct credentials
2. Verify redirect URI in Spotify Dashboard
3. Restart: `docker-compose restart api`

---

## Next Steps

See `README.md` for full documentation.

See `SETUP.md` for detailed setup guide.

See `PROJECT_SUMMARY.md` for what's implemented and what needs to be built.
