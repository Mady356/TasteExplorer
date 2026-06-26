#!/usr/bin/env python3
"""
Test environment variable loading.

Run this to verify Spotify credentials are loaded correctly.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

def test_env_loading():
    """Test environment loading from apps/api/.env"""
    print("=" * 70)
    print("Testing Environment Variable Loading")
    print("=" * 70)
    print()

    # Test 1: Load from apps/api/.env
    env_path = Path(__file__).parent / '.env'
    print(f"1. Loading from: {env_path}")
    print(f"   File exists: {env_path.exists()}")

    if not env_path.exists():
        print("   ❌ ERROR: .env file not found!")
        return False

    load_dotenv(env_path)
    print("   ✓ Loaded successfully")
    print()

    # Test 2: Check Spotify Client ID
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    print(f"2. Spotify Client ID: {client_id}")

    if not client_id:
        print("   ❌ ERROR: SPOTIFY_CLIENT_ID not set!")
        return False
    elif client_id == "your_spotify_client_id_here":
        print("   ❌ ERROR: Still using placeholder value!")
        return False
    else:
        print("   ✓ Real value loaded")
    print()

    # Test 3: Check Redirect URI
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    print(f"3. Spotify Redirect URI: {redirect_uri}")

    if not redirect_uri:
        print("   ❌ ERROR: SPOTIFY_REDIRECT_URI not set!")
        return False
    elif redirect_uri == "http://localhost:8000/auth/spotify/callback":
        print("   ⚠️  WARNING: Using default port 8000 (not 8001)")
    else:
        print("   ✓ Value loaded")
    print()

    # Test 4: Check Client Secret (don't print it)
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    print(f"4. Spotify Client Secret: {'*' * len(client_secret) if client_secret else 'NOT SET'}")

    if not client_secret:
        print("   ❌ ERROR: SPOTIFY_CLIENT_SECRET not set!")
        return False
    elif client_secret == "your_spotify_client_secret_here":
        print("   ❌ ERROR: Still using placeholder value!")
        return False
    else:
        print("   ✓ Real value loaded (hidden)")
    print()

    # Test 5: Other important vars
    print("5. Other Environment Variables:")
    print(f"   FRONTEND_URL: {os.getenv('FRONTEND_URL')}")
    print(f"   CORS_ORIGINS: {os.getenv('CORS_ORIGINS')}")
    print(f"   DATABASE_URL: {os.getenv('DATABASE_URL')}")
    print(f"   ENVIRONMENT: {os.getenv('ENVIRONMENT')}")
    print()

    print("=" * 70)
    print("✅ All environment variables loaded correctly!")
    print("=" * 70)
    print()
    print("Ready to start the server:")
    print("  uvicorn main:app --reload --port 8001")
    print()
    return True


if __name__ == "__main__":
    success = test_env_loading()
    exit(0 if success else 1)
