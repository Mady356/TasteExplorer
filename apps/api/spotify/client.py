"""Spotify API client."""
import os
from typing import Optional, Dict, List
from datetime import datetime, timedelta
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from sqlalchemy.orm import Session

from database.models import SpotifyProfile


class SpotifyClient:
    """Wrapper for Spotify API interactions."""

    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Spotify client.

        Args:
            access_token: User access token (if None, uses client credentials)
        """
        if access_token:
            self.sp = spotipy.Spotify(auth=access_token)
        else:
            # Client credentials flow (for non-user endpoints)
            client_credentials_manager = SpotifyClientCredentials(
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
            )
            self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    @classmethod
    def from_db_profile(cls, db: Session, user_id: str) -> "SpotifyClient":
        """
        Create client from database SpotifyProfile.

        Args:
            db: Database session
            user_id: User UUID

        Returns:
            SpotifyClient with user access token
        """
        profile = db.query(SpotifyProfile).filter(
            SpotifyProfile.user_id == user_id
        ).first()

        if not profile:
            raise ValueError(f"No Spotify profile found for user {user_id}")

        # Check if token is expired
        if datetime.utcnow() >= profile.token_expires_at:
            # Refresh token
            auth_manager = SpotifyOAuth(
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI")
            )
            token_info = auth_manager.refresh_access_token(profile.refresh_token)

            # Update profile
            profile.access_token = token_info["access_token"]
            profile.token_expires_at = datetime.utcnow() + timedelta(seconds=token_info["expires_in"])
            if "refresh_token" in token_info:
                profile.refresh_token = token_info["refresh_token"]
            db.commit()

        return cls(access_token=profile.access_token)

    def get_current_user(self) -> Dict:
        """Get current user's profile."""
        return self.sp.current_user()

    def get_top_artists(
        self,
        time_range: str = "medium_term",
        limit: int = 50
    ) -> List[Dict]:
        """
        Get user's top artists.

        Args:
            time_range: short_term (~4 weeks), medium_term (~6 months), long_term (years)
            limit: Number of artists (max 50)

        Returns:
            List of artist objects
        """
        response = self.sp.current_user_top_artists(
            time_range=time_range,
            limit=limit
        )
        return response["items"]

    def get_top_tracks(
        self,
        time_range: str = "medium_term",
        limit: int = 50
    ) -> List[Dict]:
        """
        Get user's top tracks.

        Args:
            time_range: short_term, medium_term, long_term
            limit: Number of tracks (max 50)

        Returns:
            List of track objects
        """
        response = self.sp.current_user_top_tracks(
            time_range=time_range,
            limit=limit
        )
        return response["items"]

    def get_saved_tracks(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Get user's saved tracks."""
        response = self.sp.current_user_saved_tracks(limit=limit, offset=offset)
        return response["items"]

    def get_recently_played(self, limit: int = 50) -> List[Dict]:
        """Get user's recently played tracks."""
        response = self.sp.current_user_recently_played(limit=limit)
        return response["items"]

    def get_audio_features(self, track_ids: List[str]) -> List[Dict]:
        """
        Get audio features for tracks.

        Args:
            track_ids: List of Spotify track IDs (max 100)

        Returns:
            List of audio feature objects
        """
        # Spotify allows max 100 IDs per request
        if len(track_ids) > 100:
            # Batch requests
            features = []
            for i in range(0, len(track_ids), 100):
                batch = track_ids[i:i + 100]
                features.extend(self.sp.audio_features(batch))
            return features
        else:
            return self.sp.audio_features(track_ids)

    def get_artist(self, artist_id: str) -> Dict:
        """Get artist details."""
        return self.sp.artist(artist_id)

    def get_track(self, track_id: str) -> Dict:
        """Get track details."""
        return self.sp.track(track_id)

    def get_album(self, album_id: str) -> Dict:
        """Get album details."""
        return self.sp.album(album_id)

    def search(
        self,
        query: str,
        search_type: str = "track",
        limit: int = 20
    ) -> Dict:
        """
        Search Spotify catalog.

        Args:
            query: Search query
            search_type: "track", "artist", "album", "playlist"
            limit: Number of results

        Returns:
            Search results
        """
        return self.sp.search(q=query, type=search_type, limit=limit)


def create_oauth_manager() -> SpotifyOAuth:
    """Create Spotify OAuth manager for authentication flow."""
    return SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=" ".join([
            "user-top-read",
            "user-library-read",
            "user-read-recently-played",
            "user-read-email",
            "user-read-private",
        ]),
        show_dialog=True,
        cache_path=None,  # Don't cache tokens to file
    )
