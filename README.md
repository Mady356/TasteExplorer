# TasteExplorer

**Intelligent music discovery platform powered by custom graph-based recommendations**

TasteExplorer analyzes your Spotify listening history to build a personalized taste profile and recommend artists and tracks that perfectly match your musical preferences. The system uses a modular architecture with clean interfaces for plugging in custom recommendation algorithms.

---

## 🎯 Project Overview

### Problem
Existing music recommendation systems (Spotify, Apple Music) often recommend popular or generic songs. They struggle to understand niche taste clusters and nuanced user preferences.

### Solution
TasteExplorer provides:
- Deep analysis of listening patterns and audio features
- Custom graph-based recommendation engine (interface provided, implementation TBD)
- Personalized explanations for every recommendation
- Visual taste graph exploration

---

## 🏗️ Architecture

```
tasteexplorer/
├── apps/
│   ├── api/              # FastAPI backend
│   │   ├── auth/         # Spotify OAuth
│   │   ├── spotify/      # Spotify API integration
│   │   ├── user/         # User management
│   │   ├── database/     # SQLAlchemy models
│   │   ├── recommender/  # Recommendation engine interface
│   │   ├── ingestion/    # Data ingestion pipelines
│   │   └── analytics/    # Analytics module
│   └── web/              # Next.js frontend
│       ├── src/
│       │   ├── app/      # App router pages
│       │   ├── components/ # React components
│       │   ├── lib/      # Utilities
│       │   └── types/    # TypeScript types
└── packages/             # Shared packages (future)
```

### Tech Stack

**Frontend:**
- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS
- shadcn/ui
- Framer Motion
- React Flow / D3.js (for graph viz)

**Backend:**
- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL 17
- Redis
- Spotipy (Spotify API client)

