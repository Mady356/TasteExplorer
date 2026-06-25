"""
Layer 1 & 2: Track and Cluster Graphs

Layer 1: Pure Python k-NN similarity graphs from enriched track records.
Layer 2: Cluster-level taste map showing relationships between taste regions.

Main entry points:
    build_track_graph(records, k=5, n_clusters=4)  # Layer 1
    build_cluster_graph(layer1_graph)               # Layer 2

Returns graph objects with nodes, edges, and metadata.
"""
from .track_graph import build_track_graph
from .cluster_graph import build_cluster_graph
from .feature_space import (
    FEATURE_COLUMNS,
    extract_feature_matrix,
    zscore_normalize,
    cosine_similarity,
)
from .clustering import assign_track_clusters
from .cluster_stats import build_cluster_stats

__all__ = [
    "build_track_graph",
    "build_cluster_graph",
    "FEATURE_COLUMNS",
    "extract_feature_matrix",
    "zscore_normalize",
    "cosine_similarity",
    "assign_track_clusters",
    "build_cluster_stats",
]
