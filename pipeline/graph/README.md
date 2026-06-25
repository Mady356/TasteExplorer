# Layer 1: Track Similarity Graph

Pure Python graph construction from enriched Spotify track records.

## Quick Start

```python
from pipeline.graph import build_track_graph

# Build k-NN graph with clustering
graph = build_track_graph(
    records,           # List[Dict] - enriched track records
    k=5,               # int - neighbors per track
    n_clusters=4       # Optional[int] - number of clusters
)

# Returns:
{
    "nodes": [...],        # List of track nodes
    "edges": [...],        # List of similarity edges
    "clusters": [...],     # List of cluster stats (if n_clusters provided)
    "metadata": {...}      # Construction metadata
}
```

## API Reference

### Main Entry Point

**`build_track_graph(records, k=5, n_clusters=None)`**

Build k-nearest-neighbor track similarity graph with optional clustering.

**Args:**
- `records` (List[Dict]): Track records with audio features
- `k` (int): Number of nearest neighbors per track (default: 5)
- `n_clusters` (Optional[int]): Number of clusters (default: None, no clustering)

**Returns:** Dict with `nodes`, `edges`, `clusters` (optional), and `metadata`

---

### Feature Utilities

**`extract_feature_matrix(records)`**

Extract features from records. Returns `(track_ids, track_lookup, feature_matrix, usable_records)`.

**`zscore_normalize(matrix)`**

Column-wise z-score normalization.

**`cosine_similarity(vec_a, vec_b)`**

Compute cosine similarity between two vectors (returns float in [-1, 1]).

---

### Clustering

**`assign_track_clusters(records, n_clusters=4)`**

Assign cluster IDs using K-Means. Returns `Dict[track_id, cluster_id]`.

**Requires:** `scikit-learn`

**`build_cluster_stats(records, cluster_assignments)`**

Compute cluster statistics. Returns list of cluster stat dicts.

---

## Feature Columns

8 Spotify audio features used for similarity:

```python
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
```

---

## Data Structures

### Node
```python
{
    "track_id": str,
    "track_name": str,
    "artists": List[str],
    "time_range": Optional[str],
    "track_rank": Optional[int],
    "features": List[float],       # 8D normalized vector
    "cluster_id": Optional[int]     # if clustering enabled
}
```

### Edge
```python
{
    "source_track_id": str,
    "target_track_id": str,
    "similarity": float,            # cosine similarity
    "distance_rank": int,           # 1 to k
    "shared_cluster_id": Optional[int]  # if both in same cluster
}
```

### Cluster Stats
```python
{
    "cluster_id": int,
    "track_count": int,
    "centroid_vector": List[float],
    "representative_tracks": List[Dict],  # top 3 closest to centroid
    "top_artists": List[Dict],            # top 5 most frequent
    "coherence_score": float              # avg similarity to centroid
}
```

---

## Input Record Format

Supports both flat and nested formats:

### Flat (preferred)
```python
{
    "track_id": "spotify_id",
    "track_name": "Song Name",
    "artists": [{"artist_name": "Artist"}],
    "danceability": 0.7,
    "energy": 0.8,
    "valence": 0.6,
    "acousticness": 0.1,
    "instrumentalness": 0.0,
    "liveness": 0.2,
    "speechiness": 0.05,
    "tempo": 120.0,
    "time_range": "medium_term",
    "rank": 1
}
```

### Nested
```python
{
    "track_id": "spotify_id",
    "track_name": "Song Name",
    "artists": [{"artist_name": "Artist"}],
    "audio_features": {
        "danceability": 0.7,
        "energy": 0.8,
        ...
    },
    "time_range": "medium_term",
    "rank": 1
}
```

Records missing any required feature are filtered out automatically.

---

## Testing

Run the test script:
```bash
python scripts/test_layer1_graph.py
```

Or with venv:
```bash
.venv/bin/python scripts/test_layer1_graph.py
```

**Note:** Install `scikit-learn` for clustering:
```bash
pip install scikit-learn
```

---

## Design Principles

- ✅ **No Spotify API calls** - works offline with pre-enriched data
- ✅ **Pure Python** - no NetworkX or heavy graph libraries
- ✅ **Simple structures** - lists and dicts, easy to inspect and modify
- ✅ **Type hints** - clear function signatures
- ✅ **Docstrings** - every public function documented
- ✅ **Small functions** - readable, testable, maintainable

---

## Module Files

```
pipeline/graph/
├── __init__.py           # Public API exports
├── feature_space.py      # Feature extraction and similarity
├── track_graph.py        # Graph construction
├── clustering.py         # K-Means clustering
├── cluster_stats.py      # Cluster analysis
└── README.md            # This file
```

---

## Example Usage

```python
from pipeline.graph import build_track_graph, FEATURE_COLUMNS

# Mock data for demo
records = [
    {
        "track_id": "1",
        "track_name": "Track A",
        "artists": [{"artist_name": "Artist X"}],
        "danceability": 0.7,
        "energy": 0.8,
        "valence": 0.6,
        "acousticness": 0.1,
        "instrumentalness": 0.0,
        "liveness": 0.2,
        "speechiness": 0.05,
        "tempo": 120.0,
    },
    # ... more tracks
]

# Build graph
graph = build_track_graph(records, k=3, n_clusters=2)

# Inspect results
print(f"Built graph with {len(graph['nodes'])} nodes")
print(f"Features used: {FEATURE_COLUMNS}")

# Find similar tracks
track_1_edges = [e for e in graph['edges'] if e['source_track_id'] == '1']
for edge in track_1_edges:
    print(f"Similar to {edge['target_track_id']}: {edge['similarity']:.3f}")

# Inspect clusters
for cluster in graph['clusters']:
    print(f"\nCluster {cluster['cluster_id']}:")
    print(f"  {cluster['track_count']} tracks")
    print(f"  Coherence: {cluster['coherence_score']:.3f}")
    print(f"  Top artists: {[a['artist_name'] for a in cluster['top_artists'][:3]]}")
```

---

Built for TasteExplorer - a custom graph-based music recommender.
