# TasteExplorer API Reference

Complete API documentation for Layers 1, 2, and 3.

---

## Layer 1: Track Similarity Graph

### `build_track_graph(records, k=5, n_clusters=None)`

Build k-NN track similarity graph with optional clustering.

**Module:** `pipeline.graph`

**Args:**
- `records` (List[Dict]): Track records with audio features
- `k` (int): Number of nearest neighbors per track (default: 5)
- `n_clusters` (Optional[int]): Number of clusters (default: None)

**Returns:**
```python
{
    "nodes": List[Dict],        # Track nodes
    "edges": List[Dict],        # k-NN similarity edges
    "clusters": List[Dict],     # Cluster stats (if n_clusters > 0)
    "metadata": Dict            # Construction metadata
}
```

**Example:**
```python
from pipeline.graph import build_track_graph

layer1 = build_track_graph(user_tracks, k=5, n_clusters=4)
print(f"Nodes: {len(layer1['nodes'])}")
```

---

## Layer 2: Cluster-Level Taste Map

### `build_cluster_graph(layer1_graph, centroid_similarity_threshold=0.3)`

Build cluster-level taste map from Layer 1 graph.

**Module:** `pipeline.graph`

**Args:**
- `layer1_graph` (Dict): Output from `build_track_graph`
- `centroid_similarity_threshold` (float): Min similarity for edges (default: 0.3)

**Returns:**
```python
{
    "cluster_nodes": List[Dict],    # Cluster nodes with labels
    "cluster_edges": List[Dict],    # Cluster relationships
    "metadata": Dict                # Construction metadata
}
```

**Cluster Node Structure:**
```python
{
    "cluster_id": int,
    "track_count": int,
    "centroid_vector": List[float],
    "representative_tracks": List[Dict],
    "top_artists": List[Dict],
    "coherence_score": float,
    "suggested_label": str          # e.g., "bright energetic"
}
```

**Cluster Edge Structure:**
```python
{
    "source_cluster_id": int,
    "target_cluster_id": int,
    "centroid_similarity": float,
    "shared_artist_count": int,
    "edge_type": str                # "strong", "artist_bridge", "feature_similar"
}
```

**Example:**
```python
from pipeline.graph import build_cluster_graph

layer2 = build_cluster_graph(layer1)

for cluster in layer2['cluster_nodes']:
    print(f"Cluster {cluster['cluster_id']}: {cluster['suggested_label']}")
    print(f"  Tracks: {cluster['track_count']}")
    print(f"  Coherence: {cluster['coherence_score']:.2f}")
```

---

## Layer 3: Discovery Graph

### `build_discovery_graph(layer2_graph, candidate_tracks, ...)`

Build discovery graph with scored tracks and ranked artists.

**Module:** `pipeline.recommender`

**Args:**
- `layer2_graph` (Dict): Output from `build_cluster_graph`
- `candidate_tracks` (List[Dict]): Candidate track records
- `known_track_ids` (Optional[Set[str]]): Track IDs to filter out
- `known_artist_ids` (Optional[Set[str]]): Artist IDs to filter out
- `similarity_weight` (float): Weight for similarity (default: 0.75)
- `novelty_weight` (float): Weight for novelty (default: 0.25)
- `top_n_tracks` (int): Number of top tracks (default: 50)
- `top_n_artists` (int): Number of top artists (default: 20)

**Returns:**
```python
{
    "candidate_track_nodes": List[Dict],
    "candidate_artist_nodes": List[Dict],
    "discovery_edges": List[Dict],
    "ranked_artists": List[Dict],
    "ranked_tracks": List[Dict],
    "metadata": Dict
}
```

**Track Node Structure:**
```python
{
    "track_id": str,
    "track_name": str,
    "artist_id": str,
    "artist_name": str,
    "matched_cluster_id": int,
    "similarity_score": float,      # 0-1
    "novelty_score": float,         # 0-1
    "final_score": float,           # 0-1
    "track_popularity": int,        # 0-100
    "explanation": str
}
```

**Artist Node Structure:**
```python
{
    "artist_id": str,
    "artist_name": str,
    "artist_score": float,
    "track_count": int,
    "matched_clusters": List[int],
    "best_track_ids": List[str]
}
```

**Example:**
```python
from pipeline.recommender import build_discovery_graph

layer3 = build_discovery_graph(
    layer2,
    candidate_tracks,
    known_track_ids=user_track_ids,
    similarity_weight=0.8,
    novelty_weight=0.2
)

# Top artists
for artist in layer3['ranked_artists'][:10]:
    print(f"{artist['artist_name']}: {artist['artist_score']:.2f}")

# Top tracks
for track in layer3['ranked_tracks'][:20]:
    print(f"{track['track_name']} - {track['explanation']}")
```

---

