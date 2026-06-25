"""Authentication routes."""
import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import logging

from database import get_db, User, SpotifyProfile
from spotify.client import create_oauth_manager

router = APIRouter()
logger = logging.getLogger(__name__)


class TokenResponse(BaseModel):
    """OAuth token response."""
    access_token: str
    token_type: str = "bearer"
    user_id: str


@router.get("/spotify/login")
async def spotify_login():
    """
    Initiate Spotify OAuth flow.

    Returns:
        Redirect to Spotify authorization page
    """
    auth_manager = create_oauth_manager()
    auth_url = auth_manager.get_authorize_url()
    return RedirectResponse(url=auth_url)


@router.get("/spotify/callback")
async def spotify_callback(
    code: str,
    state: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Spotify OAuth callback handler.

    Args:
        code: Authorization code from Spotify
        state: CSRF state parameter
        db: Database session

    Returns:
        Redirect to frontend with token
    """
    try:
        logger.info(f"Spotify callback received with code: {code[:10]}...")

        # Exchange code for token
        auth_manager = create_oauth_manager()
        token_info = auth_manager.get_access_token(code)

        if not token_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get access token from Spotify"
            )

        logger.info("Successfully obtained access token")

        # Get user profile from Spotify
        from spotify.client import SpotifyClient
        sp = SpotifyClient(access_token=token_info["access_token"])
        spotify_user = sp.get_current_user()

        logger.info(f"Authenticated Spotify user: {spotify_user.get('id')}")

        # Check if user exists
        spotify_profile = db.query(SpotifyProfile).filter(
            SpotifyProfile.spotify_id == spotify_user["id"]
        ).first()

        if spotify_profile:
            # Update existing profile
            user = spotify_profile.user
            spotify_profile.access_token = token_info["access_token"]
            spotify_profile.refresh_token = token_info["refresh_token"]
            spotify_profile.token_expires_at = datetime.utcnow() + timedelta(
                seconds=token_info["expires_in"]
            )
            spotify_profile.display_name = spotify_user.get("display_name")
            spotify_profile.email = spotify_user.get("email")
            spotify_profile.country = spotify_user.get("country")
            spotify_profile.product = spotify_user.get("product")
            spotify_profile.followers = spotify_user.get("followers", {}).get("total")

            images = spotify_user.get("images", [])
            if images:
                spotify_profile.profile_image_url = images[0]["url"]

            user.last_login = datetime.utcnow()
        else:
            # Create new user
            user = User(
                email=spotify_user.get("email"),
                username=spotify_user.get("display_name") or spotify_user["id"],
                last_login=datetime.utcnow(),
            )
            db.add(user)
            db.flush()  # Get user.id

            # Create Spotify profile
            images = spotify_user.get("images", [])
            spotify_profile = SpotifyProfile(
                user_id=user.id,
                spotify_id=spotify_user["id"],
                display_name=spotify_user.get("display_name"),
                email=spotify_user.get("email"),
                country=spotify_user.get("country"),
                product=spotify_user.get("product"),
                followers=spotify_user.get("followers", {}).get("total"),
                profile_image_url=images[0]["url"] if images else None,
                access_token=token_info["access_token"],
                refresh_token=token_info["refresh_token"],
                token_expires_at=datetime.utcnow() + timedelta(
                    seconds=token_info["expires_in"]
                ),
                scope=token_info.get("scope"),
            )
            db.add(spotify_profile)

        db.commit()

        logger.info(f"User authenticated: {user.id}")

        # Redirect to frontend with user ID
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        return RedirectResponse(
            url=f"{frontend_url}/auth/callback?user_id={user.id}"
        )

    except Exception as e:
        logger.error(f"OAuth callback error: {e}", exc_info=True)
        db.rollback()

        # Return user to frontend with error
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        return RedirectResponse(
            url=f"{frontend_url}/?error=auth_failed&message={str(e)}"
        )


@router.post("/spotify/refresh")
async def refresh_token(
    user_id: str,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Refresh Spotify access token.

    Args:
        user_id: User UUID
        db: Database session

    Returns:
        New access token
    """
    spotify_profile = db.query(SpotifyProfile).filter(
        SpotifyProfile.user_id == user_id
    ).first()

    if not spotify_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Spotify profile not found"
        )

    try:
        # Refresh token
        auth_manager = create_oauth_manager()
        token_info = auth_manager.refresh_access_token(spotify_profile.refresh_token)

        # Update profile
        spotify_profile.access_token = token_info["access_token"]
        spotify_profile.token_expires_at = datetime.utcnow() + timedelta(
            seconds=token_info["expires_in"]
        )
        if "refresh_token" in token_info:
            spotify_profile.refresh_token = token_info["refresh_token"]

        db.commit()

        return TokenResponse(
            access_token=token_info["access_token"],
            user_id=str(user_id)
        )

    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )
