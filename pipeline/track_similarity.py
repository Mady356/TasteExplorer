from typing import List, Dict, Tuple
import math


FEATURE_COLUMNS = [
    "danceability",
    "energy",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo",
]


def _has_all_features(record: Dict) -> bool:
    return all(record.get(col) is not None for col in FEATURE_COLUMNS)

def _extract_feature_matrix(records: List[Dict]) -> Tuple[List[str], List[Dict], List[List[float]]]:
    """
    Filter records with complete features and return:
    - track_ids
    - filtered records
    - raw feature matrix
    """
    filtered_records = [r for r in records if _has_all_features(r)]
    track_ids = [r["track_id"] for r in filtered_records]
    matrix = [[float(r[col]) for col in FEATURE_COLUMNS] for r in filtered_records]
    return track_ids, filtered_records, matrix

def _zscore_normalize(matrix: List[List[float]]) -> List[List[float]]:
    """
    Column-wise z-score normalization.
    """
    if not matrix:
        return []

    n_rows = len(matrix)
    n_cols = len(matrix[0])

    means = []
    stds = []

    for j in range(n_cols):
        col = [matrix[i][j] for i in range(n_rows)]
        mean = sum(col) / n_rows
        var = sum((x - mean) ** 2 for x in col) / n_rows
        std = math.sqrt(var)

        means.append(mean)
        stds.append(std if std > 0 else 1.0)

    normalized = []
    for row in matrix:
        normalized_row = [
            (row[j] - means[j]) / stds[j]
            for j in range(n_cols)
        ]
        normalized.append(normalized_row)

    return normalized

def _cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def build_track_similarity_graph(records: List[Dict], k: int = 3) -> Tuple[Dict[str, Dict], Dict[str, List[Dict]]]:
    """
    Build a k-nearest-neighbors track similarity graph.

    Returns:
    - track_lookup: track_id -> record
    - adjacency: track_id -> list of neighbor dicts
      Each neighbor dict contains:
        {
          "neighbor_track_id": ...,
          "distance": ...
        }
    """
    track_ids, filtered_records, matrix = _extract_feature_matrix(records)
    normalized_matrix = _zscore_normalize(matrix)

    track_lookup = {
        record["track_id"]: record
        for record in filtered_records
    }

    adjacency: Dict[str, List[Dict]] = {}

    for i, track_id in enumerate(track_ids):
        similarity = []

        for j, other_track_id in enumerate(track_ids):
            if i == j:
                continue

            sim = _cosine_similarity(normalized_matrix[i], normalized_matrix[j])
            similarity.append({
                "neighbor_track_id": other_track_id,
                "similairty": sim
            })

        similarity.sort(key=lambda x: x["similarity"])
        adjacency[track_id] = similarity[:k]

    return track_lookup, adjacency



