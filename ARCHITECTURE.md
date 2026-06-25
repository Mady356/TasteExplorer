# TasteExplorer Architecture

Complete architectural overview of the TasteExplorer music discovery platform.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                         │
│                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │  Landing   │  │ Dashboard  │  │ Discovery  │           │
│  │    Page    │  │    Page    │  │    Page    │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│         │                │               │                  │
│         └────────────────┴───────────────┘                  │
│                         │                                   │
│                  Next.js App Router                         │
│                   (TypeScript + React)                      │
└─────────────────────────│───────────────────────────────────┘
                          │
                    REST API (JSON)
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      API LAYER (FastAPI)                     │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Auth   │  │  Spotify │  │   User   │  │Analytics │   │
│  │  Module  │  │  Module  │  │  Module  │  │  Module  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Recommendation Engine Interface            │    │
│  │  (Stubs only - implementation required)            │    │
│  │                                                     │    │
│  │  • build_user_profile()                            │    │
│  │  • generate_artist_candidates()                    │    │
│  │  • generate_track_candidates()                     │    │
│  │  • score_recommendations()                         │    │
│  │  • explain_recommendations()                       │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────│───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                      DATA LAYER                              │
│                                                              │
│  ┌─────────────────┐         ┌────────────────┐            │
│  │   PostgreSQL    │         │     Redis      │            │
│  │   (Relational)  │         │    (Cache)     │            │
│  │                 │         │                │            │
│  │  • Users        │         │  • Sessions    │            │
│  │  • Artists      │         │  • Temp data   │            │
│  │  • Tracks       │         │                │            │
│  │  • Features     │         │                │            │
│  └─────────────────┘         └────────────────┘            │
└──────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   EXTERNAL SERVICES                          │
│                                                              │
│  ┌──────────────────────────────────────────────────┐       │
│  │              Spotify Web API                     │       │
│  │                                                  │       │
│  │  • OAuth 2.0 Authentication                     │       │
│  │  • User Top Artists/Tracks                      │       │
│  │  • Audio Features                               │       │
│  │  • Artist/Track Metadata                        │       │
│  └──────────────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────────────┘
```

---

## Module Breakdown

### Frontend (apps/web)

```
apps/web/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── page.tsx           # Landing page
│   │   ├── layout.tsx         # Root layout
│   │   ├── globals.css        # Global styles
│   │   ├── dashboard/         # Dashboard page
│   │   ├── discovery/         # Discovery page
│   │   ├── graph/             # Graph viz page
│   │   └── auth/callback/     # OAuth callback
│   │
│   ├── components/            # React components
│   │   └── ui/                # shadcn/ui components
│   │       ├── card.tsx
│   │       └── button.tsx
│   │
│   ├── lib/                   # Utilities
│   │   └── utils.ts           # Helper functions
│   │
│   ├── types/                 # TypeScript types
│   │   └── index.ts
│   │
│   └── hooks/                 # Custom React hooks
│
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── next.config.ts
```

**Technologies:**
- Next.js 15 (App Router)
- React 19
- TypeScript (strict mode)
- Tailwind CSS
- Framer Motion (animations)
- shadcn/ui (components)

**Key Features:**
- Server-side rendering
- Client-side navigation
- Dark mode support
- Responsive design
- Loading states & skeleton UI

---

### Backend (apps/api)

```
apps/api/
├── auth/                      # Authentication
│   └── routes.py             # Spotify OAuth endpoints
│
├── spotify/                   # Spotify integration
│   ├── client.py             # Spotify API client
│   ├── ingestion.py          # Data ingestion pipeline
│   └── routes.py             # Spotify endpoints
│
├── user/                      # User management
│   └── routes.py             # User CRUD endpoints
│
├── recommender/               # Recommendation engine
│   ├── engine.py             # Engine interface (STUBS)
│   └── __init__.py
│
├── database/                  # Database layer
│   ├── models.py             # SQLAlchemy models
│   ├── database.py           # Session management
│   └── __init__.py
│
├── ingestion/                 # Data ingestion
│   └── __init__.py
│
├── analytics/                 # Analytics module
│   └── __init__.py
│
├── core/                      # Core utilities
│   └── __init__.py
│
├── main.py                    # FastAPI app entry
├── requirements.txt           # Python dependencies
└── Dockerfile                 # Docker image
```

**Technologies:**
- Python 3.12
- FastAPI
- SQLAlchemy (ORM)
- Pydantic (validation)
- Spotipy (Spotify client)

**Key Features:**
- RESTful API
- Auto-generated docs (Swagger/ReDoc)
- Type validation
- Database migrations (Alembic ready)
- OAuth 2.0 flow

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────┐
│    User     │
├─────────────┤
│ id (PK)     │
│ email       │
│ username    │
└─────┬───────┘
      │ 1:1
      ▼
┌─────────────────────┐
│  SpotifyProfile     │
├─────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ spotify_id          │
│ access_token        │
│ refresh_token       │
│ last_synced_at      │
└─────────────────────┘

┌──────────────┐       ┌──────────────┐
│   UserTrack  │       │  UserArtist  │
├──────────────┤       ├──────────────┤
│ id (PK)      │       │ id (PK)      │
│ user_id (FK) │       │ user_id (FK) │
│ track_id (FK)│       │ artist_id    │
│ time_range   │       │ time_range   │
│ rank         │       │ rank         │
└──────┬───────┘       └──────┬───────┘
       │                      │
       │ M:1                  │ M:1
       ▼                      ▼
┌──────────────┐       ┌──────────────┐
│    Track     │◄──────│    Artist    │
├──────────────┤  M:N  ├──────────────┤
│ id (PK)      │       │ id (PK)      │
│ name         │       │ name         │
│ album_id     │       │ genres       │
│ duration_ms  │       │ popularity   │
│ explicit     │       │ followers    │
│ popularity   │       │ image_url    │
└──────┬───────┘       └──────────────┘
       │ 1:1
       ▼
┌────────────────┐
│ AudioFeatures  │
├────────────────┤
│ track_id (PK)  │
│ danceability   │
│ energy         │
│ valence        │
│ tempo          │
│ acousticness   │
│ ...            │
└────────────────┘
```

