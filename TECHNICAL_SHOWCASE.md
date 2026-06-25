# TasteExplorer - Technical Showcase

**Graph-based music discovery engine for SWE/FDSE recruiting**

---

## Overview

TasteExplorer is a production-grade music intelligence platform that demonstrates:
- Graph-based recommender systems
- Data pipeline engineering
- Full-stack TypeScript/Python development
- Scalable system architecture

**Core Problem:** Mainstream recommendation systems recommend popular tracks. TasteExplorer uses audio feature similarity graphs to discover niche artists at the edges of your taste profile.

**Tech Stack:**
- **Frontend:** Next.js 15, React 19, TypeScript, Tailwind CSS
- **Backend:** Python 3.12, FastAPI, SQLAlchemy, Pydantic
- **Database:** PostgreSQL 17, Redis
- **APIs:** Spotify Web API (OAuth 2.0)
- **Infrastructure:** Docker, Docker Compose

---

## System Architecture

### Data Pipeline

```
Spotify OAuth
    ↓
Top Artists/Tracks (3 time ranges)
    ↓
Audio Features API (7D vectors)
    ↓
Feature Normalization (z-score)
    ↓
Graph Construction (k-NN, cosine)
    ↓
Community Detection (Louvain)
    ↓
Candidate Generation (graph traversal)
    ↓
Composite Scoring (similarity + novelty + quality)
    ↓
Ranked Recommendations
```

### Database Schema

**Core Tables:**
- `users` - Application users
- `spotify_profiles` - OAuth tokens + Spotify metadata
- `artists` - Artist metadata (genres, popularity, followers)
- `tracks` - Track metadata
- `audio_features` - 7D feature vectors (danceability, energy, valence, acousticness, instrumentalness, liveness, tempo)
- `user_tracks` - User's top tracks with rank and time_range
- `user_artists` - User's top artists with rank and time_range
- `recommendations` - Generated recommendations (cached)
- `taste_clusters` - Detected taste clusters with centroids

**Relationships:**
- Users → Spotify Profiles (1:1)
- Users → Top Artists/Tracks (1:N)
- Tracks → Audio Features (1:1)
- Tracks ↔ Artists (M:N via `track_artists`)
- Users → Recommendations (1:N)
- Users → Taste Clusters (1:N)

---

## Recommendation Engine

### Module Structure

**`RecommendationEngine` (Interface)**

Location: `apps/api/recommender/engine.py`

**Status:** Interface defined, implementation stubbed

**Methods:**

```python
def build_user_profile(user_id: UUID) -> UserProfile:
    """
    Analyze user's listening history to extract taste profile.

    Input: User ID
    Process:
        1. Fetch top tracks/artists from database
        2. Extract audio feature preferences (weighted average)
        3. Compute genre distribution
        4. Identify taste clusters
    Output: UserProfile with feature preferences, clusters, metadata
    """

def generate_artist_candidates(
    user_id: UUID,
    strategy: RecommendationStrategy,
    limit: int
) -> List[Candidate]:
    """
    Generate artist recommendations via graph traversal.

    Strategies:
        - SIMILARITY_BASED: Genre overlap + feature distance
        - GRAPH_TRAVERSAL: Random walks on collaboration graph
        - CLUSTER_EXPANSION: Artists in adjacent taste clusters
        - NOVELTY_SEEKING: High distance, low popularity

    Output: Ranked candidates with scores
    """

def generate_track_candidates(
    user_id: UUID,
    strategy: RecommendationStrategy,
    limit: int
) -> List[Candidate]:
    """
    Generate track recommendations via k-NN search.

    Process:
        1. Build user's average feature vector
        2. Normalize all track features (z-score)
        3. Compute cosine similarity
        4. Filter by minimum threshold
        5. Apply diversity filters

    Output: Ranked candidates with scores
    """

def score_recommendations(
    user_id: UUID,
    candidates: List[Candidate]
) -> List[ScoredRecommendation]:
    """
    Composite scoring with multiple signals.

    Score = α·similarity + β·novelty + γ·quality

    Where:
        - similarity: cosine distance in feature space
        - novelty: inverse popularity + distance from known items
        - quality: popularity percentile (quality signal)

    Normalize and rank by final score.
    """

def explain_recommendations(
    user_id: UUID,
    recs: List[ScoredRecommendation]
) -> List[ScoredRecommendation]:
    """
    Generate natural language explanations.

    Template:
        "Close to your [cluster name] cluster;
         [similarity metric] similarity ([score]);
         [popularity context];
         strongest match on [features]"

    Example:
        "Close to your melancholic R&B cluster;
         cosine similarity 0.89;
         low popularity (15th percentile);
         strongest match on valence, acousticness, tempo"
    """
```

### Key Algorithms

