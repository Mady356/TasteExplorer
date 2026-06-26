"""User routes."""
from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from uuid import UUID
import logging

from database import (
    get_db,
    User,
    SpotifyProfile,
    UserTrack,
    UserArtist,
    Track,
    Artist,
    AudioFeatures,
    Recommendation,
    TasteCluster,
    TimeRange,
)
from recommender import MockRecommendationEngine
from .architecture import get_architecture_info, ArchitectureInfo

router = APIRouter()
logger = logging.getLogger(__name__)


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class SpotifyProfileResponse(BaseModel):
    """Spotify profile response."""
    spotify_id: str
    display_name: Optional[str]
    email: Optional[str]
    country: Optional[str]
    product: Optional[str]
    followers: Optional[int]
    profile_image_url: Optional[str]
    last_synced_at: Optional[str]

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    """User profile response."""
    id: str
    email: Optional[str]
    username: Optional[str]
    created_at: str
    last_login: Optional[str]
    spotify_profile: Optional[SpotifyProfileResponse]

    class Config:
        from_attributes = True


class ArtistResponse(BaseModel):
    """Artist response."""
    id: str
    name: str
    genres: Optional[List[str]]
    popularity: Optional[int]
    followers: Optional[int]
    image_url: Optional[str]
    spotify_url: Optional[str]

    class Config:
        from_attributes = True


class TrackResponse(BaseModel):
    """Track response."""
    id: str
    name: str
    artists: List[ArtistResponse]
    album_name: Optional[str]
    duration_ms: int
    explicit: bool
    popularity: Optional[int]
    preview_url: Optional[str]
    spotify_url: Optional[str]

    class Config:
        from_attributes = True


class AudioFeaturesResponse(BaseModel):
    """Audio features response."""
    danceability: float
    energy: float
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    loudness: float

    class Config:
        from_attributes = True


class UserTrackResponse(BaseModel):
    """User track with context."""
    track: TrackResponse
    rank: Optional[int]
    time_range: Optional[str]
    audio_features: Optional[AudioFeaturesResponse]

    class Config:
        from_attributes = True


class UserArtistResponse(BaseModel):
    """User artist with context."""
    artist: ArtistResponse
    rank: int
    time_range: str

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    """Recommendation response."""
    id: str
    type: str
    name: str
    image_url: Optional[str]
    score: float
    rank: int
    explanation: str
    metadata: Optional[Dict]
    spotify_url: Optional[str]


class GraphNodeResponse(BaseModel):
    """Graph node response."""
    id: str
    label: str
    type: str  # "track", "artist", "cluster"
    color: Optional[str]
    size: Optional[float]
    metadata: Optional[Dict]


class GraphEdgeResponse(BaseModel):
    """Graph edge response."""
    source: str
    target: str
    weight: float
    type: str  # "similarity", "artist_track", "cluster_member"


class GraphResponse(BaseModel):
    """Taste graph response."""
    nodes: List[GraphNodeResponse]
    edges: List[GraphEdgeResponse]
    clusters: List[Dict]


# ============================================================================
# ROUTES
# ============================================================================

@router.get("/{user_id}/profile", response_model=UserProfileResponse)
async def get_user_profile(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get user profile.

    Args:
        user_id: User UUID
        db: Database session

    Returns:
        User profile with Spotify data
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserProfileResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        created_at=user.created_at.isoformat(),
        last_login=user.last_login.isoformat() if user.last_login else None,
        spotify_profile=SpotifyProfileResponse(
            spotify_id=user.spotify_profile.spotify_id,
            display_name=user.spotify_profile.display_name,
            email=user.spotify_profile.email,
            country=user.spotify_profile.country,
            product=user.spotify_profile.product,
            followers=user.spotify_profile.followers,
            profile_image_url=user.spotify_profile.profile_image_url,
            last_synced_at=(
                user.spotify_profile.last_synced_at.isoformat()
                if user.spotify_profile.last_synced_at else None
            )
        ) if user.spotify_profile else None
    )


