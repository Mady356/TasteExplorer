"""
SQLAlchemy database models for TasteExplorer.

Normalized schema for storing Spotify data and recommendation results.
"""
from datetime import datetime
from typing import List
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, ForeignKey,
    Text, JSON, Index, UniqueConstraint, Enum as SQLEnum
)
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum


class Base(DeclarativeBase):
    pass


class TimeRange(str, enum.Enum):
    """Spotify time range options."""
    SHORT_TERM = "short_term"  # ~4 weeks
    MEDIUM_TERM = "medium_term"  # ~6 months
    LONG_TERM = "long_term"  # several years


class RecommendationType(str, enum.Enum):
    """Type of recommendation."""
    ARTIST = "artist"
    TRACK = "track"


# ============================================================================
# USER MODELS
# ============================================================================

class User(Base):
    """Application user."""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=True)
    username = Column(String(100), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    spotify_profile = relationship("SpotifyProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    user_tracks = relationship("UserTrack", back_populates="user", cascade="all, delete-orphan")
    user_artists = relationship("UserArtist", back_populates="user", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="user", cascade="all, delete-orphan")
    taste_clusters = relationship("TasteCluster", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_users_email", "email"),
        Index("idx_users_created_at", "created_at"),
    )


class SpotifyProfile(Base):
    """User's Spotify profile information."""
    __tablename__ = "spotify_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    spotify_id = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    country = Column(String(10), nullable=True)
    product = Column(String(50), nullable=True)  # premium, free
    followers = Column(Integer, nullable=True)
    profile_image_url = Column(Text, nullable=True)

    # OAuth tokens
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=False)
    token_expires_at = Column(DateTime, nullable=False)
    scope = Column(Text, nullable=True)

    last_synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="spotify_profile")

    __table_args__ = (
        Index("idx_spotify_profiles_spotify_id", "spotify_id"),
        Index("idx_spotify_profiles_user_id", "user_id"),
    )


# ============================================================================
# MUSIC ENTITY MODELS
# ============================================================================

class Artist(Base):
    """Spotify artist."""
    __tablename__ = "artists"

    id = Column(String(100), primary_key=True)  # Spotify artist ID
    name = Column(String(255), nullable=False)
    genres = Column(JSON, nullable=True)  # List of genre strings
    popularity = Column(Integer, nullable=True)
    followers = Column(Integer, nullable=True)
    image_url = Column(Text, nullable=True)
    spotify_url = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    tracks = relationship("TrackArtist", back_populates="artist")
    user_artists = relationship("UserArtist", back_populates="artist")

    __table_args__ = (
        Index("idx_artists_name", "name"),
        Index("idx_artists_popularity", "popularity"),
    )


class Album(Base):
    """Spotify album."""
    __tablename__ = "albums"

    id = Column(String(100), primary_key=True)  # Spotify album ID
    name = Column(String(255), nullable=False)
    album_type = Column(String(50), nullable=True)  # album, single, compilation
    release_date = Column(String(50), nullable=True)
    release_date_precision = Column(String(20), nullable=True)  # year, month, day
    total_tracks = Column(Integer, nullable=True)
    image_url = Column(Text, nullable=True)
    spotify_url = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    tracks = relationship("Track", back_populates="album")

    __table_args__ = (
        Index("idx_albums_release_date", "release_date"),
    )


