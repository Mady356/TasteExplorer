# Quick Start: Layers 2 & 3

Get up and running with TasteExplorer's recommendation system in 5 minutes.

---

## Installation

```bash
cd tasteexplorer

# Create/activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install scikit-learn
```

---

## Run the Demo

Test all three layers with mock data:

```bash
# Run Layer 1 test
python scripts/test_layer1_graph.py

# Run Layers 2 & 3 test
python scripts/test_layers_2_3.py
```

Expected output:
- Layer 1: 6 track nodes, 2 clusters
- Layer 2: 2 cluster nodes ("dark dance", "ambient / instrumental")
- Layer 3: Top 5 artists, top 5 tracks with explanations

---

## Basic Usage

### Full Pipeline

```python
from pipeline.graph import build_track_graph, build_cluster_graph
from pipeline.recommender import build_discovery_graph

# 1. Layer 1: Build track graph
layer1 = build_track_graph(user_tracks, k=5, n_clusters=4)

# 2. Layer 2: Build cluster map
layer2 = build_cluster_graph(layer1)

# 3. Layer 3: Get recommendations
layer3 = build_discovery_graph(
    layer2,
    candidate_tracks,
    known_track_ids={...},    # Optional: filter known tracks
    known_artist_ids={...}     # Optional: filter known artists
)

# 4. Use recommendations
for artist in layer3['ranked_artists'][:10]:
    print(f"{artist['artist_name']}: {artist['artist_score']:.2f}")
```

---

## Input Data Format

### User Tracks (Layer 1 Input)

```python
user_tracks = [
    {
        "track_id": "spotify_id",
        "track_name": "Song Name",
        "artists": [{"artist_name": "Artist Name"}],
        "rank": 1,
        "time_range": "medium_term",
        # Audio features (flat format)
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
```

### Candidate Tracks (Layer 3 Input)

```python
candidate_tracks = [
    {
        "track_id": "candidate_id",
        "track_name": "Candidate Song",
        "artists": [{"artist_id": "artist_id", "artist_name": "Artist"}],
        "popularity": 45,
        # Audio features (same as above)
        "danceability": 0.75,
        "energy": 0.85,
        # ... other features
    },
    # ... more candidates
]
```

---

## Output Structures

### Layer 1: Track Graph

```python
{
    "nodes": [
        {
            "track_id": "...",
            "track_name": "...",
            "artists": ["..."],
            "cluster_id": 0,
            "features": [...]
        }
    ],
    "edges": [
        {
            "source_track_id": "...",
            "target_track_id": "...",
            "similarity": 0.85,
            "distance_rank": 1
        }
    ],
    "clusters": [...]
}
```

### Layer 2: Cluster Map

```python
{
    "cluster_nodes": [
        {
            "cluster_id": 0,
            "suggested_label": "bright energetic",
            "track_count": 15,
            "coherence_score": 0.75,
            "top_artists": [...],
            "representative_tracks": [...]
        }
    ],
    "cluster_edges": [...]
}
```

### Layer 3: Discovery Graph

```python
{
    "ranked_artists": [
        {
            "artist_name": "MGMT",
            "artist_score": 0.766,
            "track_count": 2,
            "best_tracks": [...]
        }
    ],
    "ranked_tracks": [
        {
            "track_name": "Electric Feel",
            "artist_name": "MGMT",
            "final_score": 0.779,
            "similarity_score": 0.822,
            "novelty_score": 0.650,
            "explanation": "Matches your 'dark dance' cluster..."
        }
    ]
}
```

---

## Customization

### Adjust Cluster Count

```python
# More clusters = finer-grained taste segmentation
layer1 = build_track_graph(user_tracks, k=5, n_clusters=6)
```

### Adjust Similarity vs Novelty

```python
# Favor similarity (safe recommendations)
layer3 = build_discovery_graph(
    layer2,
    candidates,
    similarity_weight=0.9,
    novelty_weight=0.1
)

# Favor novelty (adventurous recommendations)
layer3 = build_discovery_graph(
    layer2,
    candidates,
    similarity_weight=0.6,
    novelty_weight=0.4
)
```

### Get Diverse Recommendations

```python
from pipeline.recommender import get_diverse_recommendations

# Get tracks from multiple artists
diverse = get_diverse_recommendations(
    layer3['ranked_artists'],
    top_artists=5,
    tracks_per_artist=2
)
```

### Cluster-Specific Recommendations

```python
from pipeline.recommender import get_top_tracks_per_cluster

# Get top tracks for each taste cluster
by_cluster = get_top_tracks_per_cluster(
    layer3['ranked_tracks'],
    top_n_per_cluster=5
)

for cluster_id, tracks in by_cluster.items():
    print(f"Cluster {cluster_id}:")
    for track in tracks:
        print(f"  - {track['track_name']}")
```

---

## Integration with Spotify

### Fetch User's Top Tracks

