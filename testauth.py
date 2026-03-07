import os
from pathlib import Path

# pyright: reportMissingImports=false

import spotipy
from spotipy.oauth2 import SpotifyOAuth


def load_env_file(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        if key:
            os.environ.setdefault(key.strip(), value.strip())


load_env_file()

SCOPE = "user-top-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope=SCOPE,
))

me = sp.current_user()
print("Logged in as:", me["display_name"], "|", me["id"])
top = sp.current_user_top_tracks(limit=10, time_range="medium_term")
print("\nTop tracks (medium_term):")
for i, t in enumerate(top["items"], start=1):
    print(f"{i:02d}. {t['name']} — {t['artists'][0]['name']}")