@router.get("/{user_id}/artists", response_model=List[UserArtistResponse])
async def get_user_artists(
    user_id: UUID,
    time_range: Optional[TimeRange] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get user's top artists.

    Args:
        user_id: User UUID
        time_range: Optional filter by time range
        limit: Maximum number of results
        db: Database session

    Returns:
        List of user's top artists
    """
    query = db.query(UserArtist, Artist).join(Artist).filter(
        UserArtist.user_id == user_id
    )

    if time_range:
        query = query.filter(UserArtist.time_range == time_range)

    query = query.order_by(UserArtist.time_range, UserArtist.rank).limit(limit)

    results = []
    for user_artist, artist in query.all():
        results.append(UserArtistResponse(
            artist=ArtistResponse(
                id=artist.id,
                name=artist.name,
                genres=artist.genres,
                popularity=artist.popularity,
                followers=artist.followers,
                image_url=artist.image_url,
                spotify_url=artist.spotify_url,
            ),
            rank=user_artist.rank,
            time_range=user_artist.time_range.value
        ))

    return results


@router.get("/{user_id}/tracks", response_model=List[UserTrackResponse])
async def get_user_tracks(
    user_id: UUID,
    time_range: Optional[TimeRange] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    include_audio_features: bool = Query(False),
    db: Session = Depends(get_db)
):
    """
    Get user's top tracks.

    Args:
        user_id: User UUID
        time_range: Optional filter by time range
        limit: Maximum number of results
        include_audio_features: Include audio features in response
        db: Database session

    Returns:
        List of user's top tracks
    """
    query = db.query(UserTrack, Track).join(Track).filter(
        UserTrack.user_id == user_id,
        UserTrack.source == "top_tracks"
    )

    if time_range:
        query = query.filter(UserTrack.time_range == time_range)

    query = query.order_by(UserTrack.time_range, UserTrack.rank).limit(limit)

    results = []
    for user_track, track in query.all():
        # Get artists
        from database.models import TrackArtist
        track_artists = db.query(Artist).join(TrackArtist).filter(
            TrackArtist.track_id == track.id
        ).order_by(TrackArtist.position).all()

        artist_responses = [
            ArtistResponse(
                id=artist.id,
                name=artist.name,
                genres=artist.genres,
                popularity=artist.popularity,
                followers=artist.followers,
                image_url=artist.image_url,
                spotify_url=artist.spotify_url,
            )
            for artist in track_artists
        ]

        # Get audio features if requested
        audio_features_response = None
        if include_audio_features and track.audio_features:
            af = track.audio_features
            audio_features_response = AudioFeaturesResponse(
                danceability=af.danceability,
                energy=af.energy,
                speechiness=af.speechiness,
                acousticness=af.acousticness,
                instrumentalness=af.instrumentalness,
                liveness=af.liveness,
                valence=af.valence,
                tempo=af.tempo,
                loudness=af.loudness,
            )

        results.append(UserTrackResponse(
            track=TrackResponse(
                id=track.id,
                name=track.name,
                artists=artist_responses,
                album_name=track.album.name if track.album else None,
                duration_ms=track.duration_ms,
                explicit=track.explicit,
                popularity=track.popularity,
                preview_url=track.preview_url,
                spotify_url=track.spotify_url,
            ),
            rank=user_track.rank,
            time_range=user_track.time_range.value if user_track.time_range else None,
            audio_features=audio_features_response
        ))

    return results


@router.get("/{user_id}/recommendations", response_model=Dict[str, List[RecommendationResponse]])
async def get_recommendations(
    user_id: UUID,
    num_artists: int = Query(20, ge=1, le=100),
    num_tracks: int = Query(30, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get personalized recommendations for user.

    This endpoint returns mock data until the custom recommendation engine is implemented.

    Args:
        user_id: User UUID
        num_artists: Number of artist recommendations
        num_tracks: Number of track recommendations
        db: Database session

    Returns:
        Dictionary with 'artists' and 'tracks' recommendations
    """
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # TODO: Use real RecommendationEngine once implemented
    # For now, use mock engine
    engine = MockRecommendationEngine(db)
    recommendations = engine.get_recommendations(
        user_id=user_id,
        num_artists=num_artists,
        num_tracks=num_tracks
    )

    # Format response
    return {
        "artists": [
            RecommendationResponse(
                id=rec.id,
                type=rec.type,
                name=f"Mock Artist {rec.rank}",
                image_url="https://via.placeholder.com/300",
                score=rec.score,
                rank=rec.rank,
                explanation=rec.explanation,
                metadata=rec.recommendation_metadata,
                spotify_url="https://open.spotify.com/artist/mock"
            )
            for rec in recommendations["artists"]
        ],
        "tracks": [
            RecommendationResponse(
                id=rec.id,
                type=rec.type,
                name=f"Mock Track {rec.rank}",
                image_url="https://via.placeholder.com/300",
                score=rec.score,
                rank=rec.rank,
                explanation=rec.explanation,
                metadata=rec.recommendation_metadata,
                spotify_url="https://open.spotify.com/track/mock"
            )
            for rec in recommendations["tracks"]
        ]
    }


@router.get("/{user_id}/graph", response_model=GraphResponse)
async def get_taste_graph(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get user's taste graph for visualization.

    Returns mock graph data until the graph construction algorithm is implemented.

    Args:
        user_id: User UUID
        db: Database session

    Returns:
        Graph with nodes (tracks, artists, clusters) and edges (similarities, relationships)
    """
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # TODO: Implement custom graph-based recommendation engine
    # For now, return mock graph data for frontend development

    # Mock nodes
    nodes = [
        GraphNodeResponse(
            id=f"track_{i}",
            label=f"Track {i}",
            type="track",
            color="#3b82f6",
            size=1.0,
            metadata={"cluster": i % 3}
        )
        for i in range(20)
    ] + [
        GraphNodeResponse(
            id=f"artist_{i}",
            label=f"Artist {i}",
            type="artist",
            color="#ef4444",
            size=1.5,
            metadata={}
        )
        for i in range(10)
    ] + [
        GraphNodeResponse(
            id=f"cluster_{i}",
            label=f"Cluster {i}",
            type="cluster",
            color=["#10b981", "#f59e0b", "#8b5cf6"][i],
            size=2.0,
            metadata={"name": ["Indie Rock", "Electronic", "Hip Hop"][i]}
        )
        for i in range(3)
    ]

    # Mock edges
    edges = [
        GraphEdgeResponse(
            source=f"track_{i}",
            target=f"track_{(i+1)%20}",
            weight=0.8 - (i * 0.02),
            type="similarity"
        )
        for i in range(20)
    ] + [
        GraphEdgeResponse(
            source=f"track_{i}",
            target=f"cluster_{i%3}",
            weight=0.9,
            type="cluster_member"
        )
        for i in range(20)
    ]

    # Mock clusters
    clusters = [
        {
            "id": f"cluster_{i}",
            "name": ["Indie Rock", "Electronic", "Hip Hop"][i],
            "size": [8, 7, 5][i],
            "centroid": [0.65, 0.82, 0.55, 0.43, 0.12, 0.33, 0.58]
        }
        for i in range(3)
    ]

    return GraphResponse(nodes=nodes, edges=edges, clusters=clusters)


@router.get("/{user_id}/stats")
async def get_user_stats(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get user statistics summary.

    Args:
        user_id: User UUID
        db: Database session

    Returns:
        User statistics
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Count entities
    total_artists = db.query(func.count(UserArtist.id)).filter(
        UserArtist.user_id == user_id
    ).scalar()

    total_tracks = db.query(func.count(UserTrack.id)).filter(
        UserTrack.user_id == user_id
    ).scalar()

    total_clusters = db.query(func.count(TasteCluster.id)).filter(
        TasteCluster.user_id == user_id
    ).scalar()

    # Get genre distribution
    # This is a simplified query - actual implementation would be more complex
    top_genres = {}  # TODO: Implement genre aggregation

    return {
        "total_artists": total_artists,
        "total_tracks": total_tracks,
        "total_clusters": total_clusters,
        "top_genres": top_genres,
        "last_synced": (
            user.spotify_profile.last_synced_at.isoformat()
            if user.spotify_profile and user.spotify_profile.last_synced_at
            else None
        )
    }


@router.get("/architecture", response_model=ArchitectureInfo)
async def get_architecture():
    """
    Get system architecture information.

    This endpoint provides technical details about the TasteExplorer system
    for showcasing to recruiters/interviewers.

    Returns:
        Architecture information including pipeline, database, and engine modules
    """
    return get_architecture_info()