```python
import spotipy

sp = spotipy.Spotify(auth=token)

# Get user's top tracks
top_tracks = sp.current_user_top_tracks(limit=50, time_range='medium_term')

# Enrich with audio features
from pipeline.enrich_audio_features import enrich_audio_features
user_tracks = enrich_audio_features(sp, top_tracks['items'])
```

### Fetch Candidate Tracks

```python
def fetch_candidates(sp, user_top_artists):
    """Fetch candidate tracks from related artists."""
    candidates = []
    
    for artist in user_top_artists[:10]:
        # Get related artists
        related = sp.artist_related_artists(artist['id'])
        
        for rel_artist in related['artists'][:5]:
            # Get artist's top tracks
            top_tracks = sp.artist_top_tracks(rel_artist['id'])
            
            for track in top_tracks['tracks'][:3]:
                # Fetch audio features
                features = sp.audio_features([track['id']])[0]
                if features:
                    track['audio_features'] = features
                    candidates.append(track)
    
    return candidates
```

---

## Common Workflows

### 1. Personal Recommendations

```python
# Build user's taste profile
layer1 = build_track_graph(user_tracks, k=5, n_clusters=4)
layer2 = build_cluster_graph(layer1)

# Fetch candidates from Spotify
candidates = fetch_spotify_candidates(user)

# Get recommendations
layer3 = build_discovery_graph(layer2, candidates)

# Show top 20 tracks
for track in layer3['ranked_tracks'][:20]:
    print(f"{track['track_name']} - {track['explanation']}")
```

### 2. Taste Analysis

```python
# Build taste profile
layer1 = build_track_graph(user_tracks, k=5, n_clusters=4)
layer2 = build_cluster_graph(layer1)

# Analyze taste clusters
print("Your taste profile:")
for cluster in layer2['cluster_nodes']:
    print(f"\n{cluster['suggested_label']}:")
    print(f"  {cluster['track_count']} tracks")
    print(f"  Top artists: {', '.join(a['artist_name'] for a in cluster['top_artists'][:3])}")
```

### 3. Discovery Mode

```python
# Emphasize novelty for discovery
layer3 = build_discovery_graph(
    layer2,
    candidates,
    similarity_weight=0.5,   # Lower similarity weight
    novelty_weight=0.5        # Higher novelty weight
)

# Show hidden gems
hidden_gems = [
    t for t in layer3['ranked_tracks']
    if t['novelty_score'] > 0.7
]

print("Hidden gems:")
for track in hidden_gems[:10]:
    print(f"{track['track_name']} by {track['artist_name']}")
```

---

## Troubleshooting

### "No clusters in Layer 1 graph"

Make sure to pass `n_clusters` to Layer 1:
```python
layer1 = build_track_graph(user_tracks, k=5, n_clusters=4)
```

### "scikit-learn required"

Install scikit-learn for clustering:
```bash
pip install scikit-learn
```

### Missing audio features

Ensure tracks have all required features:
- danceability, energy, valence, acousticness
- instrumentalness, liveness, speechiness, tempo

Use `enrich_audio_features()` to fetch from Spotify.

### Low recommendation scores

Try:
- Increase cluster count for finer segmentation
- Adjust similarity/novelty weights
- Fetch more diverse candidates

---

## Next Steps

1. **Integrate with Spotify** - fetch real user data and candidates
2. **Build UI** - visualize taste clusters and recommendations
3. **Add caching** - store Layer 1/2 results for fast recommendations
4. **Deploy** - containerize with Docker, deploy to cloud

See `API_REFERENCE.md` for full API documentation.

---

## Examples

### Minimal Example

```python
from pipeline.graph import build_track_graph, build_cluster_graph
from pipeline.recommender import build_discovery_graph

# Mock data
user_tracks = [...]  # Your tracks
candidates = [...]   # Candidate tracks

# Build full pipeline
layer1 = build_track_graph(user_tracks, k=5, n_clusters=4)
layer2 = build_cluster_graph(layer1)
layer3 = build_discovery_graph(layer2, candidates)

# Get top 10 recommendations
print("Top 10 Recommended Tracks:")
for i, track in enumerate(layer3['ranked_tracks'][:10], 1):
    print(f"{i}. {track['track_name']} by {track['artist_name']}")
    print(f"   {track['explanation']}\n")
```

### With Filtering

```python
# Extract known IDs
known_tracks = {t['track_id'] for t in user_tracks}
known_artists = {
    artist.get('artist_id')
    for t in user_tracks
    for artist in t.get('artists', [])
    if artist.get('artist_id')
}

# Filter out known
layer3 = build_discovery_graph(
    layer2,
    candidates,
    known_track_ids=known_tracks,
    known_artist_ids=known_artists
)
```

---

## Performance Tips

- **Cache Layer 1/2**: Rebuild only when user's library changes
- **Batch candidates**: Score 100-500 candidates at once
- **Parallel processing**: Use multiprocessing for large candidate sets
- **Limit features**: 8 features is optimal balance of quality/speed

---

Ready to explore! 🎵
