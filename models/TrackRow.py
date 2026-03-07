from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class TrackRow:
    track_name: str
    artists: List[Dict]
    album_name: str
    track_id: str
    track_popularity: int
    track_duration_ms: int
    track_explicit: bool
    track_preview_url: str
    track_album_image_url: str
    track_album_release_date: str
    track_rank: int

def fetch_top_tracks(sp, time_range:str, limit:int=50):
    """
    Fetch the current user's top tracks for a given time range.
    Args:
        sp: spotipy.Spotify client (already authenticated)
        time_range: one of {"short_term", "medium_term", "long_term"}
        limit: number of tracks to fetch (1..50)
    Returns:
        [dict]: raw Spotify track objects (the items in the response)
    """
    allowed = {"short_term", "medium_term", "long_term"}
    if time_range not in allowed:
        raise ValueError(f"time_range must be one of {sorted(allowed)}, got: {time_range}")
    if not (1 <= limit <= 50):
        raise ValueError(f"limit must be between 1 and 50, got: {limit}")
    resp = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    return resp["items"]

def normalize_track(raw_track, time_range: str, rank: int, pulled_at: str) -> TrackRow:
    """
    Convert a raw Spotify track object into a TrackRow.
    """

    # Extract album information
    album = raw_track["album"]
    album_name = album["name"]
    album_release_date = album["release_date"]

    # Build artists list
    artists_list = []
    for artist in raw_track["artists"]:
        artists_list.append({
            "artist_id": artist["id"],
            "artist_name": artist["name"],
            "influence": None   # will compute later
        })

    # Create TrackRow
    row = TrackRow(
        track_id=raw_track["id"],
        track_name=raw_track["name"],
        track_popularity=raw_track["popularity"],
        track_album_name=album_name,
        track_album_release_date=album_release_date,
        time_range=time_range,
        track_rank=rank,
        pulled_at=pulled_at,
        artists=artists_list
    )

    return row

if __name__ == "__main__":
    print("success")


        # Create TrackRow


    

        