### Key Tables

**Users & Auth:**
- `users` - Application users
- `spotify_profiles` - OAuth tokens & profile data

**Music Entities:**
- `artists` - Artist metadata & genres
- `tracks` - Track metadata
- `albums` - Album information
- `audio_features` - Spotify audio analysis

**User Relationships:**
- `user_tracks` - User's top/saved tracks
- `user_artists` - User's top artists
- `track_artists` - Track-artist M:N relationship

**Recommendations:**
- `recommendations` - Generated recommendations
- `taste_clusters` - User taste clusters

---

## API Contracts

### Authentication Flow

```
1. User clicks "Connect Spotify"
   └─> GET /auth/spotify/login

2. Redirect to Spotify OAuth
   └─> User authorizes

3. Spotify callback
   └─> GET /auth/spotify/callback?code=...

4. Backend exchanges code for tokens
   └─> Creates User + SpotifyProfile

5. Redirect to frontend
   └─> GET /auth/callback?user_id=...

6. Frontend stores user_id
   └─> Navigate to /dashboard
```

### Data Sync Flow

```
1. User clicks "Sync" button
   └─> POST /spotify/sync?user_id=...

2. Backend fetches Spotify data
   ├─> Top artists (3 time ranges)
   ├─> Top tracks (3 time ranges)
   └─> Audio features (batch)

3. Normalize and store in database
   ├─> Upsert artists
   ├─> Upsert tracks & albums
   ├─> Upsert audio features
   ├─> Create user relationships
   └─> Update last_synced_at

4. Return sync statistics
   └─> { total, new, updated }
```

### Recommendation Flow (To Be Implemented)

```
1. User navigates to /discovery
   └─> GET /users/{id}/recommendations

2. Backend calls RecommendationEngine
   ├─> build_user_profile()
   ├─> generate_artist_candidates()
   ├─> generate_track_candidates()
   ├─> score_recommendations()
   └─> explain_recommendations()

3. Return recommendations with scores & explanations
   └─> Frontend displays cards with similarity scores
```

---

## Recommendation Engine Design

### Interface (Provided)

```python
class RecommendationEngine:
    """Graph-based recommendation system interface."""

    def build_user_profile(user_id: UUID) -> UserProfile:
        """
        Build comprehensive taste profile.

        Analyzes:
        - Top artists & tracks
        - Audio feature preferences
        - Genre distribution
        - Taste clusters
        - Listening patterns

        Returns: UserProfile with all metadata
        """

    def generate_artist_candidates(
        user_id: UUID,
        strategy: RecommendationStrategy,
        limit: int
    ) -> List[Candidate]:
        """
        Generate artist recommendation candidates.

        Strategies:
        - SIMILARITY_BASED: Genre/style similarity
        - GRAPH_TRAVERSAL: Walk artist graph
        - CLUSTER_EXPANSION: Adjacent clusters
        - NOVELTY_SEEKING: Related but different

        Returns: List of candidates with scores
        """

    def generate_track_candidates(
        user_id: UUID,
        strategy: RecommendationStrategy,
        limit: int
    ) -> List[Candidate]:
        """
        Generate track recommendation candidates.

        Uses:
        - Audio feature similarity (cosine)
        - Graph traversal
        - Cluster membership
        - Novelty scoring

        Returns: List of candidates with features
        """

    def score_recommendations(
        user_id: UUID,
        candidates: List[Candidate]
    ) -> List[ScoredRecommendation]:
        """
        Score and rank candidates.

        Scoring factors:
        - Base similarity score
        - Novelty/diversity
        - Popularity/quality
        - Feature alignment
        - Serendipity

        Returns: Ranked recommendations
        """

    def explain_recommendations(
        user_id: UUID,
        recs: List[ScoredRecommendation]
    ) -> List[ScoredRecommendation]:
        """
        Generate human-readable explanations.

        Examples:
        - "Similar to Arctic Monkeys and The Strokes"
        - "High energy tracks like your favorites"
        - "Bridges your indie rock and electronic clusters"

        Returns: Recommendations with explanations
        """
```

