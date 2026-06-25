"""
Artist ranking from scored candidate tracks.

Groups tracks by artist and computes artist-level scores.
"""
from typing import List, Dict
from collections import defaultdict


def rank_candidate_artists(
    scored_tracks: List[Dict],
    top_tracks_per_artist: int = 3
) -> List[Dict]:
    """
    Rank candidate artists based on their best tracks.

    Artist score = average of top N track final_scores.

    Args:
        scored_tracks: List of scored candidate tracks
        top_tracks_per_artist: Number of top tracks to average (default: 3)

    Returns:
        List of artist dicts sorted by artist_score (descending)
    """
    # Group tracks by artist
    tracks_by_artist = defaultdict(list)

    for track in scored_tracks:
        artist_id = track.get("artist_id")
        artist_name = track.get("artist_name", "Unknown Artist")

        # Use artist_name as fallback key if no ID
        artist_key = artist_id if artist_id else artist_name

        tracks_by_artist[artist_key].append(track)

    # Compute artist scores
    ranked_artists = []

    for artist_key, tracks in tracks_by_artist.items():
        # Sort tracks by final_score (descending)
        sorted_tracks = sorted(tracks, key=lambda t: t["final_score"], reverse=True)

        # Take top N tracks
        top_tracks = sorted_tracks[:top_tracks_per_artist]

        # Compute artist score (average of top tracks)
        artist_score = sum(t["final_score"] for t in top_tracks) / len(top_tracks)

        # Extract artist info from first track
        first_track = tracks[0]
        artist_id = first_track.get("artist_id")
        artist_name = first_track.get("artist_name", "Unknown Artist")

        # Get matched clusters (unique)
        matched_clusters = list(set(
            t["matched_cluster_id"]
            for t in tracks
            if "matched_cluster_id" in t
        ))

        ranked_artists.append({
            "artist_id": artist_id,
            "artist_name": artist_name,
            "artist_score": artist_score,
            "best_tracks": top_tracks,
            "all_tracks": sorted_tracks,
            "matched_clusters": matched_clusters,
            "track_count": len(tracks),
        })

    # Sort by artist_score (descending)
    ranked_artists.sort(key=lambda a: a["artist_score"], reverse=True)

    return ranked_artists


def get_top_tracks_overall(
    scored_tracks: List[Dict],
    top_n: int = 20
) -> List[Dict]:
    """
    Get top N tracks overall (not grouped by artist).

    Args:
        scored_tracks: List of scored candidate tracks
        top_n: Number of top tracks to return

    Returns:
        List of top tracks sorted by final_score
    """
    # Already sorted by score in score_candidates_against_clusters
    return scored_tracks[:top_n]


def get_top_tracks_per_cluster(
    scored_tracks: List[Dict],
    top_n_per_cluster: int = 5
) -> Dict[int, List[Dict]]:
    """
    Get top N tracks for each cluster.

    Useful for cluster-specific recommendations.

    Args:
        scored_tracks: List of scored candidate tracks
        top_n_per_cluster: Number of top tracks per cluster

    Returns:
        Dict mapping cluster_id to list of top tracks
    """
    tracks_by_cluster = defaultdict(list)

    for track in scored_tracks:
        cluster_id = track.get("matched_cluster_id")
        if cluster_id is not None:
            tracks_by_cluster[cluster_id].append(track)

    # Get top N per cluster
    top_per_cluster = {}
    for cluster_id, tracks in tracks_by_cluster.items():
        sorted_tracks = sorted(tracks, key=lambda t: t["final_score"], reverse=True)
        top_per_cluster[cluster_id] = sorted_tracks[:top_n_per_cluster]

    return top_per_cluster


def get_diverse_recommendations(
    ranked_artists: List[Dict],
    top_artists: int = 5,
    tracks_per_artist: int = 2
) -> List[Dict]:
    """
    Get diverse recommendations by selecting tracks from multiple artists.

    Args:
        ranked_artists: List of ranked artist dicts
        top_artists: Number of top artists to include
        tracks_per_artist: Tracks per artist

    Returns:
        List of diverse track recommendations
    """
    diverse_tracks = []

    for artist in ranked_artists[:top_artists]:
        best_tracks = artist["best_tracks"][:tracks_per_artist]
        diverse_tracks.extend(best_tracks)

    return diverse_tracks