class Track(Base):
    """Spotify track."""
    __tablename__ = "tracks"

    id = Column(String(100), primary_key=True)  # Spotify track ID
    name = Column(String(500), nullable=False)
    album_id = Column(String(100), ForeignKey("albums.id"), nullable=True)
    duration_ms = Column(Integer, nullable=False)
    explicit = Column(Boolean, default=False, nullable=False)
    popularity = Column(Integer, nullable=True)
    preview_url = Column(Text, nullable=True)
    track_number = Column(Integer, nullable=True)
    disc_number = Column(Integer, nullable=True)
    spotify_url = Column(Text, nullable=True)
    isrc = Column(String(50), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    album = relationship("Album", back_populates="tracks")
    artists = relationship("TrackArtist", back_populates="track")
    audio_features = relationship("AudioFeatures", back_populates="track", uselist=False, cascade="all, delete-orphan")
    user_tracks = relationship("UserTrack", back_populates="track")

    __table_args__ = (
        Index("idx_tracks_name", "name"),
        Index("idx_tracks_popularity", "popularity"),
        Index("idx_tracks_album_id", "album_id"),
    )


class TrackArtist(Base):
    """Many-to-many relationship between tracks and artists."""
    __tablename__ = "track_artists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    track_id = Column(String(100), ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False)
    artist_id = Column(String(100), ForeignKey("artists.id", ondelete="CASCADE"), nullable=False)
    position = Column(Integer, nullable=False, default=0)  # Artist order on track

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    track = relationship("Track", back_populates="artists")
    artist = relationship("Artist", back_populates="tracks")

    __table_args__ = (
        UniqueConstraint("track_id", "artist_id", name="uq_track_artist"),
        Index("idx_track_artists_track_id", "track_id"),
        Index("idx_track_artists_artist_id", "artist_id"),
    )


class AudioFeatures(Base):
    """Spotify audio features for a track."""
    __tablename__ = "audio_features"

    track_id = Column(String(100), ForeignKey("tracks.id", ondelete="CASCADE"), primary_key=True)

    # Core audio features (0.0 to 1.0 range)
    danceability = Column(Float, nullable=False)
    energy = Column(Float, nullable=False)
    speechiness = Column(Float, nullable=False)
    acousticness = Column(Float, nullable=False)
    instrumentalness = Column(Float, nullable=False)
    liveness = Column(Float, nullable=False)
    valence = Column(Float, nullable=False)

    # Other features
    loudness = Column(Float, nullable=False)  # dB
    tempo = Column(Float, nullable=False)  # BPM
    key = Column(Integer, nullable=True)  # 0-11 (C, C#, D, ...)
    mode = Column(Integer, nullable=True)  # 0=minor, 1=major
    time_signature = Column(Integer, nullable=True)
    duration_ms = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    track = relationship("Track", back_populates="audio_features")

    __table_args__ = (
        Index("idx_audio_features_danceability", "danceability"),
        Index("idx_audio_features_energy", "energy"),
        Index("idx_audio_features_valence", "valence"),
        Index("idx_audio_features_tempo", "tempo"),
    )


# ============================================================================
# USER-MUSIC RELATIONSHIP MODELS
# ============================================================================

class UserTrack(Base):
    """User's relationship with a track (top track, saved track, recently played)."""
    __tablename__ = "user_tracks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    track_id = Column(String(100), ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False)

    # Context
    source = Column(String(50), nullable=False)  # top_tracks, saved, recently_played
    time_range = Column(SQLEnum(TimeRange), nullable=True)  # For top tracks
    rank = Column(Integer, nullable=True)  # Position in top tracks
    played_at = Column(DateTime, nullable=True)  # For recently played
    saved_at = Column(DateTime, nullable=True)  # For saved tracks

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="user_tracks")
    track = relationship("Track", back_populates="user_tracks")

    __table_args__ = (
        Index("idx_user_tracks_user_id", "user_id"),
        Index("idx_user_tracks_track_id", "track_id"),
        Index("idx_user_tracks_source", "source"),
        Index("idx_user_tracks_time_range", "time_range"),
    )


class UserArtist(Base):
    """User's relationship with an artist (top artist)."""
    __tablename__ = "user_artists"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    artist_id = Column(String(100), ForeignKey("artists.id", ondelete="CASCADE"), nullable=False)

    # Context
    time_range = Column(SQLEnum(TimeRange), nullable=False)
    rank = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="user_artists")
    artist = relationship("Artist", back_populates="user_artists")

    __table_args__ = (
        Index("idx_user_artists_user_id", "user_id"),
        Index("idx_user_artists_artist_id", "artist_id"),
        Index("idx_user_artists_time_range", "time_range"),
        UniqueConstraint("user_id", "artist_id", "time_range", name="uq_user_artist_time_range"),
    )


# ============================================================================
# RECOMMENDATION MODELS
# ============================================================================

class Recommendation(Base):
    """Recommended artist or track for a user."""
    __tablename__ = "recommendations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Recommendation target
    recommendation_type = Column(SQLEnum(RecommendationType), nullable=False)
    artist_id = Column(String(100), ForeignKey("artists.id", ondelete="CASCADE"), nullable=True)
    track_id = Column(String(100), ForeignKey("tracks.id", ondelete="CASCADE"), nullable=True)

    # Scoring
    score = Column(Float, nullable=False)  # Recommendation confidence score
    rank = Column(Integer, nullable=False)  # Position in recommendation list

    # Explanation
    explanation = Column(Text, nullable=True)  # Human-readable explanation
    recommendation_metadata = Column("metadata", JSON, nullable=True)  # Additional context (similar_to, cluster_id, etc.)

    # Timestamps
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="recommendations")

    __table_args__ = (
        Index("idx_recommendations_user_id", "user_id"),
        Index("idx_recommendations_type", "recommendation_type"),
        Index("idx_recommendations_score", "score"),
        Index("idx_recommendations_generated_at", "generated_at"),
    )


class TasteCluster(Base):
    """User's taste cluster (e.g., "indie rock", "chill electronic")."""
    __tablename__ = "taste_clusters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Cluster metadata
    name = Column(String(255), nullable=False)  # Human-readable name
    description = Column(Text, nullable=True)
    size = Column(Integer, nullable=False, default=0)  # Number of tracks in cluster

    # Cluster characteristics
    centroid = Column(JSON, nullable=True)  # Feature vector centroid
    representative_tracks = Column(JSON, nullable=True)  # List of track IDs
    representative_artists = Column(JSON, nullable=True)  # List of artist IDs

    # Metadata
    cluster_metadata = Column("metadata", JSON, nullable=True)  # Additional context

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="taste_clusters")

    __table_args__ = (
        Index("idx_taste_clusters_user_id", "user_id"),
        Index("idx_taste_clusters_size", "size"),
    )