## Utility Functions

### Candidate Normalization

#### `normalize_candidate_track(raw_track)`

Normalize candidate track into standard format.

**Module:** `pipeline.recommender`

**Args:**
- `raw_track` (Dict): Raw track dict (Spotify or other source)

**Returns:**
- `Dict` - Normalized track, or `None` if missing required fields

**Example:**
```python
from pipeline.recommender import normalize_candidate_track

normalized = normalize_candidate_track(spotify_track)
if normalized:
    print(normalized['track_name'])
```

---

### Scoring Functions

#### `score_candidate_track(candidate_track, cluster_node, similarity_weight=0.75, novelty_weight=0.25)`

Score a single candidate track against a cluster.

**Module:** `pipeline.recommender`

**Returns:**
```python
{
    "track_id": str,
    "track_name": str,
    "artist_id": str,
    "artist_name": str,
    "matched_cluster_id": int,
    "similarity_score": float,
    "novelty_score": float,
    "final_score": float
}
```

#### `score_candidates_against_clusters(candidate_tracks, cluster_nodes, ...)`

Score all candidates against all clusters.

**Module:** `pipeline.recommender`

**Returns:** List of scored tracks sorted by `final_score` (descending)

---

### Filtering Functions

#### `filter_known_tracks(candidate_tracks, known_track_ids)`

Remove tracks already in user's library.

**Module:** `pipeline.recommender`

**Args:**
- `candidate_tracks` (List[Dict]): Candidates
- `known_track_ids` (Set[str]): Track IDs to exclude

**Returns:** Filtered list

#### `filter_known_artists(candidate_tracks, known_artist_ids)`

Remove tracks by artists already in user's library.

**Module:** `pipeline.recommender`

**Args:**
- `candidate_tracks` (List[Dict]): Candidates
- `known_artist_ids` (Set[str]): Artist IDs to exclude

**Returns:** Filtered list

---

### Artist Ranking Functions

#### `rank_candidate_artists(scored_tracks, top_tracks_per_artist=3)`

Rank artists by their best tracks.

**Module:** `pipeline.recommender`

**Args:**
- `scored_tracks` (List[Dict]): Scored candidate tracks
- `top_tracks_per_artist` (int): Number of top tracks to average

**Returns:** List of artist dicts sorted by `artist_score`

#### `get_top_tracks_overall(scored_tracks, top_n=20)`

Get top N tracks overall (not grouped by artist).

**Module:** `pipeline.recommender`

**Returns:** List of top N tracks

#### `get_top_tracks_per_cluster(scored_tracks, top_n_per_cluster=5)`

Get top N tracks for each cluster.

**Module:** `pipeline.recommender`

**Returns:** Dict mapping `cluster_id` to list of top tracks

#### `get_diverse_recommendations(ranked_artists, top_artists=5, tracks_per_artist=2)`

Get diverse recommendations across multiple artists.

**Module:** `pipeline.recommender`

**Returns:** List of diverse track recommendations

---

### Explanation Functions

#### `generate_explanation(scored_track, cluster_node, candidate_track=None)`

Generate human-readable explanation for a track recommendation.

**Module:** `pipeline.recommender`

**Returns:** Explanation string

**Example:**
```python
from pipeline.recommender import generate_explanation

explanation = generate_explanation(scored_track, cluster)
print(explanation)
# "Matches your 'bright energetic' cluster with very strong similarity. This is an undiscovered track."
```

#### `generate_artist_explanation(artist_dict)`

Generate explanation for an artist recommendation.

**Module:** `pipeline.recommender`

**Returns:** Explanation string

#### `generate_cluster_specific_explanation(scored_track, cluster_node)`

Generate short cluster-specific explanation.

**Module:** `pipeline.recommender`

**Returns:** Short explanation (e.g., "Perfect match, hidden gem")

---

## Feature Space Utilities

### `extract_feature_matrix(records)`

Extract feature matrix from track records.

**Module:** `pipeline.graph`

**Returns:**
```python
(
    track_ids: List[str],
    track_lookup: Dict[str, Dict],
    feature_matrix: List[List[float]],
    usable_records: List[Dict]
)
```

### `zscore_normalize(matrix)`

Z-score normalization (column-wise).

**Module:** `pipeline.graph`

**Returns:** Normalized matrix

### `cosine_similarity(vec_a, vec_b)`

Compute cosine similarity between two vectors.

**Module:** `pipeline.graph`

**Returns:** float in [-1, 1]

---

## Constants

### `FEATURE_COLUMNS`

Audio features used for similarity.

**Module:** `pipeline.graph`

**Value:**
```python
[
    "danceability",
    "energy",
    "valence",
    "acousticness",
    "instrumentalness",
    "liveness",
    "speechiness",
    "tempo"
]
```

---

