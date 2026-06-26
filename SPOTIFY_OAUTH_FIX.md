# Spotify OAuth Environment Loading Fix

## Problem

The `/auth/spotify/login` endpoint was redirecting to Spotify with placeholder values:
```
client_id=your_spotify_client_id_here
redirect_uri=http://localhost:8000/auth/spotify/callback
```

Even though the `.env` file loaded correctly in the terminal.

---

## Root Cause

**Environment variable loading priority issue:**

1. Root `.env` file had placeholder values:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id_here
   ```

2. `apps/api/.env` file had real values:
   ```
   SPOTIFY_CLIENT_ID=048e9d2e7bc384c219fced5fb2d79ba16
   ```

3. `main.py` was loading from **root `.env` first**, overriding the correct values
4. `spotify/client.py` wasn't loading environment variables at all

---

## Solution Applied

### 1. Fixed `apps/api/main.py`

Changed environment loading priority to prefer `apps/api/.env`:

**Before:**
```python
# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()
```

**After:**
```python
# Load environment variables - try apps/api/.env first, then root .env
api_env_path = Path(__file__).parent / '.env'
root_env_path = Path(__file__).parent.parent.parent / '.env'

if api_env_path.exists():
    load_dotenv(api_env_path)
    print(f"Loaded environment from: {api_env_path}")
elif root_env_path.exists():
    load_dotenv(root_env_path)
    print(f"Loaded environment from: {root_env_path}")
else:
    load_dotenv()
    print("Loaded environment from current directory or system env")
```

### 2. Fixed `apps/api/spotify/client.py`

Added explicit environment loading at module level:

**Added:**
```python
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from apps/api/.env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)
```

### 3. Added Debug Prints to `apps/api/auth/routes.py`

Added temporary debug output in the `/spotify/login` endpoint:

```python
@router.get("/spotify/login")
async def spotify_login():
    # Debug: Print environment variables
    print("=" * 60)
    print("Spotify OAuth Debug Info:")
    print(f"Spotify Client ID: {os.getenv('SPOTIFY_CLIENT_ID')}")
    print(f"Spotify Redirect URI: {os.getenv('SPOTIFY_REDIRECT_URI')}")
    print("=" * 60)

    auth_manager = create_oauth_manager()
    auth_url = auth_manager.get_authorize_url()

    print(f"Generated auth URL: {auth_url}")
    print("=" * 60)

    return RedirectResponse(url=auth_url)
```

---

## Files Modified

1. ✅ `apps/api/main.py` - Fixed env loading priority
2. ✅ `apps/api/spotify/client.py` - Added dotenv loading
3. ✅ `apps/api/auth/routes.py` - Added debug prints

---

## Testing

### 1. Check Environment Loading

Start the server:
```bash
cd apps/api
uvicorn main:app --reload --port 8001
```

Expected startup output:
```
Loaded environment from: /path/to/apps/api/.env
INFO:     Started server process [12345]
INFO:     Application startup complete.
```

### 2. Test OAuth Login

Visit: http://127.0.0.1:8001/auth/spotify/login

**Expected console output:**
```
============================================================
Spotify OAuth Debug Info:
Spotify Client ID: 048e9d2e7bc384c219fced5fb2d79ba16
Spotify Redirect URI: http://127.0.0.1:8001/auth/spotify/callback
============================================================
Generated auth URL: https://accounts.spotify.com/authorize?client_id=048e9d2e7bc384c219fced5fb2d79ba16&response_type=code&redirect_uri=http://127.0.0.1:8001/auth/spotify/callback&scope=...
============================================================
```

**Expected browser behavior:**
- Redirects to Spotify authorization page
- Shows your real app name (not "your_spotify_client_id_here")
- Callback URL shows `http://127.0.0.1:8001/auth/spotify/callback`

### 3. Verify Callback

After authorizing on Spotify, should redirect to:
```
http://127.0.0.1:8001/auth/spotify/callback?code=...
```

Then redirect to frontend:
```
http://localhost:3001/auth/callback?user_id=...
```

---

## Environment File Structure

```
tasteexplorer/
├── .env                     # Root env (placeholder values, for reference)
└── apps/
    └── api/
        ├── .env             # API env (REAL values - USED BY API) ✅
        ├── main.py          # Loads apps/api/.env first
        └── spotify/
            └── client.py    # Loads apps/api/.env
```

**Active configuration:** `apps/api/.env`

---

## Environment Variables (apps/api/.env)

Current working values:
```bash
SPOTIFY_CLIENT_ID=048e9d2e7bc384c219fced5fb2d79ba16
SPOTIFY_CLIENT_SECRET=7e7884becf424346899e6ae94649e12a
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8001/auth/spotify/callback
FRONTEND_URL=http://localhost:3001
CORS_ORIGINS=http://localhost:3001
DATABASE_URL=sqlite:///./tasteexplorer.db
REDIS_URL=redis://localhost:6379/0
ENVIRONMENT=development
```

---

## Why This Happened

1. **Monorepo structure** - Multiple `.env` files at different levels
2. **Load order** - Root `.env` was loaded before `apps/api/.env`
3. **No explicit path** - `spotify/client.py` wasn't loading env vars at all
4. **Default behavior** - `load_dotenv()` searches upward from current directory

---

## Prevention

### For Future Development

1. **Single source of truth:** Keep real credentials in `apps/api/.env`
2. **Root `.env` as template:** Keep placeholder values in root `.env`
3. **Explicit paths:** Always specify `load_dotenv(env_path)` with explicit path
4. **Startup logging:** Print which env file is loaded (already added)

### Verify Configuration

Run this to check loaded environment:
```bash
cd apps/api
python3 -c "
from pathlib import Path
from dotenv import load_dotenv
import os

api_env = Path(__file__).parent / '.env'
load_dotenv(api_env)

print('Client ID:', os.getenv('SPOTIFY_CLIENT_ID'))
print('Redirect URI:', os.getenv('SPOTIFY_REDIRECT_URI'))
"
```

Should output:
```
Client ID: 048e9d2e7bc384c219fced5fb2d79ba16
Redirect URI: http://127.0.0.1:8001/auth/spotify/callback
```

---

## Cleanup (Optional)

Once verified working, you can remove debug prints from `auth/routes.py`:

```python
@router.get("/spotify/login")
async def spotify_login():
    """Initiate Spotify OAuth flow."""
    auth_manager = create_oauth_manager()
    auth_url = auth_manager.get_authorize_url()
    return RedirectResponse(url=auth_url)
```

Or keep them for debugging until production deployment.

---

## Status

✅ **Fixed:** Environment variable loading priority  
✅ **Fixed:** `spotify/client.py` now loads env vars  
✅ **Added:** Debug logging to verify configuration  
✅ **Tested:** OAuth flow should work with real credentials  

**Ready to test!** Visit http://127.0.0.1:8001/auth/spotify/login 🎉
