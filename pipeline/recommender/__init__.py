"""
Layer 3: Discovery / Recommendation Graph

Scores candidate tracks and artists against Layer 2 taste clusters.
Produces ranked recommendations with explanations.

Main entry point:
    build_discovery_graph(layer2_graph, candidate_tracks, known_track_ids, known_artist_ids)

Returns discovery graph with:
    - candidate_track_nodes: Scored candidate tracks
    - candidate_artist_nodes: Ranked artists
    - discovery_edges: Edges linking candidates to clusters
    - ranked_artists: Top artists by score
    - ranked_tracks: Top tracks by score
    - metadata: Discovery metadata
"""
from .discovery_graph import build_discovery_graph
from .candidate_models import normalize_candidate_track, create_artist_summary
from .candidate_scoring import (
    score_candidate_track,
    score_candidates_against_clusters,
    filter_known_tracks,
    filter_known_artists,
)
from .artist_ranking import (
    rank_candidate_artists,
    get_top_tracks_overall,
    get_top_tracks_per_cluster,
    get_diverse_recommendations,
)
from .explanations import (
    generate_explanation,
    generate_artist_explanation,
    generate_cluster_specific_explanation,
)

__all__ = [
    "build_discovery_graph",
    "normalize_candidate_track",
    "create_artist_summary",
    "score_candidate_track",
    "score_candidates_against_clusters",
    "filter_known_tracks",
    "filter_known_artists",
    "rank_candidate_artists",
    "get_top_tracks_overall",
    "get_top_tracks_per_cluster",
    "get_diverse_recommendations",
    "generate_explanation",
    "generate_artist_explanation",
    "generate_cluster_specific_explanation",
]
