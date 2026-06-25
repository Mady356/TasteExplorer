"""
Layer 3: Discovery Graph

Scores candidate tracks/artists against Layer 2 clusters and builds
a discovery graph for recommendations.
"""
from typing import List, Dict, Optional, Set
from .candidate_models import normalize_candidate_track
from .candidate_scoring import (
    score_candidates_against_clusters,
    filter_known_tracks,
    filter_known_artists,
)
from .artist_ranking import rank_candidate_artists, get_top_tracks_overall
from .explanations import generate_explanation


def build_discovery_graph(
    layer2_graph: Dict,
    candidate_tracks: List[Dict],
    known_track_ids: Optional[Set[str]] = None,
    known_artist_ids: Optional[Set[str]] = None,
    similarity_weight: float = 0.75,
    novelty_weight: float = 0.25,
    top_n_tracks: int = 50,
    top_n_artists: int = 20,
) -> Dict:
    """
    Build discovery graph from Layer 2 clusters and candidate tracks.

    Filters known tracks/artists, scores candidates, ranks artists,
    and creates a graph structure for recommendations.

    Args:
        layer2_graph: Output from build_cluster_graph (Layer 2)
        candidate_tracks: List of candidate track dicts (raw or normalized)
        known_track_ids: Set of track IDs already in user's library
        known_artist_ids: Set of artist IDs already in user's library
        similarity_weight: Weight for similarity score (default: 0.75)
        novelty_weight: Weight for novelty score (default: 0.25)
        top_n_tracks: Number of top tracks to include (default: 50)
        top_n_artists: Number of top artists to include (default: 20)

    Returns:
        Dict with:
            - candidate_track_nodes: Scored candidate tracks
            - candidate_artist_nodes: Ranked artists
            - discovery_edges: Edges linking candidates to clusters
            - ranked_artists: Top artists sorted by score
            - ranked_tracks: Top tracks sorted by score
            - metadata: Discovery graph metadata
    """
    cluster_nodes = layer2_graph.get("cluster_nodes", [])

    if not cluster_nodes:
        return {
            "candidate_track_nodes": [],
            "candidate_artist_nodes": [],
            "discovery_edges": [],
            "ranked_artists": [],
            "ranked_tracks": [],
            "metadata": {
                "error": "No clusters in Layer 2 graph."
            }
        }

    # Normalize candidate tracks
    normalized_candidates = []
    for track in candidate_tracks:
        normalized = normalize_candidate_track(track)
        if normalized:
            normalized_candidates.append(normalized)

    # Filter known tracks/artists
    if known_track_ids:
        normalized_candidates = filter_known_tracks(normalized_candidates, known_track_ids)

    if known_artist_ids:
        normalized_candidates = filter_known_artists(normalized_candidates, known_artist_ids)

    if not normalized_candidates:
        return {
            "candidate_track_nodes": [],
            "candidate_artist_nodes": [],
            "discovery_edges": [],
            "ranked_artists": [],
            "ranked_tracks": [],
            "metadata": {
                "total_candidates": len(candidate_tracks),
                "after_normalization": 0,
                "after_filtering": 0,
            }
        }

    # Score candidates against clusters
    scored_tracks = score_candidates_against_clusters(
        normalized_candidates,
        cluster_nodes,
        similarity_weight,
        novelty_weight
    )

    # Rank artists
    ranked_artists = rank_candidate_artists(scored_tracks, top_tracks_per_artist=3)

    # Get top tracks
    top_tracks = get_top_tracks_overall(scored_tracks, top_n=top_n_tracks)

    # Build nodes and edges
    candidate_track_nodes = _build_track_nodes(top_tracks, cluster_nodes)
    candidate_artist_nodes = _build_artist_nodes(ranked_artists[:top_n_artists])
    discovery_edges = _build_discovery_edges(top_tracks, ranked_artists[:top_n_artists])

    return {
        "candidate_track_nodes": candidate_track_nodes,
        "candidate_artist_nodes": candidate_artist_nodes,
        "discovery_edges": discovery_edges,
        "ranked_artists": ranked_artists[:top_n_artists],
        "ranked_tracks": top_tracks,
        "metadata": {
            "total_candidates": len(candidate_tracks),
            "after_normalization": len(normalized_candidates),
            "after_filtering": len(normalized_candidates),
            "scored_tracks": len(scored_tracks),
            "top_artists": len(ranked_artists[:top_n_artists]),
            "top_tracks": len(top_tracks),
            "similarity_weight": similarity_weight,
            "novelty_weight": novelty_weight,
        }
    }


def _build_track_nodes(scored_tracks: List[Dict], cluster_nodes: List[Dict]) -> List[Dict]:
    """
    Build track nodes with metadata.

    Args:
        scored_tracks: List of scored tracks
        cluster_nodes: Cluster nodes from Layer 2

    Returns:
        List of track node dicts
    """
    cluster_lookup = {c["cluster_id"]: c for c in cluster_nodes}

    track_nodes = []
    for track in scored_tracks:
        cluster_id = track.get("matched_cluster_id")
        cluster = cluster_lookup.get(cluster_id, {})

        # Generate explanation
        explanation = generate_explanation(track, cluster)

        track_node = {
            "track_id": track["track_id"],
            "track_name": track["track_name"],
            "artist_id": track.get("artist_id"),
            "artist_name": track["artist_name"],
            "matched_cluster_id": cluster_id,
            "similarity_score": track["similarity_score"],
            "novelty_score": track["novelty_score"],
            "final_score": track["final_score"],
            "track_popularity": track.get("track_popularity"),
            "explanation": explanation,
        }
        track_nodes.append(track_node)

    return track_nodes


def _build_artist_nodes(ranked_artists: List[Dict]) -> List[Dict]:
    """
    Build artist nodes with metadata.

    Args:
        ranked_artists: List of ranked artist dicts

    Returns:
        List of artist node dicts
    """
    artist_nodes = []

    for artist in ranked_artists:
        artist_node = {
            "artist_id": artist.get("artist_id"),
            "artist_name": artist["artist_name"],
            "artist_score": artist["artist_score"],
            "track_count": artist["track_count"],
            "matched_clusters": artist.get("matched_clusters", []),
            "best_track_ids": [t["track_id"] for t in artist["best_tracks"]],
        }
        artist_nodes.append(artist_node)

    return artist_nodes


def _build_discovery_edges(
    scored_tracks: List[Dict],
    ranked_artists: List[Dict]
) -> List[Dict]:
    """
    Build discovery edges.

    Creates edges:
    - candidate_track -> matched_cluster
    - candidate_artist -> candidate_track

    Args:
        scored_tracks: List of scored tracks
        ranked_artists: List of ranked artists

    Returns:
        List of edge dicts
    """
    edges = []

    # Track -> Cluster edges
    for track in scored_tracks:
        edges.append({
            "edge_type": "track_to_cluster",
            "source_id": track["track_id"],
            "target_id": track.get("matched_cluster_id"),
            "score": track["final_score"],
            "reason": f"similarity={track['similarity_score']:.2f}, novelty={track['novelty_score']:.2f}",
        })

    # Artist -> Track edges
    for artist in ranked_artists:
        for track in artist["best_tracks"]:
            edges.append({
                "edge_type": "artist_to_track",
                "source_id": artist.get("artist_id") or artist["artist_name"],
                "target_id": track["track_id"],
                "score": track["final_score"],
                "reason": f"best track for {artist['artist_name']}",
            })

    return edges
