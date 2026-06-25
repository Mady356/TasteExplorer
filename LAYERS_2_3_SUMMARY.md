# Layers 2 & 3: Cluster Map & Discovery Graph - Summary

## ✅ Status: Complete

Layers 2 and 3 have been successfully implemented and tested. These layers build on Layer 1 to create cluster-level taste maps and generate personalized track/artist recommendations.

---

## 📁 Files Created

### Layer 2: Cluster-Level Taste Map (`pipeline/graph/`)

**`cluster_graph.py`** (268 lines)
- `build_cluster_graph(layer1_graph)` - main entry point
- Creates cluster nodes with suggested labels
- Builds cluster edges based on centroid similarity and shared artists
- Rule-based cluster labeling (e.g., "bright energetic", "melancholic acoustic")

### Layer 3: Discovery Graph (`pipeline/recommender/`)

1. **`candidate_models.py`** (111 lines)
   - `normalize_candidate_track()` - standardizes candidate track format
   - `create_artist_summary()` - aggregates artist data from tracks
   - Handles flat and nested data formats

2. **`candidate_scoring.py`** (169 lines)
   - `score_candidate_track()` - scores single track against cluster
   - `score_candidates_against_clusters()` - batch scoring
   - `filter_known_tracks()` / `filter_known_artists()` - deduplication
   - Combines similarity (75%) and novelty (25%) scores

3. **`artist_ranking.py`** (131 lines)
   - `rank_candidate_artists()` - groups tracks by artist, computes artist scores
   - `get_top_tracks_overall()` - top N tracks globally
   - `get_top_tracks_per_cluster()` - top N tracks per cluster
   - `get_diverse_recommendations()` - diverse selection across artists

4. **`explanations.py`** (151 lines)
   - `generate_explanation()` - track-level explanations
   - `generate_artist_explanation()` - artist-level explanations
   - `generate_cluster_specific_explanation()` - short cluster explanations
   - Rule-based, human-readable, no LLM

5. **`discovery_graph.py`** (218 lines)
   - `build_discovery_graph()` - main Layer 3 entry point
   - Orchestrates scoring, ranking, and graph construction
   - Creates track nodes, artist nodes, and discovery edges

6. **`__init__.py`** (53 lines)
   - Clean API exports

### Test Script (`scripts/`)

**`test_layers_2_3.py`** (460 lines)
- Tests full pipeline: Layer 1 → Layer 2 → Layer 3
- 6 mock user tracks, 10 mock candidate tracks
- Prints cluster nodes, edges, top artists, top tracks, explanations
- Executable demo

---

## 🎯 Layer 2: Cluster-Level Taste Map

### Purpose
Convert track-level graph (Layer 1) into a higher-level cluster graph representing major taste regions.

### Input
```python
layer1_graph = {
    "nodes": [...],      # Track nodes
    "edges": [...],      # k-NN similarity edges
    "clusters": [...]    # Cluster stats
}
```

### Output
```python
layer2_graph = {
    "cluster_nodes": [...],    # Cluster nodes with labels
    "cluster_edges": [...],    # Cluster relationships
    "metadata": {...}
}
```

### Cluster Node Fields
- `cluster_id` - Cluster number
- `track_count` - Number of tracks in cluster
- `centroid_vector` - 8D normalized centroid
- `representative_tracks` - Top 3 tracks closest to centroid
- `top_artists` - Top 5 most frequent artists
- `coherence_score` - Average similarity to centroid
- **`suggested_label`** - Human-readable label (rule-based)

### Cluster Labels (Examples)
Based on audio feature centroids:
- `"bright energetic"` - high energy + high valence
- `"melancholic acoustic"` - low valence + high acousticness
- `"ambient / instrumental"` - high instrumentalness + low energy
- `"upbeat dance"` - high energy + valence + danceability
- `"dark dance"` - high energy + danceability + low valence
- `"intense / powerful"` - high energy + low valence
- `"calm uplifting"` - low energy + high valence

### Cluster Edge Creation
Edges created if:
1. **Centroid similarity** ≥ threshold (default: 0.3), OR
2. **Shared artists** > 0

Edge types:
- `"strong"` - both criteria met
- `"artist_bridge"` - shared artists only
- `"feature_similar"` - centroid similarity only

### Answers
"What are the user's major taste regions and how are they related?"

---

## 🎯 Layer 3: Discovery Graph

### Purpose
Score candidate tracks/artists against Layer 2 clusters and generate ranked recommendations with explanations.

