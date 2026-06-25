"""Spotify integration module."""
from .client import SpotifyClient, create_oauth_manager
from .ingestion import SpotifyIngestionPipeline

__all__ = [
    "SpotifyClient",
    "create_oauth_manager",
    "SpotifyIngestionPipeline",
]
