"""
Layer 2: Cluster-Level Taste Map

Converts Layer 1 track-level graph into a higher-level cluster graph.
Clusters represent major taste regions in the user's music profile.
"""
from typing import List, Dict
from .feature_space import cosine_similarity, FEATURE_COLUMNS


def build_cluster_graph(
    layer1_graph: Dict,
    centroid_similarity_threshold: float = 0.3,
) -> Dict:
    """
    Build cluster-level taste map from Layer 1 graph.

    Creates a higher-level graph where nodes are taste clusters and edges
    represent relationships between clusters (centroid similarity or shared artists).

    Args:
        layer1_graph: Output from build_track_graph (Layer 1)
        centroid_similarity_threshold: Minimum similarity to create edge (default: 0.3)

    Returns:
        Dict with:
            - cluster_nodes: List of cluster node dicts
            - cluster_edges: List of cluster edge dicts
            - metadata: Construction metadata
    """
    if "clusters" not in layer1_graph or not layer1_graph["clusters"]:
        return {
            "cluster_nodes": [],
            "cluster_edges": [],
            "metadata": {
                "error": "No clusters in Layer 1 graph. Run build_track_graph with n_clusters > 0."
            }
        }

    clusters = layer1_graph["clusters"]
    nodes_by_cluster = _group_nodes_by_cluster(layer1_graph["nodes"])

    # Build cluster nodes
    cluster_nodes = []
    for cluster in clusters:
        cluster_id = cluster["cluster_id"]
        cluster_node = _build_cluster_node(cluster, nodes_by_cluster.get(cluster_id, []))
        cluster_nodes.append(cluster_node)

    # Build cluster edges
    cluster_edges = _build_cluster_edges(
        cluster_nodes,
        nodes_by_cluster,
        centroid_similarity_threshold
    )

    return {
        "cluster_nodes": cluster_nodes,
        "cluster_edges": cluster_edges,
        "metadata": {
            "num_clusters": len(cluster_nodes),
            "num_cluster_edges": len(cluster_edges),
            "centroid_similarity_threshold": centroid_similarity_threshold,
        }
    }


def _group_nodes_by_cluster(nodes: List[Dict]) -> Dict[int, List[Dict]]:
    """
    Group track nodes by cluster_id.

    Args:
        nodes: List of track nodes from Layer 1

    Returns:
        Dict mapping cluster_id to list of nodes
    """
    groups = {}
    for node in nodes:
        cluster_id = node.get("cluster_id")
        if cluster_id is not None:
            if cluster_id not in groups:
                groups[cluster_id] = []
            groups[cluster_id].append(node)
    return groups


def _build_cluster_node(cluster: Dict, nodes: List[Dict]) -> Dict:
    """
    Build a cluster node with metadata and suggested label.

    Args:
        cluster: Cluster stats from Layer 1
        nodes: Track nodes in this cluster

    Returns:
        Cluster node dict
    """
    cluster_id = cluster["cluster_id"]
    centroid = cluster["centroid_vector"]

    # Generate suggested label based on centroid features
    suggested_label = _generate_cluster_label(centroid)

    cluster_node = {
        "cluster_id": cluster_id,
        "track_count": cluster["track_count"],
        "centroid_vector": centroid,
        "representative_tracks": cluster["representative_tracks"],
        "top_artists": cluster["top_artists"],
        "coherence_score": cluster["coherence_score"],
        "suggested_label": suggested_label,
    }

    return cluster_node


