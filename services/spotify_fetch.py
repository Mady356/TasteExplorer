def fetch_top_tracks(sp, time_range: str, limit: int = 50):
    """
    Fetch the current user's top tracks for a given time range.
    Args:
        sp: spotipy.Spotify client (already authenticated)
        time_range: one of {"short_term", "medium_term", "long_term"}
        limit: number of tracks to fetch (1..50)
    Returns:
        List[dict]: raw Spotify track objects (the items in the response)
    """
    allowed = {"short_term", "medium_term", "long_term"}
    if time_range not in allowed:
        raise ValueError(f"time_range must be one of {sorted(allowed)}, got: {time_range}")
    if not (1 <= limit <= 50):
        raise ValueError(f"limit must be between 1 and 50, got: {limit}")
    resp = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    return resp["items"]

def fetch_audio_features(sp, track_ids: List[str]):
    """
    Fetch audio features for a list of track IDs.
    """
    resp = sp.audio_features(track_ids)
    return resp 