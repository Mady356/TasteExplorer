"""
Architecture and system information endpoint.

Returns technical details about the TasteExplorer system for
showcasing the project architecture to recruiters/interviewers.
"""
from typing import Dict, List
from pydantic import BaseModel


class PipelineStage(BaseModel):
    """Data pipeline stage."""
    name: str
    description: str
    input: str
    output: str
    status: str  # implemented, stub, planned


class DatabaseTable(BaseModel):
    """Database table schema summary."""
    name: str
    description: str
    row_count_estimate: str
    key_columns: List[str]


class EngineModule(BaseModel):
    """Recommendation engine module."""
    name: str
    description: str
    status: str  # implemented, stub, planned
    methods: List[str]


class ArchitectureInfo(BaseModel):
    """Complete architecture information."""
    pipeline: List[PipelineStage]
    database: List[DatabaseTable]
    engine_modules: List[EngineModule]
    tech_stack: Dict[str, List[str]]
    key_algorithms: List[Dict[str, str]]


def get_architecture_info() -> ArchitectureInfo:
    """
    Return system architecture information.

    This is used for technical showcase/interview purposes.
    """
    return ArchitectureInfo(
        pipeline=[
            PipelineStage(
                name="Data Ingestion",
                description="OAuth with Spotify, fetch top artists/tracks (3 time ranges), audio features",
                input="Spotify user token",
                output="Normalized track/artist records with audio features",
                status="implemented"
            ),
            PipelineStage(
                name="Feature Extraction",
                description="Extract 7-dimensional audio feature vectors (danceability, energy, valence, etc.)",
                input="Track IDs",
                output="Normalized feature vectors (z-score)",
                status="implemented"
            ),
            PipelineStage(
                name="Graph Construction",
                description="Build k-NN similarity graph using cosine distance on feature vectors",
                input="Feature matrix",
                output="Adjacency list with edge weights",
                status="stub"
            ),
            PipelineStage(
                name="Clustering",
                description="Detect taste clusters using graph community detection (Louvain/DBSCAN)",
                input="Similarity graph",
                output="Cluster assignments + centroids",
                status="stub"
            ),
            PipelineStage(
                name="Candidate Generation",
                description="Generate artist/track candidates via graph traversal and cluster expansion",
                input="User profile + graph",
                output="Ranked candidate list",
                status="stub"
            ),
            PipelineStage(
                name="Scoring & Ranking",
                description="Composite scoring: similarity + novelty + quality signals",
                input="Candidates",
                output="Final rankings with scores",
                status="stub"
            ),
            PipelineStage(
                name="Explanation Generation",
                description="Generate human-readable explanations using template + context",
                input="Recommendation + user profile",
                output="Natural language explanation",
                status="stub"
            ),
        ],
        database=[
            DatabaseTable(
                name="users",
                description="Application users",
                row_count_estimate="1-10K",
                key_columns=["id", "email", "created_at"]
            ),
            DatabaseTable(
                name="spotify_profiles",
                description="OAuth tokens and Spotify user data",
                row_count_estimate="1-10K",
                key_columns=["user_id", "spotify_id", "access_token"]
            ),
            DatabaseTable(
                name="artists",
                description="Artist metadata (name, genres, popularity)",
                row_count_estimate="10K-1M",
                key_columns=["id", "name", "genres", "popularity"]
            ),
            DatabaseTable(
                name="tracks",
                description="Track metadata",
                row_count_estimate="50K-5M",
                key_columns=["id", "name", "album_id", "popularity"]
            ),
            DatabaseTable(
                name="audio_features",
                description="7D feature vectors from Spotify Audio Features API",
                row_count_estimate="50K-5M",
                key_columns=["track_id", "danceability", "energy", "valence"]
            ),
            DatabaseTable(
                name="user_tracks",
                description="User's top tracks with rank and time_range",
                row_count_estimate="50-150 per user",
                key_columns=["user_id", "track_id", "rank", "time_range"]
            ),
            DatabaseTable(
                name="user_artists",
                description="User's top artists with rank and time_range",
                row_count_estimate="50-150 per user",
                key_columns=["user_id", "artist_id", "rank", "time_range"]
            ),
            DatabaseTable(
                name="recommendations",
                description="Generated recommendations (persisted for caching)",
                row_count_estimate="20-100 per user",
                key_columns=["user_id", "type", "rank", "score"]
            ),
            DatabaseTable(
                name="taste_clusters",
                description="User taste clusters with centroids",
                row_count_estimate="3-10 per user",
                key_columns=["user_id", "name", "size", "centroid"]
            ),
        ],
        engine_modules=[
            EngineModule(
                name="RecommendationEngine",
                description="Core graph-based recommendation system",
                status="stub",
                methods=[
                    "build_user_profile() - Extract taste profile from listening history",
                    "generate_artist_candidates() - Find candidate artists via graph traversal",
                    "generate_track_candidates() - Find candidate tracks via k-NN search",
                    "score_recommendations() - Composite scoring (similarity + novelty + quality)",
                    "explain_recommendations() - Generate natural language explanations",
                ]
            ),
            EngineModule(
                name="GraphBuilder",
                description="Constructs track and artist similarity graphs",
                status="stub",
                methods=[
                    "build_track_graph() - k-NN graph with cosine similarity",
                    "build_artist_graph() - Genre/collaboration-based graph",
                    "normalize_features() - Z-score normalization",
                ]
            ),
            EngineModule(
                name="ClusterEngine",
                description="Detects and labels taste clusters",
                status="stub",
                methods=[
                    "detect_clusters() - Community detection algorithm",
                    "compute_centroids() - Calculate cluster centers",
                    "label_clusters() - Assign genre/mood labels",
                ]
            ),
            EngineModule(
                name="NoveltyEngine",
                description="Scores recommendations by novelty/diversity",
                status="stub",
                methods=[
                    "compute_novelty_score() - Inverse popularity + distance from known items",
                    "apply_diversity_filter() - Ensure recommendation diversity",
                ]
            ),
        ],
        tech_stack={
            "frontend": ["Next.js 15", "React 19", "TypeScript", "Tailwind CSS"],
            "backend": ["Python 3.12", "FastAPI", "SQLAlchemy", "Pydantic"],
            "database": ["PostgreSQL 17", "Redis (caching)"],
            "apis": ["Spotify Web API", "OAuth 2.0"],
            "infrastructure": ["Docker", "Docker Compose"],
            "planned": ["scikit-learn (k-NN)", "NetworkX (graph algorithms)", "NumPy/SciPy"],
        },
        key_algorithms=[
            {
                "name": "k-NN Graph Construction",
                "description": "Build similarity graph using cosine distance on z-score normalized audio features",
                "complexity": "O(n² log k) for n tracks, k neighbors",
                "status": "To implement"
            },
            {
                "name": "Community Detection",
                "description": "Detect taste clusters using Louvain or label propagation",
                "complexity": "O(n log n) average case",
                "status": "To implement"
            },
            {
                "name": "Random Walk Sampling",
                "description": "Traverse similarity graph to discover related artists/tracks",
                "complexity": "O(walk_length × degree)",
                "status": "To implement"
            },
            {
                "name": "Composite Ranking",
                "description": "Score = α·similarity + β·novelty + γ·quality, then normalize and rank",
                "complexity": "O(n log n) for sorting",
                "status": "To implement"
            },
        ]
    )