**Infrastructure:**
- Docker & Docker Compose
- GitHub Actions (CI/CD ready)

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Spotify Developer Account ([create one here](https://developer.spotify.com/dashboard))
- Git

### 1. Set Up Spotify App

**Complete guide:** See [SPOTIFY_SETUP.md](SPOTIFY_SETUP.md) for detailed instructions.

**Quick version:**
1. Go to https://developer.spotify.com/dashboard
2. Create app with redirect URI: `http://localhost:8000/auth/spotify/callback`
3. Copy Client ID and Client Secret

### 2. Clone Repository

```bash
cd /path/to/tasteexplorer
```

### 2. Set Up Spotify App

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Add redirect URI: `http://localhost:8000/auth/spotify/callback`
4. Copy Client ID and Client Secret

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Spotify credentials:

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8000/auth/spotify/callback
FRONTEND_URL=http://localhost:3000
```

### 4. Start Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- FastAPI backend (port 8000)
- Next.js frontend (port 3000)

### 5. Initialize Database

The database tables will be created automatically on first run.

### 6. Access Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🔧 Development Setup

### Backend (FastAPI)

```bash
cd apps/api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run development server
python main.py
```

Backend runs on http://localhost:8000

### Frontend (Next.js)

```bash
cd apps/web

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs on http://localhost:3000

---

## 📊 Database Schema

### Core Tables

- **users** - Application users
- **spotify_profiles** - Spotify OAuth profiles
- **artists** - Artist metadata
- **tracks** - Track metadata
- **albums** - Album metadata
- **audio_features** - Spotify audio features
- **user_tracks** - User's top/saved tracks
- **user_artists** - User's top artists
- **recommendations** - Generated recommendations
- **taste_clusters** - User taste clusters

See `apps/api/database/models.py` for complete schema.

---

## 🎵 API Endpoints

### Authentication

- `GET /auth/spotify/login` - Initiate Spotify OAuth
- `GET /auth/spotify/callback` - OAuth callback
- `POST /auth/spotify/refresh` - Refresh access token

### User

- `GET /users/{id}/profile` - Get user profile
- `GET /users/{id}/artists` - Get top artists
- `GET /users/{id}/tracks` - Get top tracks
- `GET /users/{id}/recommendations` - Get recommendations
- `GET /users/{id}/graph` - Get taste graph
- `GET /users/{id}/stats` - Get user statistics

### Spotify

- `POST /spotify/sync` - Sync Spotify data
- `GET /spotify/test` - Test Spotify connection

Full API documentation: http://localhost:8000/docs

---

## 🧠 Recommendation Engine Interface

The recommendation engine is **NOT implemented** - only the interface is provided.

### Location

`apps/api/recommender/engine.py`

### Interface Methods

```python
class RecommendationEngine:
    def build_user_profile(user_id: UUID) -> UserProfile:
        """Build comprehensive taste profile"""
        # TODO: Implement custom algorithm

    def generate_artist_candidates(user_id: UUID, strategy: str, limit: int) -> List[Candidate]:
        """Generate artist recommendation candidates"""
        # TODO: Implement custom algorithm

    def generate_track_candidates(user_id: UUID, strategy: str, limit: int) -> List[Candidate]:
        """Generate track recommendation candidates"""
        # TODO: Implement custom algorithm

    def score_recommendations(user_id: UUID, candidates: List[Candidate]) -> List[ScoredRecommendation]:
        """Score and rank candidates"""
        # TODO: Implement custom scoring

    def explain_recommendations(user_id: UUID, recs: List[ScoredRecommendation]) -> List[ScoredRecommendation]:
        """Generate human-readable explanations"""
        # TODO: Implement explanation generation

    def get_recommendations(user_id: UUID, num_artists: int, num_tracks: int) -> Dict:
        """Full recommendation pipeline"""
        # TODO: Orchestrate all steps
```

### Mock Implementation

A `MockRecommendationEngine` is provided for frontend development. It returns placeholder data.

### Implementation Notes

The engine should implement:
- Track similarity graphs (audio feature based)
- Artist relationship graphs
- Taste cluster detection
- Graph traversal algorithms
- Novelty scoring
- Feature embeddings

---

## 🎨 Frontend Pages

### 1. Landing Page (`/`)
- Product pitch
- Call-to-action
- Animated hero section
- Feature highlights

### 2. Dashboard (`/dashboard`)
- Top artists grid
- Top tracks list
- Statistics cards
- Sync button

### 3. Discovery (`/discovery`)
- Artist recommendations with explanations
- Track recommendations with scores
- Spotify integration links

### 4. Graph Visualization (`/graph`)
- **Shell only** - visualization not implemented
- Placeholder for React Flow / D3.js graph
- Cluster summaries
- Graph statistics

---

## 🛠️ Common Commands

### Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build

# Reset database
docker-compose down -v
docker-compose up -d
```

### Database

```bash
# Access PostgreSQL
docker exec -it tasteexplorer_postgres psql -U tasteexplorer

# Run migrations (future)
cd apps/api
alembic upgrade head
```

### Frontend

```bash
cd apps/web

# Type check
npm run type-check

# Lint
npm run lint

# Build for production
npm run build
```

### Backend

```bash
cd apps/api

# Run tests (future)
pytest

# Format code
black .

# Lint
flake8
```

---

## 📁 Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/tasteexplorer
REDIS_URL=redis://localhost:6379/0
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:8000/auth/spotify/callback
FRONTEND_URL=http://localhost:3000
CORS_ORIGINS=http://localhost:3000
ENVIRONMENT=development
SQL_ECHO=false  # Set to true for SQL logging
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🚧 TODO: Recommendation Engine

The following components need manual implementation:

### 1. Graph Construction
- [ ] Build track similarity graph using audio features
- [ ] Build artist relationship graph
- [ ] Implement k-NN graph with cosine similarity
- [ ] Add graph persistence layer

### 2. Clustering
- [ ] Implement taste cluster detection algorithm
- [ ] Compute cluster centroids
- [ ] Label clusters with genre/mood tags
- [ ] Store cluster memberships

### 3. Recommendation Generation
- [ ] Implement similarity-based candidate generation
- [ ] Add graph traversal strategies
- [ ] Build cluster expansion logic
- [ ] Add novelty scoring

### 4. Scoring & Ranking
- [ ] Composite scoring (similarity + novelty + quality)
- [ ] Diversity filtering
- [ ] Preference alignment scoring

### 5. Explanation Generation
- [ ] Context-aware explanation templates
- [ ] Similar items identification
- [ ] Cluster/dimension attribution

---

## 🎯 Next Steps

1. **Implement Recommendation Engine**
   - Start with `RecommendationEngine.build_user_profile()`
   - Build track similarity graph
   - Implement clustering algorithm

2. **Add Graph Visualization**
   - Integrate React Flow or D3.js
   - Connect to API graph endpoint
   - Add interactive controls (zoom, pan, filter)

3. **Enhance UI**
   - Add loading skeletons
   - Implement error boundaries
   - Add toast notifications
   - Polish animations

4. **Testing**
   - Unit tests for API endpoints
   - Integration tests for data pipeline
   - E2E tests for user flows

5. **Deployment**
   - Set up CI/CD with GitHub Actions
   - Configure production environment
   - Add monitoring and logging

---

## 📝 Contributing

This is a personal project. The recommendation engine implementation is intentionally left blank for manual development.

---

## 📄 License

MIT License

---

## 🤝 Support

For questions or issues:
1. Check API documentation: http://localhost:8000/docs
2. Review this README
3. Inspect Docker logs: `docker-compose logs -f`

---

## 🎉 Features

✅ Spotify OAuth integration
✅ Data ingestion pipelines
✅ Normalized database schema
✅ REST API with full documentation
✅ Modern, responsive UI
✅ Dark mode support
✅ 3-layer graph-based recommendation engine (Layers 1, 2, 3)
✅ Docker development environment
✅ Production-ready deployment configs

🚧 **To Be Implemented:**
- Graph visualization
- Advanced analytics
- Testing suite

---

## 🚀 Deployment

Ready to deploy to production?

**Quick Deploy:**
- Frontend → Vercel (free tier)
- Backend → Render or Railway (free tier)
- Database → Supabase or Railway (free tier)

**Complete deployment guide:** See [DEPLOYMENT.md](./DEPLOYMENT.md)

**Quick checklist:** See [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)

**What you need:**
- GitHub account (for repo)
- Spotify Developer account (for API keys)
- Vercel account (for frontend)
- Render or Railway account (for backend + database)

**Deployment time:** ~20 minutes following the guide

---

**Built with ❤️ using Next.js, FastAPI, and custom graph algorithms**