## Complete Pipeline Example

```python
from pipeline.graph import build_track_graph, build_cluster_graph
from pipeline.recommender import build_discovery_graph
from pipeline.storage import load_dataset  # If available

# Load user's listening history
user_tracks, metadata = load_dataset("data/user_tracks_enriched.parquet")

# Layer 1: Build track similarity graph
layer1 = build_track_graph(
    user_tracks,
    k=5,            # 5 nearest neighbors per track
    n_clusters=4    # 4 taste clusters
)

print(f"Layer 1: {len(layer1['nodes'])} tracks, {len(layer1['clusters'])} clusters")

# Layer 2: Build cluster-level taste map
layer2 = build_cluster_graph(layer1)

print("Layer 2: Taste clusters:")
for cluster in layer2['cluster_nodes']:
    print(f"  - {cluster['suggested_label']} ({cluster['track_count']} tracks)")

# Fetch candidate tracks (from Spotify API, etc.)
candidate_tracks = fetch_spotify_recommendations(user_tracks)

# Extract known IDs
known_track_ids = {t['track_id'] for t in user_tracks}
known_artist_ids = extract_artist_ids(user_tracks)

# Layer 3: Build discovery graph
layer3 = build_discovery_graph(
    layer2,
    candidate_tracks,
    known_track_ids=known_track_ids,
    known_artist_ids=known_artist_ids,
    similarity_weight=0.75,
    novelty_weight=0.25,
    top_n_tracks=50,
    top_n_artists=20
)

# Display recommendations
print("\nTop 10 Recommended Artists:")
for i, artist in enumerate(layer3['ranked_artists'][:10], 1):
    print(f"{i}. {artist['artist_name']} (score: {artist['artist_score']:.2f})")
    for track in artist['best_tracks'][:2]:
        print(f"   - {track['track_name']}")

print("\nTop 20 Recommended Tracks:")
for i, track in enumerate(layer3['ranked_tracks'][:20], 1):
    print(f"{i}. {track['track_name']} by {track['artist_name']}")
    print(f"   Score: {track['final_score']:.2f} | {track['explanation']}")
```

---

## Error Handling

### Layer 1
- Returns empty graph if no valid tracks
- Filters out tracks missing audio features
- Requires `scikit-learn` for clustering (clear error if missing)

### Layer 2
- Returns error metadata if Layer 1 has no clusters
- Handles missing cluster data gracefully

### Layer 3
- Returns empty results if no clusters or no valid candidates
- Normalizes candidates and filters out invalid ones
- Handles missing artist/track IDs

---

## Performance Notes

### Layer 1
- **Time complexity**: O(n² × d) where n = tracks, d = feature dimensions
- **Space complexity**: O(n × d)
- Typical: 1000 tracks → ~1 second

### Layer 2
- **Time complexity**: O(c² × d) where c = clusters (c << n)
- **Space complexity**: O(c × d)
- Typical: 4 clusters → < 0.01 seconds

### Layer 3
- **Time complexity**: O(m × c × d) where m = candidates
- **Space complexity**: O(m)
- Typical: 100 candidates → ~0.1 seconds

**Total pipeline**: ~1-2 seconds for 1000 user tracks + 100 candidates

---

## Type Hints

All functions use type hints for clarity:

```python
def build_track_graph(
    records: List[Dict],
    k: int = 5,
    n_clusters: Optional[int] = None
) -> Dict:
    ...

def score_candidate_track(
    candidate_track: Dict,
    cluster_node: Dict,
    similarity_weight: float = 0.75,
    novelty_weight: float = 0.25
) -> Optional[Dict]:
    ...
```

---

## Testing

Run the test suite:

```bash
# Layer 1
python scripts/test_layer1_graph.py

# Layers 2 & 3
python scripts/test_layers_2_3.py
```

Or with venv:

```bash
.venv/bin/python scripts/test_layer1_graph.py
.venv/bin/python scripts/test_layers_2_3.py
```

---

## Dependencies

**Required:**
- Python 3.12+
- Standard library only (for core functionality)

**Optional:**
- `scikit-learn` - for K-Means clustering (Layer 1)
  - Install: `pip install scikit-learn`
  - Graceful fallback if missing

**Not used:**
- NetworkX (kept simple with lists/dicts)
- NumPy (pure Python implementations)
- Pandas (simple dict/list operations)
- TensorFlow/PyTorch (no deep learning)

---

## Design Philosophy

1. **Transparency over complexity** - rule-based, deterministic
2. **Explainability over accuracy** - users understand recommendations
3. **Simplicity over optimization** - easy to read and modify
4. **Modularity over monolith** - small, composable functions
5. **Type safety over duck typing** - clear contracts

This API is designed to be **interview-friendly**: easy to explain, easy to extend, easy to debug.
