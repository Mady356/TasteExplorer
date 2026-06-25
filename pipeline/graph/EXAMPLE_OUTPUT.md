# Layer 1 Example Output

This shows the exact structure returned by `build_track_graph()`.

## Input

```python
records = [
    {
        "track_id": "track_001",
        "track_name": "Midnight City",
        "artists": [{"artist_name": "M83"}],
        "danceability": 0.67,
        "energy": 0.82,
        "valence": 0.54,
        # ... other features
    },
    # ... more tracks
]

graph = build_track_graph(records, k=3, n_clusters=2)
```

## Output Structure

```python
{
    "nodes": [
        {
            "track_id": "track_001",
            "track_name": "Midnight City",
            "artists": ["M83"],
            "time_range": "medium_term",
            "track_rank": 1,
            "features": [0.12, -0.45, 0.78, ...],  # 8D normalized vector
            "cluster_id": 0
        },
        {
            "track_id": "track_002",
            "track_name": "Do I Wanna Know?",
            "artists": ["Arctic Monkeys"],
            "time_range": "medium_term",
            "track_rank": 2,
            "features": [-0.32, -0.12, -0.56, ...],
            "cluster_id": 1
        },
        # ... more nodes
    ],
    
    "edges": [
        {
            "source_track_id": "track_001",
            "target_track_id": "track_003",
            "similarity": 0.8763,
            "distance_rank": 1,
            "shared_cluster_id": 0
        },
        {
            "source_track_id": "track_001",
            "target_track_id": "track_005",
            "similarity": 0.7234,
            "distance_rank": 2,
            "shared_cluster_id": 0
        },
        {
            "source_track_id": "track_001",
            "target_track_id": "track_002",
            "similarity": 0.4521,
            "distance_rank": 3,
            "shared_cluster_id": None  # Different clusters
        },
        # ... more edges (k per source node)
    ],
    
    "clusters": [
        {
            "cluster_id": 0,
            "track_count": 3,
            "centroid_vector": [0.45, 0.32, 0.67, ...],
            "representative_tracks": [
                {
                    "track_id": "track_003",
                    "track_name": "Digital Love",
                    "artists": ["Daft Punk"],
                    "similarity_to_centroid": 0.9234
                },
                {
                    "track_id": "track_001",
                    "track_name": "Midnight City",
                    "artists": ["M83"],
                    "similarity_to_centroid": 0.8765
                },
                # ... up to 3 tracks
            ],
            "top_artists": [
                {"artist_name": "M83", "track_count": 1},
                {"artist_name": "Daft Punk", "track_count": 1},
                # ... up to 5 artists
            ],
            "coherence_score": 0.7845
        },
        {
            "cluster_id": 1,
            "track_count": 2,
            "centroid_vector": [-0.23, -0.45, -0.12, ...],
            "representative_tracks": [
                # ... similar structure
            ],
            "top_artists": [
                # ... similar structure
            ],
            "coherence_score": 0.8234
        }
    ],
    
    "metadata": {
        "total_input_records": 5,
        "usable_records": 5,
        "k": 3,
        "n_clusters": 2,
        "feature_columns": [
            "danceability",
            "energy",
            "valence",
            "acousticness",
            "instrumentalness",
            "liveness",
            "speechiness",
            "tempo"
        ]
    }
}
```

## Graph Topology

For 5 tracks with k=3:

```
Total nodes: 5
Total edges: 15 (5 tracks × 3 neighbors each)

Track 001 → [003, 005, 002]  (3 outgoing edges)
Track 002 → [004, 003, 001]  (3 outgoing edges)
Track 003 → [001, 005, 002]  (3 outgoing edges)
Track 004 → [002, 003, 001]  (3 outgoing edges)
Track 005 → [003, 001, 002]  (3 outgoing edges)
```

Edges are **directed**: Track A → Track B means "B is similar to A".

## Clusters

Clusters partition the tracks based on feature similarity:

```
Cluster 0: [track_001, track_003, track_005]
  - Coherence: 0.78
  - Representative: Digital Love
  - Top artists: M83, Daft Punk, Earth Wind & Fire

Cluster 1: [track_002, track_004]
  - Coherence: 0.82
  - Representative: Breathe
  - Top artists: Arctic Monkeys, Pink Floyd
```

Higher coherence = tighter cluster (tracks more similar to centroid).

## Edge Attributes

Each edge includes:
- **similarity**: Cosine similarity in [-1, 1]
  - 1.0 = identical tracks
  - 0.0 = orthogonal (unrelated)
  - -1.0 = opposite (rare)
- **distance_rank**: 1 = most similar, k = least similar
- **shared_cluster_id**: Non-null if both tracks in same cluster

## Using the Output

```python
# Find track by ID
def get_track(graph, track_id):
    return next((n for n in graph['nodes'] if n['track_id'] == track_id), None)

# Get neighbors of a track
def get_neighbors(graph, track_id):
    return [e for e in graph['edges'] if e['source_track_id'] == track_id]

# Get all tracks in a cluster
def get_cluster_tracks(graph, cluster_id):
    return [n for n in graph['nodes'] if n.get('cluster_id') == cluster_id]

# Find most similar pair
def most_similar_edge(graph):
    return max(graph['edges'], key=lambda e: e['similarity'])

# Get cluster with highest coherence
def most_coherent_cluster(graph):
    return max(graph['clusters'], key=lambda c: c['coherence_score'])
```

---

This output structure is **pure Python** (lists and dicts), making it easy to:
- Serialize to JSON
- Store in a database
- Convert to NetworkX graph
- Visualize with D3.js
- Query with list comprehensions
