"""
Candidate track and artist data models.

Simple data structures for representing recommendation candidates.
"""
from typing import List, Dict, Optional


def normalize_candidate_track(raw_track: Dict) -> Optional[Dict]:
    """
    Normalize a candidate track into standard format.

    Extracts required fields and ensures consistent structure.

    Args:
        raw_track: Raw track dict (from Spotify or other source)

    Returns:
        Normalized candidate track dict, or None if missing required fields
    """
    track_id = raw_track.get("track_id") or raw_track.get("id")
    if not track_id:
        return None

    track_name = raw_track.get("track_name") or raw_track.get("name", "Unknown Track")

    # Extract artist info
    artists = []
    artist_id = None
    artist_name = None

    if "artists" in raw_track:
        artists_data = raw_track["artists"]
        if isinstance(artists_data, list) and len(artists_data) > 0:
            # Take first artist as primary
            first_artist = artists_data[0]
            if isinstance(first_artist, dict):
                artist_id = first_artist.get("artist_id") or first_artist.get("id")
                artist_name = first_artist.get("artist_name") or first_artist.get("name")
                artists = [
                    a.get("artist_name") or a.get("name", "Unknown")
                    for a in artists_data
                    if isinstance(a, dict)
                ]

    # Popularity (default to 50 if missing)
    track_popularity = raw_track.get("track_popularity") or raw_track.get("popularity", 50)

    # Audio features (flat or nested)
    features = {}
    if "audio_features" in raw_track and isinstance(raw_track["audio_features"], dict):
        features = raw_track["audio_features"]
    else:
        # Assume flat format
        feature_keys = [
            "danceability", "energy", "valence", "acousticness",
            "instrumentalness", "liveness", "speechiness", "tempo"
        ]
        for key in feature_keys:
            if key in raw_track:
                features[key] = raw_track[key]

    return {
        "track_id": track_id,
        "track_name": track_name,
        "artists": artists,
        "artist_id": artist_id,
        "artist_name": artist_name or (artists[0] if artists else "Unknown Artist"),
        "track_popularity": track_popularity,
        "audio_features": features,
    }


def create_artist_summary(artist_id: str, artist_name: str, tracks: List[Dict]) -> Dict:
    """
    Create artist summary from scored tracks.

    Args:
        artist_id: Artist ID
        artist_name: Artist name
        tracks: List of scored track dicts

    Returns:
        Artist summary dict
    """
    if not tracks:
        return {
            "artist_id": artist_id,
            "artist_name": artist_name,
            "artist_score": 0.0,
            "best_tracks": [],
            "matched_clusters": [],
            "track_count": 0,
        }

    # Sort tracks by score
    sorted_tracks = sorted(tracks, key=lambda t: t.get("final_score", 0), reverse=True)

    # Get matched clusters
    matched_clusters = list(set(
        t.get("matched_cluster_id")
        for t in tracks
        if t.get("matched_cluster_id") is not None
    ))

    return {
        "artist_id": artist_id,
        "artist_name": artist_name,
        "artist_score": sum(t.get("final_score", 0) for t in sorted_tracks) / len(sorted_tracks),
        "best_tracks": sorted_tracks,
        "matched_clusters": matched_clusters,
        "track_count": len(tracks),
    }