def _generate_cluster_label(centroid: List[float]) -> str:
    """
    Generate simple rule-based label for a cluster.

    Based on normalized feature values in the centroid.

    Args:
        centroid: Normalized feature vector

    Returns:
        Human-readable label string
    """
    if len(centroid) != len(FEATURE_COLUMNS):
        return "unknown"

    # Map features to values
    features = {
        col: centroid[i]
        for i, col in enumerate(FEATURE_COLUMNS)
    }

    # Simple rule-based labeling
    # Note: centroid values are z-score normalized, so:
    # > 0.5 = high, < -0.5 = low

    energy = features["energy"]
    valence = features["valence"]
    acousticness = features["acousticness"]
    instrumentalness = features["instrumentalness"]
    danceability = features["danceability"]
    speechiness = features["speechiness"]

    # High instrumental
    if instrumentalness > 0.5:
        if energy > 0.5:
            return "energetic instrumental"
        else:
            return "ambient / instrumental"

    # High speechiness (podcasts, spoken word, rap)
    if speechiness > 0.5:
        return "speech-heavy / rap"

    # Acoustic
    if acousticness > 0.5:
        if valence > 0.5:
            return "bright acoustic"
        else:
            return "melancholic acoustic"

    # Energetic
    if energy > 0.5:
        if valence > 0.5:
            if danceability > 0.5:
                return "upbeat dance"
            else:
                return "bright energetic"
        else:
            if danceability > 0.5:
                return "dark dance"
            else:
                return "intense / powerful"

    # Low energy
    if energy < -0.5:
        if valence > 0.5:
            return "calm uplifting"
        else:
            return "melancholic / downtempo"

    # High valence (happy)
    if valence > 0.5:
        return "uplifting / positive"

    # Low valence (sad)
    if valence < -0.5:
        return "melancholic / introspective"

    # Default
    return "balanced / eclectic"


def _build_cluster_edges(
    cluster_nodes: List[Dict],
    nodes_by_cluster: Dict[int, List[Dict]],
    similarity_threshold: float
) -> List[Dict]:
    """
    Build edges between clusters.

    Edges are created if:
    1. Centroid similarity exceeds threshold, OR
    2. Clusters share artists

    Args:
        cluster_nodes: List of cluster nodes
        nodes_by_cluster: Track nodes grouped by cluster
        similarity_threshold: Minimum centroid similarity

    Returns:
        List of cluster edge dicts
    """
    edges = []

    for i, source_cluster in enumerate(cluster_nodes):
        source_id = source_cluster["cluster_id"]
        source_centroid = source_cluster["centroid_vector"]
        source_artists = _extract_artists_from_nodes(nodes_by_cluster.get(source_id, []))

        for j, target_cluster in enumerate(cluster_nodes):
            if i >= j:  # Skip self and avoid duplicates
                continue

            target_id = target_cluster["cluster_id"]
            target_centroid = target_cluster["centroid_vector"]
            target_artists = _extract_artists_from_nodes(nodes_by_cluster.get(target_id, []))

            # Compute centroid similarity
            centroid_sim = cosine_similarity(source_centroid, target_centroid)

            # Compute shared artists
            shared_artists = source_artists.intersection(target_artists)
            shared_artist_count = len(shared_artists)

            # Create edge if criteria met
            if centroid_sim >= similarity_threshold or shared_artist_count > 0:
                edge_type = _determine_edge_type(centroid_sim, shared_artist_count, similarity_threshold)

                edge = {
                    "source_cluster_id": source_id,
                    "target_cluster_id": target_id,
                    "centroid_similarity": centroid_sim,
                    "shared_artist_count": shared_artist_count,
                    "edge_type": edge_type,
                }
                edges.append(edge)

    return edges


def _extract_artists_from_nodes(nodes: List[Dict]) -> set:
    """
    Extract unique artist names from track nodes.

    Args:
        nodes: List of track nodes

    Returns:
        Set of artist names
    """
    artists = set()
    for node in nodes:
        if "artists" in node:
            for artist in node["artists"]:
                if isinstance(artist, dict):
                    name = artist.get("artist_name") or artist.get("name")
                    if name:
                        artists.add(name)
                elif isinstance(artist, str):
                    artists.add(artist)
    return artists


def _determine_edge_type(
    centroid_sim: float,
    shared_artist_count: int,
    threshold: float
) -> str:
    """
    Determine edge type based on connection reason.

    Args:
        centroid_sim: Cosine similarity between centroids
        shared_artist_count: Number of shared artists
        threshold: Similarity threshold

    Returns:
        Edge type string
    """
    if centroid_sim >= threshold and shared_artist_count > 0:
        return "strong"  # Both criteria met
    elif shared_artist_count > 0:
        return "artist_bridge"  # Shared artists only
    else:
        return "feature_similar"  # Centroid similarity only
