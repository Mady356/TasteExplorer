"""Spotify data ingestion pipelines."""
from typing import List, Dict, Tuple
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
import logging

from database.models import (
    User,
    Artist,
    Album,
    Track,
    TrackArtist,
    AudioFeatures,
    UserTrack,
    UserArtist,
    TimeRange,
)
from .client import SpotifyClient

logger = logging.getLogger(__name__)


class SpotifyIngestionPipeline:
    """Pipeline for ingesting Spotify data into database."""

    def __init__(self, db: Session, spotify_client: SpotifyClient):
        """
        Initialize ingestion pipeline.

        Args:
            db: Database session
            spotify_client: Authenticated Spotify client
        """
        self.db = db
        self.sp = spotify_client

    def ingest_artist(self, artist_data: Dict) -> Artist:
        """
        Ingest a single artist into database.

        Args:
            artist_data: Raw Spotify artist object

        Returns:
            Artist model instance
        """
        artist_id = artist_data["id"]

        # Check if artist exists
        artist = self.db.query(Artist).filter(Artist.id == artist_id).first()

        if artist:
            # Update existing artist
            artist.name = artist_data["name"]
            artist.genres = artist_data.get("genres", [])
            artist.popularity = artist_data.get("popularity")
            artist.followers = artist_data.get("followers", {}).get("total")
            artist.spotify_url = artist_data.get("external_urls", {}).get("spotify")

            images = artist_data.get("images", [])
            if images:
                artist.image_url = images[0]["url"]

            artist.updated_at = datetime.utcnow()
        else:
            # Create new artist
            images = artist_data.get("images", [])
            artist = Artist(
                id=artist_id,
                name=artist_data["name"],
                genres=artist_data.get("genres", []),
                popularity=artist_data.get("popularity"),
                followers=artist_data.get("followers", {}).get("total"),
                image_url=images[0]["url"] if images else None,
                spotify_url=artist_data.get("external_urls", {}).get("spotify"),
            )
            self.db.add(artist)

        return artist

    def ingest_album(self, album_data: Dict) -> Album:
        """
        Ingest a single album into database.

        Args:
            album_data: Raw Spotify album object

        Returns:
            Album model instance
        """
        album_id = album_data["id"]

        # Check if album exists
        album = self.db.query(Album).filter(Album.id == album_id).first()

        if album:
            # Update existing album
            album.name = album_data["name"]
            album.album_type = album_data.get("album_type")
            album.release_date = album_data.get("release_date")
            album.release_date_precision = album_data.get("release_date_precision")
            album.total_tracks = album_data.get("total_tracks")
            album.spotify_url = album_data.get("external_urls", {}).get("spotify")

            images = album_data.get("images", [])
            if images:
                album.image_url = images[0]["url"]

            album.updated_at = datetime.utcnow()
        else:
            # Create new album
            images = album_data.get("images", [])
            album = Album(
                id=album_id,
                name=album_data["name"],
                album_type=album_data.get("album_type"),
                release_date=album_data.get("release_date"),
                release_date_precision=album_data.get("release_date_precision"),
                total_tracks=album_data.get("total_tracks"),
                image_url=images[0]["url"] if images else None,
                spotify_url=album_data.get("external_urls", {}).get("spotify"),
            )
            self.db.add(album)

        return album

    def ingest_track(self, track_data: Dict) -> Track:
        """
        Ingest a single track into database.

        Args:
            track_data: Raw Spotify track object

        Returns:
            Track model instance
        """
        track_id = track_data["id"]

        # Ingest album first
        album_data = track_data.get("album")
        album = None
        if album_data:
            album = self.ingest_album(album_data)

        # Check if track exists
        track = self.db.query(Track).filter(Track.id == track_id).first()

        if track:
            # Update existing track
            track.name = track_data["name"]
            track.album_id = album.id if album else None
            track.duration_ms = track_data.get("duration_ms", 0)
            track.explicit = track_data.get("explicit", False)
            track.popularity = track_data.get("popularity")
            track.preview_url = track_data.get("preview_url")
            track.track_number = track_data.get("track_number")
            track.disc_number = track_data.get("disc_number")
            track.spotify_url = track_data.get("external_urls", {}).get("spotify")
            track.isrc = track_data.get("external_ids", {}).get("isrc")
            track.updated_at = datetime.utcnow()
        else:
            # Create new track
            track = Track(
                id=track_id,
                name=track_data["name"],
                album_id=album.id if album else None,
                duration_ms=track_data.get("duration_ms", 0),
                explicit=track_data.get("explicit", False),
                popularity=track_data.get("popularity"),
                preview_url=track_data.get("preview_url"),
                track_number=track_data.get("track_number"),
                disc_number=track_data.get("disc_number"),
                spotify_url=track_data.get("external_urls", {}).get("spotify"),
                isrc=track_data.get("external_ids", {}).get("isrc"),
            )
            self.db.add(track)

        # Ingest track artists
        artists_data = track_data.get("artists", [])
        for position, artist_data in enumerate(artists_data):
            artist = self.ingest_artist(artist_data)

            # Check if track-artist relationship exists
            track_artist = self.db.query(TrackArtist).filter(
                TrackArtist.track_id == track_id,
                TrackArtist.artist_id == artist.id
            ).first()

            if not track_artist:
                track_artist = TrackArtist(
                    track_id=track_id,
                    artist_id=artist.id,
                    position=position
                )
                self.db.add(track_artist)

        return track

    def ingest_audio_features(self, track_id: str, features_data: Dict) -> AudioFeatures:
        """
        Ingest audio features for a track.

        Args:
            track_id: Spotify track ID
            features_data: Raw Spotify audio features object

        Returns:
            AudioFeatures model instance
        """
        # Check if features exist
        features = self.db.query(AudioFeatures).filter(
            AudioFeatures.track_id == track_id
        ).first()

        if features:
            # Update existing features
            features.danceability = features_data["danceability"]
            features.energy = features_data["energy"]
            features.speechiness = features_data["speechiness"]
            features.acousticness = features_data["acousticness"]
            features.instrumentalness = features_data["instrumentalness"]
            features.liveness = features_data["liveness"]
            features.valence = features_data["valence"]
            features.loudness = features_data["loudness"]
            features.tempo = features_data["tempo"]
            features.key = features_data.get("key")
            features.mode = features_data.get("mode")
            features.time_signature = features_data.get("time_signature")
            features.duration_ms = features_data["duration_ms"]
            features.updated_at = datetime.utcnow()
        else:
            # Create new features
            features = AudioFeatures(
                track_id=track_id,
                danceability=features_data["danceability"],
                energy=features_data["energy"],
                speechiness=features_data["speechiness"],
                acousticness=features_data["acousticness"],
                instrumentalness=features_data["instrumentalness"],
                liveness=features_data["liveness"],
                valence=features_data["valence"],
                loudness=features_data["loudness"],
                tempo=features_data["tempo"],
                key=features_data.get("key"),
                mode=features_data.get("mode"),
                time_signature=features_data.get("time_signature"),
                duration_ms=features_data["duration_ms"],
            )
            self.db.add(features)

        return features

    def sync_top_artists(self, user_id: UUID) -> Tuple[int, int, int]:
        """
        Sync user's top artists across all time ranges.

        Args:
            user_id: User UUID

        Returns:
            Tuple of (total_artists, new_artists, updated_artists)
        """
        total = 0
        new = 0
        updated = 0

        for time_range in ["short_term", "medium_term", "long_term"]:
            logger.info(f"Syncing top artists for user {user_id}, time_range={time_range}")

            # Fetch from Spotify
            artists_data = self.sp.get_top_artists(time_range=time_range, limit=50)

            # Delete existing user-artist relationships for this time range
            self.db.query(UserArtist).filter(
                UserArtist.user_id == user_id,
                UserArtist.time_range == time_range
            ).delete()

            for rank, artist_data in enumerate(artists_data, start=1):
                # Ingest artist
                artist_existed = self.db.query(Artist).filter(
                    Artist.id == artist_data["id"]
                ).first() is not None

                artist = self.ingest_artist(artist_data)

                if artist_existed:
                    updated += 1
                else:
                    new += 1
                total += 1

                # Create user-artist relationship
                user_artist = UserArtist(
                    user_id=user_id,
                    artist_id=artist.id,
                    time_range=TimeRange(time_range),
                    rank=rank
                )
                self.db.add(user_artist)

        self.db.commit()
        logger.info(f"Synced {total} top artists (new={new}, updated={updated})")
        return total, new, updated

    def sync_top_tracks(self, user_id: UUID) -> Tuple[int, int, int]:
        """
        Sync user's top tracks across all time ranges.

        Args:
            user_id: User UUID

        Returns:
            Tuple of (total_tracks, new_tracks, updated_tracks)
        """
        total = 0
        new = 0
        updated = 0
        track_ids = []

        for time_range in ["short_term", "medium_term", "long_term"]:
            logger.info(f"Syncing top tracks for user {user_id}, time_range={time_range}")

            # Fetch from Spotify
            tracks_data = self.sp.get_top_tracks(time_range=time_range, limit=50)

            # Delete existing user-track relationships for this time range
            self.db.query(UserTrack).filter(
                UserTrack.user_id == user_id,
                UserTrack.source == "top_tracks",
                UserTrack.time_range == time_range
            ).delete()

            for rank, track_data in enumerate(tracks_data, start=1):
                # Ingest track (and album, artists)
                track_existed = self.db.query(Track).filter(
                    Track.id == track_data["id"]
                ).first() is not None

                track = self.ingest_track(track_data)

                if track_existed:
                    updated += 1
                else:
                    new += 1
                total += 1

                track_ids.append(track.id)

                # Create user-track relationship
                user_track = UserTrack(
                    user_id=user_id,
                    track_id=track.id,
                    source="top_tracks",
                    time_range=TimeRange(time_range),
                    rank=rank
                )
                self.db.add(user_track)

        self.db.commit()

        # Fetch and ingest audio features
        logger.info(f"Fetching audio features for {len(set(track_ids))} unique tracks")
        unique_track_ids = list(set(track_ids))
        features_data = self.sp.get_audio_features(unique_track_ids)

        for features in features_data:
            if features:  # Can be None if features unavailable
                self.ingest_audio_features(features["id"], features)

        self.db.commit()
        logger.info(f"Synced {total} top tracks (new={new}, updated={updated})")
        return total, new, updated

    def sync_all(self, user_id: UUID) -> Dict:
        """
        Sync all user data from Spotify.

        Args:
            user_id: User UUID

        Returns:
            Summary statistics
        """
        logger.info(f"Starting full sync for user {user_id}")

        artist_stats = self.sync_top_artists(user_id)
        track_stats = self.sync_top_tracks(user_id)

        # Update last_synced_at on SpotifyProfile
        from database.models import SpotifyProfile
        profile = self.db.query(SpotifyProfile).filter(
            SpotifyProfile.user_id == user_id
        ).first()
        if profile:
            profile.last_synced_at = datetime.utcnow()
            self.db.commit()

        return {
            "artists": {
                "total": artist_stats[0],
                "new": artist_stats[1],
                "updated": artist_stats[2],
            },
            "tracks": {
                "total": track_stats[0],
                "new": track_stats[1],
                "updated": track_stats[2],
            },
            "synced_at": datetime.utcnow().isoformat(),
        }