**1. k-NN Graph Construction**
- Input: N tracks with 7D feature vectors
- Algorithm: Ball tree or KD tree for approximate nearest neighbors
- Distance: Cosine similarity on z-score normalized features
- Output: Adjacency list with k=5-10 neighbors per node
- Complexity: O(n² log k) naive, O(n log n) with spatial indexing

**2. Community Detection**
- Input: Similarity graph
- Algorithm: Louvain method or label propagation
- Goal: Detect taste clusters (e.g., "indie rock", "electronic", "R&B")
- Output: Cluster assignments + centroids
- Complexity: O(n log n) average case

**3. Graph Traversal**
- Input: User's top tracks, similarity graph
- Algorithm: Random walks with restart
- Goal: Discover related tracks via graph structure
- Output: Candidate set with visitation probabilities
- Complexity: O(walk_length × degree)

**4. Composite Ranking**
- Input: Candidate list
- Algorithm: Weighted linear combination
- Signals:
  - Similarity score (0.5 weight)
  - Novelty score (0.3 weight)
  - Quality score (0.2 weight)
- Output: Final ranked recommendations
- Complexity: O(n log n) for sorting

---

## Implementation Status

### ✅ Completed

**Backend:**
- FastAPI application structure
- SQLAlchemy database models (normalized schema)
- Spotify OAuth 2.0 flow
- Data ingestion pipeline (artists, tracks, audio features)
- RESTful API endpoints with Pydantic validation
- Mock recommendation engine (placeholder data)

**Frontend:**
- Next.js 15 with App Router
- TypeScript (strict mode)
- Minimal UI design (Linear/Palantir aesthetic)
- Dashboard page (top tracks/artists tables)
- Discovery page (ranked recommendations with technical explanations)
- Graph explorer page (UI shell)
- Architecture page (system documentation)

**Infrastructure:**
- Docker Compose (postgres, redis, api, web)
- Environment configuration
- Database migrations ready (Alembic)

### 🚧 To Implement

**Core Algorithms (Manual Implementation Required):**

1. **Graph Construction Module**
   - k-NN graph builder using scikit-learn or annoy
   - Feature normalization (z-score)
   - Edge weight calculation (cosine similarity)
   - Graph persistence layer

2. **Clustering Module**
   - Louvain community detection (via NetworkX or louvain-community)
   - Cluster centroid calculation
   - Cluster labeling (genre/mood inference)

3. **Candidate Generation Module**
   - Random walk sampling
   - Cluster expansion logic
   - Diversity filtering

4. **Scoring Module**
   - Novelty calculation (inverse popularity + distance)
   - Composite scoring function
   - Ranking algorithm

5. **Explanation Module**
   - Template-based generation
   - Context extraction (similar tracks, cluster membership)
   - Natural language output

---

## API Contracts

### Endpoints

**`GET /users/{user_id}/profile`**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "spotify_profile": {
    "spotify_id": "...",
    "display_name": "...",
    "last_synced_at": "2026-01-01T00:00:00Z"
  }
}
```

**`GET /users/{user_id}/tracks?time_range=medium_term&limit=50`**
```json
[
  {
    "track": {
      "id": "...",
      "name": "Midnight City",
      "artists": [{"name": "M83", ...}],
      "duration_ms": 245000
    },
    "rank": 1,
    "time_range": "medium_term"
  }
]
```

**`GET /users/{user_id}/recommendations?num_artists=20&num_tracks=30`**
```json
{
  "artists": [
    {
      "id": "...",
      "type": "artist",
      "name": "...",
      "score": 0.95,
      "rank": 1,
      "explanation": "Close to your melancholic indie cluster...",
      "metadata": {
        "similarity_score": 0.87,
        "novelty_score": 0.65,
        "popularity_percentile": 15,
        "cluster": "indie"
      }
    }
  ],
  "tracks": [...]
}
```

**`GET /users/{user_id}/graph`**
```json
{
  "nodes": [
    {"id": "track_1", "label": "...", "type": "track", ...}
  ],
  "edges": [
    {"source": "track_1", "target": "track_2", "weight": 0.87}
  ],
  "clusters": [
    {"id": "cluster_1", "name": "indie rock", "size": 25, "centroid": [...]}
  ]
}
```

**`GET /users/architecture`**
Returns complete system architecture (pipeline, database, algorithms).

---

## Running the Project

### Prerequisites

- Docker Desktop
- Spotify Developer Account (get credentials at developer.spotify.com)

### Setup

```bash
# 1. Clone and navigate
cd tasteexplorer

# 2. Configure environment
cp .env.example .env
# Edit .env with your Spotify credentials

# 3. Start services
docker-compose up -d

