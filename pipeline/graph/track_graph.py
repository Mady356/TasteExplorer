"""
Track similarity graph construction.

Builds k-nearest-neighbor graph from enriched track records.
"""
from typing import List, Dict, Optional
from .feature_space import (
    extract_feature_matrix,
    zscore_normalize,
    cosine_similarity,
    FEATURE_COLUMNS,
)


def build_track_graph(
    records: List[Dict],
    k: int = 5,
    n_clusters: Optional[int] = None
) -> Dict:
    """
    Build k-NN track similarity graph with optional clustering.

    Creates nodes for each track and directed edges to k most similar tracks.
    Optionally assigns clusters and computes cluster statistics.

    Args:
        records: List of track records with audio features
        k: Number of nearest neighbors per track
        n_clusters: Number of clusters (if None, no clustering)

    Returns:
        Dict with:
            - nodes: List of node dicts (track_id, track_name, artists, cluster_id, etc.)
            - edges: List of edge dicts (source, target, similarity, rank, shared_cluster)
            - clusters: List of cluster stats (if n_clusters provided)
            - metadata: Graph construction metadata
    """
    # Extract features
    track_ids, track_lookup, feature_matrix, usable_records = extract_feature_matrix(records)

    if not track_ids:
        return {
            "nodes": [],
            "edges": [],
            "metadata": {
                "total_input_records": len(records),
                "usable_records": 0,
                "k": k,
                "feature_columns": FEATURE_COLUMNS,
            }
        }

    # Normalize features
    normalized_matrix = zscore_normalize(feature_matrix)

    # Optional clustering
    cluster_assignments = {}
    cluster_stats = []
    if n_clusters is not None and n_clusters > 0:
        try:
            from .clustering import assign_track_clusters
            from .cluster_stats import build_cluster_stats

            cluster_assignments = assign_track_clusters(usable_records, n_clusters=n_clusters)
            cluster_stats = build_cluster_stats(usable_records, cluster_assignments)
        except ImportError:
            # Clustering not available - continue without it
            pass

    # Build nodes
    nodes = []
    for i, track_id in enumerate(track_ids):
        record = track_lookup[track_id]
        cluster_id = cluster_assignments.get(track_id)
        node = _create_node(track_id, record, normalized_matrix[i], cluster_id)
        nodes.append(node)

    # Build edges (k-NN)
    edges = []
    for i, source_track_id in enumerate(track_ids):
        # Compute similarities to all other tracks
        similarities = []
        for j, target_track_id in enumerate(track_ids):
            if i == j:
                continue  # Skip self

            sim = cosine_similarity(normalized_matrix[i], normalized_matrix[j])
            similarities.append((target_track_id, sim))

        # Sort by similarity (descending) and take top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_k = similarities[:k]

        # Create edges
        for rank, (target_track_id, sim) in enumerate(top_k, start=1):
            # Check if source and target share a cluster
            source_cluster = cluster_assignments.get(source_track_id)
            target_cluster = cluster_assignments.get(target_track_id)
            shared_cluster = source_cluster if source_cluster == target_cluster else None

            edge = {
                "source_track_id": source_track_id,
                "target_track_id": target_track_id,
                "similarity": sim,
                "distance_rank": rank,
                "shared_cluster_id": shared_cluster,
            }
            edges.append(edge)

    result = {
        "nodes": nodes,
        "edges": edges,
        "metadata": {
            "total_input_records": len(records),
            "usable_records": len(usable_records),
            "k": k,
            "n_clusters": n_clusters,
            "feature_columns": FEATURE_COLUMNS,
        }
    }

    if cluster_stats:
        result["clusters"] = cluster_stats

    return result


def _create_node(
    track_id: str,
    record: Dict,
    features: List[float],
    cluster_id: Optional[int] = None
) -> Dict:
    """
    Create node dict from track record.

    Args:
        track_id: Track ID
        record: Track record
        features: Normalized feature vector
        cluster_id: Optional cluster assignment

    Returns:
        Node dict
    """
    # Extract track name
    track_name = record.get("track_name") or record.get("name", "Unknown Track")

    # Extract artists
    artists = []
    if "artists" in record:
        artists_data = record["artists"]
        if isinstance(artists_data, list):
            for artist in artists_data:
                if isinstance(artist, dict):
                    artists.append(artist.get("artist_name") or artist.get("name", "Unknown"))
                elif isinstance(artist, str):
                    artists.append(artist)
        elif isinstance(artists_data, str):
            artists = [artists_data]

    # Extract metadata
    time_range = record.get("time_range")
    track_rank = record.get("rank")

    node = {
        "track_id": track_id,
        "track_name": track_name,
        "artists": artists,
        "time_range": time_range,
        "track_rank": track_rank,
        "features": features,
    }

    if cluster_id is not None:
        node["cluster_id"] = cluster_id

    return node
