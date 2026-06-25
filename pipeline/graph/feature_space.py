"""
Feature space operations for track similarity.

Handles feature extraction, normalization, and distance calculations.
"""
from typing import List, Dict, Tuple
import math


# Audio features used for similarity
FEATURE_COLUMNS = [
    "danceability",
    "energy",
    "valence",
    "acousticness",
    "instrumentalness",
    "liveness",
    "speechiness",
    "tempo",
]


def extract_feature_matrix(
    records: List[Dict]
) -> Tuple[List[str], Dict[str, Dict], List[List[float]], List[Dict]]:
    """
    Extract feature matrix from track records.

    Supports both flat format (record["danceability"]) and nested format
    (record["audio_features"]["danceability"]).

    Args:
        records: List of track records with audio features

    Returns:
        Tuple of:
            - track_ids: List of track IDs
            - track_lookup: Dict mapping track_id to full record
            - feature_matrix: List of feature vectors (one per track)
            - usable_records: List of records with complete features
    """
    track_ids = []
    track_lookup = {}
    feature_matrix = []
    usable_records = []

    for record in records:
        track_id = record.get("track_id")
        if not track_id:
            continue

        # Try to extract features (flat format first, then nested)
        features = _extract_features_from_record(record)

        # Check if all required features are present
        if features is None or None in features:
            continue

        # Valid record with complete features
        track_ids.append(track_id)
        track_lookup[track_id] = record
        feature_matrix.append(features)
        usable_records.append(record)

    return track_ids, track_lookup, feature_matrix, usable_records


def _extract_features_from_record(record: Dict) -> List[float] | None:
    """
    Extract feature vector from a single record.

    Tries flat format first, then nested "audio_features" format.

    Args:
        record: Track record

    Returns:
        List of feature values, or None if any feature is missing
    """
    features = []

    for col in FEATURE_COLUMNS:
        value = None

        # Try flat format
        if col in record:
            value = record[col]

        # Try nested format
        elif "audio_features" in record and isinstance(record["audio_features"], dict):
            value = record["audio_features"].get(col)

        # Special handling for tempo (needs normalization)
        if value is not None and col == "tempo":
            # Normalize tempo from BPM to 0-1 range (assume 40-200 BPM)
            value = (value - 40) / 160
            value = max(0.0, min(1.0, value))  # Clamp to [0, 1]

        if value is None:
            return None

        features.append(float(value))

    return features


def zscore_normalize(matrix: List[List[float]]) -> List[List[float]]:
    """
    Z-score normalization (column-wise).

    Normalizes each feature dimension to zero mean and unit variance.

    Args:
        matrix: Feature matrix (rows = tracks, cols = features)

    Returns:
        Normalized feature matrix
    """
    if not matrix:
        return []

    n_rows = len(matrix)
    n_cols = len(matrix[0])

    # Compute mean and std for each column
    means = []
    stds = []

    for j in range(n_cols):
        col = [matrix[i][j] for i in range(n_rows)]
        mean = sum(col) / n_rows
        variance = sum((x - mean) ** 2 for x in col) / n_rows
        std = math.sqrt(variance) if variance > 0 else 1.0

        means.append(mean)
        stds.append(std)

    # Normalize
    normalized = []
    for i in range(n_rows):
        normalized_row = [
            (matrix[i][j] - means[j]) / stds[j]
            for j in range(n_cols)
        ]
        normalized.append(normalized_row)

    return normalized


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    Cosine similarity = dot(a, b) / (||a|| * ||b||)
    Returns value in [-1, 1], where 1 = identical direction.

    Args:
        vec_a: First vector
        vec_b: Second vector

    Returns:
        Cosine similarity score
    """
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have same length")

    # Dot product
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))

    # Magnitudes
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))

    # Avoid division by zero
    if mag_a == 0 or mag_b == 0:
        return 0.0

    return dot_product / (mag_a * mag_b)
