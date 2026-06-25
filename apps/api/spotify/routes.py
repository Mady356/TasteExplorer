"""Spotify routes."""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from uuid import UUID
import logging

from database import get_db, User
from spotify.client import SpotifyClient
from spotify.ingestion import SpotifyIngestionPipeline

router = APIRouter()
logger = logging.getLogger(__name__)


class SyncResponse(BaseModel):
    """Sync operation response."""
    status: str
    message: str
    details: dict


@router.post("/sync", response_model=SyncResponse)
async def sync_spotify_data(
    user_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Sync user's Spotify data (top artists, top tracks, audio features).

    This endpoint triggers a background task to fetch and store all user data.

    Args:
        user_id: User UUID
        background_tasks: FastAPI background tasks
        db: Database session

    Returns:
        Sync operation status
    """
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.spotify_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has no Spotify profile"
        )

    try:
        # Create Spotify client
        sp = SpotifyClient.from_db_profile(db, user_id)

        # Create ingestion pipeline
        pipeline = SpotifyIngestionPipeline(db, sp)

        # Run sync (this can take a while)
        logger.info(f"Starting Spotify sync for user {user_id}")
        sync_results = pipeline.sync_all(user_id)

        logger.info(f"Spotify sync completed for user {user_id}: {sync_results}")

        return SyncResponse(
            status="success",
            message="Spotify data synced successfully",
            details=sync_results
        )

    except Exception as e:
        logger.error(f"Spotify sync failed for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Sync failed: {str(e)}"
        )


@router.get("/test")
async def test_spotify_connection(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Test Spotify API connection.

    Args:
        user_id: User UUID
        db: Database session

    Returns:
        Connection test result
    """
    try:
        sp = SpotifyClient.from_db_profile(db, user_id)
        user_data = sp.get_current_user()

        return {
            "status": "connected",
            "spotify_user": {
                "id": user_data["id"],
                "display_name": user_data.get("display_name"),
                "email": user_data.get("email"),
            }
        }

    except Exception as e:
        logger.error(f"Spotify connection test failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Connection test failed: {str(e)}"
        )
