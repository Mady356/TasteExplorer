# Layer 1: Track Similarity Graph - Summary

## ✅ Status: Complete

Layer 1 has been successfully implemented and tested. This layer converts enriched track records into a pure Python graph structure with k-nearest-neighbor similarity edges and clustering.

---

## 📁 Files Created

### Core Modules (`pipeline/graph/`)

1. **`feature_space.py`**
   - `FEATURE_COLUMNS` - 8 audio features used for similarity
   - `extract_feature_matrix()` - extracts features from records (supports flat and nested formats)
   - `zscore_normalize()` - column-wise z-score normalization
   - `cosine_similarity()` - pure Python cosine similarity calculation

2. **`track_graph.py`**
   - `build_track_graph(records, k=5, n_clusters=None)` - main entry point
   - Creates track nodes with metadata and feature vectors
   - Builds directed k-NN edges with similarity scores
   - Integrates clustering when `n_clusters` is provided
   - Returns graph object with nodes, edges, clusters, and metadata

3. **`clustering.py`**
   - `assign_track_clusters(records, n_clusters=4)` - K-Means clustering
   - Uses scikit-learn for clustering
   - Returns track_id → cluster_id mapping
   - Graceful error message if scikit-learn not installed

4. **`cluster_stats.py`**
   - `build_cluster_stats(records, cluster_assignments)` - cluster analysis
   - Computes centroid vectors
   - Finds representative tracks (closest to centroid)
   - Identifies top artists per cluster
   - Calculates coherence score (avg similarity to centroid)

5. **`__init__.py`**
   - Exports main API: `build_track_graph()` and utility functions
   - Clean module interface

### Test Script (`scripts/`)

6. **`test_layer1_graph.py`**
   - Demo script with 5 mock tracks
   - Shows graph construction with k=3 neighbors and 2 clusters
   - Prints:
     - Graph statistics (nodes, edges, features)
     - First 3 nodes with metadata
     - First 3 edges with similarity scores
     - Cluster summaries (track count, coherence, top artists, representatives)
   - Executable with `python scripts/test_layer1_graph.py`

---

## 🎯 Feature Columns (8 dimensions)

The following Spotify audio features are used for similarity:

1. `danceability`
2. `energy`
3. `valence`
4. `acousticness`
5. `instrumentalness`
6. `liveness`
7. `speechiness`
8. `tempo` (normalized from BPM to 0-1 range)

---

## 📊 Graph Structure

### Nodes
Each node represents a track with:
- `track_id` - Spotify track ID
- `track_name` - Track title
- `artists` - List of artist names
- `time_range` - Spotify time range (short/medium/long_term)
- `track_rank` - Original ranking in user's top tracks
- `features` - Normalized 8D feature vector
- `cluster_id` - Cluster assignment (if clustering enabled)

### Edges
Each edge represents a similarity relationship:
- `source_track_id` - Origin track
- `target_track_id` - Similar track
- `similarity` - Cosine similarity score (-1 to 1)
- `distance_rank` - Rank among k nearest neighbors (1 to k)
- `shared_cluster_id` - Cluster ID if both tracks in same cluster, else None

### Clusters (optional)
Each cluster includes:
- `cluster_id` - Cluster number
- `track_count` - Number of tracks
- `centroid_vector` - Mean feature vector
- `representative_tracks` - Top 3 tracks closest to centroid
- `top_artists` - Top 5 most frequent artists
- `coherence_score` - Avg similarity to centroid (0-1, higher = tighter)

---

## 🧪 Test Results

Successfully tested with 5 mock tracks:
- ✅ 5 nodes created
- ✅ 15 edges generated (5 tracks × 3 neighbors)
- ✅ 2 clusters assigned
- ✅ Cluster stats computed (coherence, representatives, top artists)

Example output:
```
Cluster 0: 3 tracks, coherence=0.62
  Top artists: M83, Daft Punk, Earth Wind & Fire
  Representative: September (similarity to centroid: 0.77)

Cluster 1: 2 tracks, coherence=0.76
  Top artists: Arctic Monkeys, Pink Floyd
  Representative: Breathe (similarity to centroid: 0.91)
```

---

## 🔧 Dependencies

Required:
- Python 3.12+ (no external dependencies for core graph building)

Optional:
- `scikit-learn` - for clustering (K-Means)
  - Install: `pip install scikit-learn`
  - If missing, clustering raises helpful error message

---

## 📝 Data Format Support

The layer supports two record formats:

### Flat format (preferred):
```python
{
    "track_id": "spotify_id",
    "track_name": "Song Name",
    "artists": [{"artist_name": "Artist"}],
    "danceability": 0.7,
    "energy": 0.8,
    ...
}
```

### Nested format:
```python
{
    "track_id": "spotify_id",
    "track_name": "Song Name",
    "artists": [{"artist_name": "Artist"}],
    "audio_features": {
        "danceability": 0.7,
        "energy": 0.8,
        ...
    }
}
```

Records missing any required features are filtered out automatically.

---

## 🚀 Usage

```python
from pipeline.graph import build_track_graph
from pipeline.storage import load_dataset  # if available

# Load enriched track records
records, metadata = load_dataset("data/tracks_enriched.parquet")

# Build graph with k=5 neighbors and 4 clusters
graph = build_track_graph(records, k=5, n_clusters=4)

# Access results
print(f"Nodes: {len(graph['nodes'])}")
print(f"Edges: {len(graph['edges'])}")
print(f"Clusters: {len(graph['clusters'])}")

# Get first node
node = graph['nodes'][0]
print(f"Track: {node['track_name']} (cluster {node['cluster_id']})")

# Get edges from a track
track_edges = [e for e in graph['edges'] if e['source_track_id'] == node['track_id']]
print(f"Similar tracks: {len(track_edges)}")
```

---

## ✨ Design Principles

✅ **Pure Python** - No Spotify API calls, no UI, no external graph libraries  
✅ **Clear & Readable** - Small functions, docstrings, type hints  
✅ **Flexible Input** - Handles flat and nested record formats  
✅ **Graceful Degradation** - Works without scikit-learn (no clustering)  
✅ **Easy to Edit** - Simple list/dict structures, no over-engineering  

---

## 🎯 Next Steps (Future Layers)

Layer 1 provides the foundation. Future layers might include:

- **Layer 2**: Artist aggregation and artist-level recommendations
- **Layer 3**: Multi-hop graph traversal and path-based recommendations
- **Layer 4**: UI visualization and interactive exploration

Layer 1 is complete and ready for integration! 🎉