### Implementation Strategy (To Do)

**Phase 1: Graph Construction**
```python
# Build track similarity graph
def build_track_graph(user_id):
    tracks = get_user_tracks(user_id)
    features = get_audio_features(tracks)
    normalized = zscore_normalize(features)
    graph = knn_graph(normalized, k=5, metric='cosine')
    return graph
```

**Phase 2: Clustering**
```python
# Detect taste clusters
def detect_clusters(user_id, graph):
    clusters = graph_clustering(graph)  # e.g., Louvain
    centroids = compute_centroids(clusters)
    labels = assign_labels(clusters)  # Genre/mood
    return clusters, centroids, labels
```

**Phase 3: Candidate Generation**
```python
# Generate candidates via graph traversal
def generate_candidates(user_id, graph, strategy):
    if strategy == SIMILARITY_BASED:
        return knn_search(graph, user_tracks)
    elif strategy == GRAPH_TRAVERSAL:
        return random_walk(graph, user_tracks)
    elif strategy == CLUSTER_EXPANSION:
        return expand_clusters(graph, clusters)
```

**Phase 4: Scoring**
```python
# Composite scoring
def score_candidate(candidate, user_profile):
    sim_score = cosine_similarity(candidate, user_profile)
    novelty_score = compute_novelty(candidate)
    quality_score = popularity / 100
    final_score = (0.5 * sim_score) + (0.3 * novelty_score) + (0.2 * quality_score)
    return final_score
```

---

## Technology Decisions

### Why Next.js?
- Server-side rendering for SEO
- App Router for modern routing
- Built-in optimization
- Excellent TypeScript support

### Why FastAPI?
- Fast (async/await)
- Auto-generated API docs
- Type validation with Pydantic
- Easy to learn and deploy

### Why PostgreSQL?
- Relational data model fits music entities
- Excellent JSON support for metadata
- ACID guarantees
- Mature ecosystem

### Why Docker?
- Consistent dev/prod environments
- Easy dependency management
- Service isolation
- Simple deployment

---

## Security Considerations

### Authentication
- OAuth 2.0 via Spotify
- Access tokens stored encrypted
- Automatic token refresh
- No password storage

### API Security
- CORS configured for frontend only
- Input validation on all endpoints
- SQL injection prevention (SQLAlchemy)
- XSS prevention (React escaping)

### Data Privacy
- User data isolated by user_id
- OAuth tokens encrypted at rest
- No sharing of user data
- GDPR-ready data model

---

## Performance Optimization

### Backend
- Database connection pooling
- Redis caching for hot data
- Batch Spotify API requests
- Async endpoints where applicable

### Frontend
- Next.js automatic code splitting
- Image optimization
- Lazy loading for components
- Debounced API calls

### Database
- Indexes on foreign keys
- Indexes on frequently queried fields
- Composite indexes for complex queries
- Partitioning ready for scale

---

## Deployment Architecture (Future)

```
┌─────────────────────────────────────────────┐
│              Load Balancer                   │
└──────────┬────────────────────────┬──────────┘
           │                        │
           ▼                        ▼
    ┌─────────────┐          ┌─────────────┐
    │  Frontend   │          │  Frontend   │
    │   (Vercel)  │          │   (Vercel)  │
    └─────────────┘          └─────────────┘
           │                        │
           └────────┬───────────────┘
                    │
                    ▼
           ┌─────────────────┐
           │   API Gateway    │
           └────────┬─────────┘
                    │
           ┌────────┴──────────┐
           ▼                   ▼
    ┌─────────────┐     ┌─────────────┐
    │  Backend    │     │  Backend    │
    │   (Cloud    │     │   (Cloud    │
    │    Run)     │     │    Run)     │
    └──────┬──────┘     └──────┬──────┘
           │                   │
           └────────┬──────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
 ┌──────────┐ ┌──────────┐ ┌──────────┐
 │CloudSQL  │ │  Redis   │ │  Cloud   │
 │(Postgres)│ │MemStore  │ │ Storage  │
 └──────────┘ └──────────┘ └──────────┘
```

---

## Future Enhancements

### Phase 1 (MVP)
- ✅ Spotify OAuth
- ✅ Data ingestion
- ✅ Database schema
- ✅ REST API
- ✅ Basic UI
- 🚧 Recommendation engine

### Phase 2 (Enhanced)
- [ ] Graph visualization (React Flow/D3.js)
- [ ] Real-time updates
- [ ] Playlist generation
- [ ] Collaborative filtering
- [ ] A/B testing framework

### Phase 3 (Advanced)
- [ ] Last.fm integration
- [ ] Apple Music support
- [ ] Social features
- [ ] Machine learning models
- [ ] Mobile app

---

**Architecture designed for extensibility and clean separation of concerns.**