# 4. Access application
open http://localhost:3000
```

### Development

```bash
# Backend (FastAPI)
cd apps/api
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python main.py  # Runs on :8000

# Frontend (Next.js)
cd apps/web
npm install
npm run dev  # Runs on :3000
```

---

## Interview Talking Points

### System Design

**Interviewer:** "How would you scale this system to millions of users?"

**Answer:**
1. **Data Pipeline:** 
   - Batch ingestion with job queues (Celery/RQ)
   - Rate limit Spotify API calls (429 handling)
   - Cache audio features (Redis)

2. **Graph Construction:**
   - Pre-compute similarity graphs offline
   - Use approximate nearest neighbors (Annoy, FAISS)
   - Shard by user_id for parallel processing

3. **Recommendations:**
   - Cache recommendations with TTL (24h)
   - Pre-compute for active users
   - Use CDN for static assets

4. **Database:**
   - Read replicas for analytics queries
   - Partition user_tracks by user_id
   - Index on (user_id, time_range, rank)

### Algorithm Choices

**Interviewer:** "Why k-NN over matrix factorization?"

**Answer:**
- **Interpretability:** k-NN recommendations are explainable (cosine similarity, feature matches)
- **Cold Start:** Works with audio features even without collaborative signals
- **Scalability:** Approximate NN (FAISS) scales to millions of tracks
- **Hybrid Approach:** Can combine with collaborative filtering later

Trade-offs:
- Higher inference cost than pre-computed embeddings
- Requires feature engineering
- Limited by Spotify's feature space (7D)

### Technical Deep-Dive

**Interviewer:** "Walk me through the recommendation pipeline."

**Answer:**
1. **Ingestion:** OAuth → Fetch top 150 tracks (3 time ranges) → Store with audio features
2. **Profile Building:** Extract user's average feature vector + genre distribution
3. **Graph Construction:** Build k-NN graph (k=5-10) with cosine similarity
4. **Clustering:** Detect taste communities (Louvain algorithm)
5. **Candidate Generation:** Random walks + cluster expansion → 100-200 candidates
6. **Scoring:** Composite score = 0.5·similarity + 0.3·novelty + 0.2·quality
7. **Ranking:** Top 20 artists + 30 tracks
8. **Explanation:** Template + context → "Close to [cluster], matches [features]"

---

## Technical Showcase Features

1. **Clean Architecture**
   - Modular backend (auth, spotify, user, recommender)
   - Type-safe API contracts (Pydantic)
   - Normalized database schema

2. **Production Patterns**
   - OAuth 2.0 with token refresh
   - Error handling and validation
   - Loading/empty states in UI
   - Docker containerization

3. **Interview-Ready**
   - Architecture page in the app (system diagram + implementation status)
   - Clear TODO markers for algorithm implementation
   - Mock data for frontend development
   - Documented API contracts

4. **Minimal, Professional UI**
   - No generic SaaS styling
   - Data-focused tables and layouts
   - Technical explanations in recommendations
   - Clean typography and spacing

---

## Next Steps for Implementation

1. **Implement `build_user_profile()`**
   - Query user's tracks with audio features
   - Compute average feature vector
   - Extract genre distribution

2. **Build k-NN Graph**
   - Install scikit-learn or annoy
   - Normalize features (z-score)
   - Build similarity graph
   - Persist to database or in-memory store

3. **Implement Clustering**
   - Install NetworkX
   - Apply Louvain algorithm
   - Label clusters by dominant genre

4. **Generate Candidates**
   - Implement random walk sampling
   - Add diversity filters
   - Score and rank

5. **Replace Mock Engine**
   - Swap `MockRecommendationEngine` with real implementation
   - Test with your own Spotify data

---

## Repository Structure

```
tasteexplorer/
├── apps/
│   ├── api/                    # FastAPI Backend
│   │   ├── auth/              # OAuth routes
│   │   ├── spotify/           # Spotify API client + ingestion
│   │   ├── user/              # User endpoints + architecture
│   │   ├── database/          # SQLAlchemy models
│   │   ├── recommender/       # Engine interface (STUBS)
│   │   └── main.py            # FastAPI app
│   │
│   └── web/                    # Next.js Frontend
│       └── src/
│           └── app/
│               ├── page.tsx           # Landing (technical showcase)
│               ├── dashboard/         # Top tracks/artists
│               ├── discovery/         # Recommendations
│               ├── graph/             # Graph explorer (UI shell)
│               └── architecture/      # System docs
│
├── docker-compose.yml          # 4 services
├── README.md                   # Setup guide
├── ARCHITECTURE.md             # System architecture
└── TECHNICAL_SHOWCASE.md       # This file
```

---

**Built as a technical showcase for Palantir/FAANG SWE recruiting. Demonstrates full-stack engineering, graph algorithms, and production system design.**
