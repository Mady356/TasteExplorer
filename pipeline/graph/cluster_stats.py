"""
Cluster statistics and analysis.

Computes centroids, coherence, and representative tracks for each cluster.
"""
from typing import List, Dict
from collections import Counter
from .feature_space import extract_feature_matrix, zscore_normalize, cosine_similarity


def build_cluster_stats(
    records: List[Dict],
    cluster_assignments: Dict[str, int]
) -> List[Dict]:
    """
    Compute statistics for each cluster.

    Args:
        records: List of track records with audio features
        cluster_assignments: Dict mapping track_id to cluster_id

    Returns:
        List of cluster stat dicts, one per cluster
    """
    # Extract features
    track_ids, track_lookup, feature_matrix, usable_records = extract_feature_matrix(records)
    normalized_matrix = zscore_normalize(feature_matrix)

    # Group tracks by cluster
    clusters = {}
    for i, track_id in enumerate(track_ids):
        if track_id not in cluster_assignments:
            continue

        cluster_id = cluster_assignments[track_id]

        if cluster_id not in clusters:
            clusters[cluster_id] = {
                "track_ids": [],
                "track_indices": [],
                "records": [],
            }

        clusters[cluster_id]["track_ids"].append(track_id)
        clusters[cluster_id]["track_indices"].append(i)
        clusters[cluster_id]["records"].append(track_lookup[track_id])

    # Compute stats for each cluster
    cluster_stats = []

    for cluster_id in sorted(clusters.keys()):
        cluster_data = clusters[cluster_id]
        indices = cluster_data["track_indices"]
        track_ids_in_cluster = cluster_data["track_ids"]
        records_in_cluster = cluster_data["records"]

        # Compute centroid
        centroid = _compute_centroid(normalized_matrix, indices)

        # Find representative tracks (closest to centroid)
        representative_tracks = _find_representative_tracks(
            normalized_matrix,
            indices,
            track_ids_in_cluster,
            track_lookup,
            centroid,
            top_n=3
        )

        # Find top artists
        top_artists = _find_top_artists(records_in_cluster, top_n=5)

        # Compute coherence (average similarity to centroid)
        coherence_score = _compute_coherence(normalized_matrix, indices, centroid)

        cluster_stats.append({
            "cluster_id": cluster_id,
            "track_count": len(track_ids_in_cluster),
            "centroid_vector": centroid,
            "representative_tracks": representative_tracks,
            "top_artists": top_artists,
            "coherence_score": coherence_score,
        })

    return cluster_stats


def _compute_centroid(matrix: List[List[float]], indices: List[int]) -> List[float]:
    """
    Compute centroid (mean) of feature vectors.

    Args:
        matrix: Normalized feature matrix
        indices: Indices of tracks in this cluster

    Returns:
        Centroid vector
    """
    if not indices:
        return []

    n_features = len(matrix[0])
    centroid = [0.0] * n_features

    for idx in indices:
        for j in range(n_features):
            centroid[j] += matrix[idx][j]

    for j in range(n_features):
        centroid[j] /= len(indices)

    return centroid


def _find_representative_tracks(
    matrix: List[List[float]],
    indices: List[int],
    track_ids: List[str],
    track_lookup: Dict[str, Dict],
    centroid: List[float],
    top_n: int
) -> List[Dict]:
    """
    Find tracks closest to centroid.

    Args:
        matrix: Normalized feature matrix
        indices: Indices of tracks in cluster
        track_ids: Track IDs in cluster
        track_lookup: Mapping of track_id to record
        centroid: Cluster centroid vector
        top_n: Number of representative tracks to return

    Returns:
        List of representative track dicts with track_id, track_name, similarity
    """
    similarities = []

    for i, idx in enumerate(indices):
        track_id = track_ids[i]
        sim = cosine_similarity(matrix[idx], centroid)
        similarities.append((track_id, sim))

    # Sort by similarity (descending) and take top N
    similarities.sort(key=lambda x: x[1], reverse=True)
    top_tracks = similarities[:top_n]

    representatives = []
    for track_id, sim in top_tracks:
        record = track_lookup[track_id]
        track_name = record.get("track_name") or record.get("name", "Unknown")

        # Extract artist names
        artists = []
        if "artists" in record:
            artists_data = record["artists"]
            if isinstance(artists_data, list):
                for artist in artists_data:
                    if isinstance(artist, dict):
                        artists.append(artist.get("artist_name") or artist.get("name", "Unknown"))
                    elif isinstance(artist, str):
                        artists.append(artist)

        representatives.append({
            "track_id": track_id,
            "track_name": track_name,
            "artists": artists,
            "similarity_to_centroid": sim,
        })

    return representatives


def _find_top_artists(records: List[Dict], top_n: int) -> List[Dict]:
    """
    Find most frequent artists in cluster.

    Args:
        records: Track records in cluster
        top_n: Number of top artists to return

    Returns:
        List of dicts with artist_name and track_count
    """
    artist_counts = Counter()

    for record in records:
        if "artists" in record:
            artists_data = record["artists"]
            if isinstance(artists_data, list):
                for artist in artists_data:
                    if isinstance(artist, dict):
                        name = artist.get("artist_name") or artist.get("name")
                        if name:
                            artist_counts[name] += 1
                    elif isinstance(artist, str):
                        artist_counts[artist] += 1

    top_artists = []
    for artist_name, count in artist_counts.most_common(top_n):
        top_artists.append({
            "artist_name": artist_name,
            "track_count": count,
        })

    return top_artists


def _compute_coherence(
    matrix: List[List[float]],
    indices: List[int],
    centroid: List[float]
) -> float:
    """
    Compute cluster coherence.

    Coherence = average cosine similarity of tracks to centroid.
    Higher coherence = tighter cluster.

    Args:
        matrix: Normalized feature matrix
        indices: Indices of tracks in cluster
        centroid: Cluster centroid vector

    Returns:
        Coherence score (0-1)
    """
    if not indices:
        return 0.0

    total_similarity = 0.0
    for idx in indices:
        sim = cosine_similarity(matrix[idx], centroid)
        total_similarity += sim

    return total_similarity / len(indices)
