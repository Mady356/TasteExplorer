"""
Candidate track scoring against taste clusters.

Scores candidate tracks based on similarity to clusters and novelty.
"""
from typing import Dict, List, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.feature_space import cosine_similarity, FEATURE_COLUMNS


def score_candidate_track(
    candidate_track: Dict,
    cluster_node: Dict,
    similarity_weight: float = 0.75,
    novelty_weight: float = 0.25
) -> Optional[Dict]:
    """
    Score a candidate track against a cluster.

    Combines similarity (how well it matches the cluster's taste) and
    novelty (how undiscovered/niche it is).

    Args:
        candidate_track: Normalized candidate track dict
        cluster_node: Cluster node from Layer 2
        similarity_weight: Weight for similarity score (default: 0.75)
        novelty_weight: Weight for novelty score (default: 0.25)

    Returns:
        Scored track dict with similarity, novelty, and final scores,
        or None if candidate lacks required features
    """
    # Extract candidate features
    candidate_features = _extract_candidate_features(candidate_track)
    if candidate_features is None:
        return None

    # Get cluster centroid
    cluster_centroid = cluster_node["centroid_vector"]

    # Compute similarity
    similarity_score = cosine_similarity(candidate_features, cluster_centroid)

    # Normalize similarity from [-1, 1] to [0, 1]
    similarity_score = (similarity_score + 1) / 2

    # Compute novelty (inverse of normalized popularity)
    popularity = candidate_track.get("track_popularity", 50)
    novelty_score = 1.0 - (popularity / 100.0)

    # Compute final score
    final_score = (
        similarity_weight * similarity_score +
        novelty_weight * novelty_score
    )

    return {
        "track_id": candidate_track["track_id"],
        "track_name": candidate_track["track_name"],
        "artist_id": candidate_track.get("artist_id"),
        "artist_name": candidate_track.get("artist_name", "Unknown Artist"),
        "matched_cluster_id": cluster_node["cluster_id"],
        "similarity_score": similarity_score,
        "novelty_score": novelty_score,
        "final_score": final_score,
        "track_popularity": popularity,
    }


def score_candidates_against_clusters(
    candidate_tracks: List[Dict],
    cluster_nodes: List[Dict],
    similarity_weight: float = 0.75,
    novelty_weight: float = 0.25
) -> List[Dict]:
    """
    Score all candidate tracks against all clusters.

    For each candidate, finds the best matching cluster and assigns that score.

    Args:
        candidate_tracks: List of normalized candidate tracks
        cluster_nodes: List of cluster nodes from Layer 2
        similarity_weight: Weight for similarity score
        novelty_weight: Weight for novelty score

    Returns:
        List of scored tracks sorted by final_score (descending)
    """
    if not cluster_nodes:
        return []

    scored_tracks = []

    for candidate in candidate_tracks:
        # Score against all clusters
        cluster_scores = []
        for cluster in cluster_nodes:
            scored = score_candidate_track(
                candidate,
                cluster,
                similarity_weight,
                novelty_weight
            )
            if scored:
                cluster_scores.append(scored)

        # Take best cluster match
        if cluster_scores:
            best_match = max(cluster_scores, key=lambda s: s["final_score"])
            scored_tracks.append(best_match)

    # Sort by final score (descending)
    scored_tracks.sort(key=lambda s: s["final_score"], reverse=True)

    return scored_tracks


def _extract_candidate_features(candidate_track: Dict) -> Optional[List[float]]:
    """
    Extract feature vector from candidate track.

    Args:
        candidate_track: Normalized candidate track

    Returns:
        Feature vector matching FEATURE_COLUMNS order, or None if incomplete
    """
    audio_features = candidate_track.get("audio_features", {})

    features = []
    for col in FEATURE_COLUMNS:
        value = audio_features.get(col)

        if value is None:
            return None  # Missing required feature

        # Normalize tempo
        if col == "tempo":
            value = (value - 40) / 160
            value = max(0.0, min(1.0, value))

        features.append(float(value))

    return features


def filter_known_tracks(
    candidate_tracks: List[Dict],
    known_track_ids: set
) -> List[Dict]:
    """
    Filter out tracks that are already in the user's library.

    Args:
        candidate_tracks: List of candidate tracks
        known_track_ids: Set of track IDs in user's library

    Returns:
        List of candidate tracks excluding known ones
    """
    return [
        track for track in candidate_tracks
        if track.get("track_id") not in known_track_ids
    ]


def filter_known_artists(
    candidate_tracks: List[Dict],
    known_artist_ids: set
) -> List[Dict]:
    """
    Filter out tracks by artists already in the user's library.

    Args:
        candidate_tracks: List of candidate tracks
        known_artist_ids: Set of artist IDs in user's library

    Returns:
        List of candidate tracks excluding known artists
    """
    return [
        track for track in candidate_tracks
        if track.get("artist_id") not in known_artist_ids
    ]
