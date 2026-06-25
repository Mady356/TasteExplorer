"""
Track clustering using K-Means.

Groups tracks into taste clusters based on audio features.
"""
from typing import List, Dict
from .feature_space import extract_feature_matrix, zscore_normalize


def assign_track_clusters(records: List[Dict], n_clusters: int = 4) -> Dict[str, int]:
    """
    Assign cluster IDs to tracks using K-Means clustering.

    Args:
        records: List of track records with audio features
        n_clusters: Number of clusters to create

    Returns:
        Dict mapping track_id to cluster_id

    Raises:
        ImportError: If scikit-learn is not installed
    """
    try:
        from sklearn.cluster import KMeans
    except ImportError:
        raise ImportError(
            "scikit-learn is required for clustering.\n"
            "Install it with: pip install scikit-learn"
        )

    # Extract and normalize features
    track_ids, track_lookup, feature_matrix, usable_records = extract_feature_matrix(records)

    if len(track_ids) < n_clusters:
        # Not enough tracks for clustering - assign all to cluster 0
        return {track_id: 0 for track_id in track_ids}

    normalized_matrix = zscore_normalize(feature_matrix)

    # Run K-Means
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=42,  # For reproducibility
        n_init=10,
    )
    cluster_labels = kmeans.fit_predict(normalized_matrix)

    # Build mapping
    cluster_assignments = {}
    for track_id, cluster_id in zip(track_ids, cluster_labels):
        cluster_assignments[track_id] = int(cluster_id)

    return cluster_assignments