### Input
```python
layer2_graph = build_cluster_graph(layer1_graph)

candidate_tracks = [...]  # From Spotify API, related artists, etc.
known_track_ids = {...}   # User's existing library
known_artist_ids = {...}
```

### Output
```python
layer3_graph = {
    "candidate_track_nodes": [...],   # Scored tracks with explanations
    "candidate_artist_nodes": [...],  # Ranked artists
    "discovery_edges": [...],         # Candidate → cluster edges
    "ranked_artists": [...],          # Top artists by score
    "ranked_tracks": [...],           # Top tracks by score
    "metadata": {...}
}
```

### Scoring Algorithm

**Track Score = 0.75 × similarity + 0.25 × novelty**

1. **Similarity Score** (0-1)
   - Cosine similarity between candidate features and cluster centroid
   - Normalized from [-1, 1] to [0, 1]
   - Higher = better fit with user's taste

2. **Novelty Score** (0-1)
   - `novelty = 1 - (popularity / 100)`
   - Based on Spotify track popularity
   - Higher = more undiscovered/niche

3. **Final Score**
   - Weighted combination (default: 75% similarity, 25% novelty)
   - Balances fit with discovery potential

**Artist Score**
- Average of top 3 track scores per artist
- Ensures artists with multiple strong tracks rank higher

### Candidate Track Node
```python
{
    "track_id": "...",
    "track_name": "...",
    "artist_id": "...",
    "artist_name": "...",
    "matched_cluster_id": 0,
    "similarity_score": 0.85,
    "novelty_score": 0.65,
    "final_score": 0.80,
    "track_popularity": 35,
    "explanation": "Matches your 'bright energetic' cluster..."
}
```

### Candidate Artist Node
```python
{
    "artist_id": "...",
    "artist_name": "MGMT",
    "artist_score": 0.766,
    "track_count": 2,
    "matched_clusters": [0, 1],
    "best_track_ids": ["...", "..."]
}
```

### Discovery Edges
1. **Track → Cluster**: Links candidate track to best-matching cluster
2. **Artist → Track**: Links artist to their best tracks

### Explanations
Rule-based, transparent explanations:
- Cluster match: `"Matches your 'dark dance' cluster"`
- Similarity: `"with very strong similarity"` (>0.8)
- Novelty: `"This is a hidden gem"` (novelty > 0.8)
- Features: `"Features: high energy, very danceable"`

No LLM calls - fully deterministic and editable.

### Answers
"What new artists and exact tracks should the user try?"

---

## 🧪 Test Results

Tested with:
- **6 user tracks** (Layer 1 input)
- **10 candidate tracks** (Layer 3 input)

### Layer 1 Output
- 6 track nodes
- 18 similarity edges (k=3)
- 2 clusters

### Layer 2 Output
**Cluster 0: "dark dance"**
- 4 tracks
- Coherence: 0.555
- Top artists: M83, Arctic Monkeys, Daft Punk
- Representatives: September, Midnight City

**Cluster 1: "ambient / instrumental"**
- 2 tracks
- Coherence: 0.978
- Top artists: Pink Floyd
- Representatives: Time, Breathe

**Cluster edges**: 0 (clusters too dissimilar, no shared artists)

### Layer 3 Output
**Top 5 Artists:**
1. MGMT (score: 0.766)
2. Arctic Monkeys (score: 0.729)
3. Earth, Wind & Fire (score: 0.723)
4. M83 (score: 0.706)
5. Daft Punk (score: 0.689)

**Top Track:**
- "Electric Feel" by MGMT (score: 0.779)
- Explanation: "Matches your 'dark dance' cluster. with very strong similarity. This is an undiscovered track."

---

## 🏗️ Architecture

```
Layer 1 (Track Graph)
    ↓
    └─ user tracks → k-NN graph → clusters

Layer 2 (Cluster Map)
    ↓
    └─ clusters → cluster nodes → cluster edges → labels

Layer 3 (Discovery)
    ↓
    └─ candidate tracks → scoring → ranking → explanations
```

### Data Flow
1. **Ingest**: User's Spotify listening history → enriched with audio features
2. **Layer 1**: Build track similarity graph with clusters
3. **Layer 2**: Aggregate into cluster-level taste map
4. **Layer 3**: Score external candidates → rank → explain

---

## 📊 File Statistics

```
Layer 2:
  cluster_graph.py          268 lines

Layer 3:
  candidate_models.py       111 lines
  candidate_scoring.py      169 lines
  artist_ranking.py         131 lines
  explanations.py           151 lines
  discovery_graph.py        218 lines
  __init__.py                53 lines
  
Test:
  test_layers_2_3.py        460 lines

Total:                     1,561 lines
```

---

## 🎨 Design Principles

✅ **No Spotify API in scoring** - candidate fetching isolated, scoring offline  
✅ **No UI** - pure backend logic  
✅ **No LLM** - rule-based explanations, fully deterministic  
✅ **No NetworkX** - simple Python lists/dicts  
✅ **No deep ML** - transparent cosine similarity + novelty scoring  
✅ **Type hints & docstrings** - self-documenting code  
✅ **Small functions** - easy to understand and modify  
✅ **Immutable inputs** - no data mutation  

---

## 🚀 Usage

### Quick Start
```python
from pipeline.graph import build_track_graph, build_cluster_graph
from pipeline.recommender import build_discovery_graph

# Layer 1: Track graph
layer1 = build_track_graph(user_tracks, k=5, n_clusters=4)

# Layer 2: Cluster map
layer2 = build_cluster_graph(layer1)

# Layer 3: Discovery
layer3 = build_discovery_graph(
    layer2,
    candidate_tracks,
    known_track_ids={...},
    known_artist_ids={...}
)

# Get recommendations
for artist in layer3['ranked_artists'][:5]:
    print(f"{artist['artist_name']}: {artist['artist_score']:.2f}")

for track in layer3['ranked_tracks'][:10]:
    print(f"{track['track_name']} - {track['explanation']}")
```

### Custom Weights
```python
layer3 = build_discovery_graph(
    layer2,
    candidates,
    similarity_weight=0.6,  # Lower weight on fit
    novelty_weight=0.4,     # Higher weight on discovery
)
```

---

## 🔧 Integration Points

### Candidate Fetching (Not Implemented)
You'll need to implement:
```python
# Example: Fetch from Spotify
def fetch_candidates(user_top_artists):
    candidates = []
    for artist in user_top_artists:
        # Get related artists
        related = spotify.artist_related_artists(artist['id'])
        for r in related:
            # Get top tracks
            tracks = spotify.artist_top_tracks(r['id'])
            candidates.extend(tracks)
    return candidates
```

This should be **isolated** from Layers 2-3, which work with pre-fetched data.

### Recommendation API
```python
@app.get("/recommendations")
def get_recommendations(user_id: str):
    # Load user's tracks
    user_tracks = load_user_tracks(user_id)
    
    # Build layers
    layer1 = build_track_graph(user_tracks, k=5, n_clusters=4)
    layer2 = build_cluster_graph(layer1)
    
    # Fetch candidates (from Spotify, cache, etc.)
    candidates = fetch_candidates_for_user(user_id)
    
    # Build discovery graph
    layer3 = build_discovery_graph(layer2, candidates)
    
    return {
        "artists": layer3['ranked_artists'][:20],
        "tracks": layer3['ranked_tracks'][:50],
    }
```

---

## 🎓 Interview-Ready

This implementation demonstrates:

1. **Graph algorithms** - k-NN, clustering, similarity scoring
2. **Data pipeline** - multi-stage transformation (tracks → clusters → recommendations)
3. **Scoring systems** - weighted combination of similarity + novelty
4. **Scalable design** - offline preprocessing, fast online scoring
5. **Explainability** - rule-based, transparent reasoning
6. **Clean architecture** - separation of concerns, immutable data flow
7. **Type safety** - type hints throughout
8. **Testability** - mock data, isolated functions

Key talking points:
- "I built a 3-layer music recommender using k-NN and K-Means clustering"
- "Scored candidates using cosine similarity against taste clusters"
- "Balanced fit (75%) with novelty (25%) to encourage discovery"
- "Generated rule-based explanations - no black-box ML"
- "Pure Python, no external graph libraries - easy to inspect and modify"

---

## 🎉 Complete!

Layers 2 and 3 are fully functional and ready for integration:

✅ **Layer 2**: Cluster-level taste map with human-readable labels  
✅ **Layer 3**: Discovery graph with scored tracks, ranked artists, and explanations  
✅ **Test suite**: Full pipeline test with mock data  
✅ **Documentation**: Comprehensive guides and examples  

Next steps: Integrate with Spotify API for candidate fetching, build UI, deploy!
