from fastapi import HTTPException, APIRouter
from loguru import logger
from pydantic import BaseModel

from api.dependencies import SpotifyAuthServiceDependency
from api.models.models import TokenData
from api.services.music.spotify_auth_service import SpotifyAuthServiceException

router = APIRouter()


class RefreshRequest(BaseModel):
    refresh_token: str


@router.post("/tokens/refresh", response_model=TokenData)
async def refresh_tokens(refresh_request: RefreshRequest, spotify_auth_service: SpotifyAuthServiceDependency) -> TokenData:
    try:
        tokens = await spotify_auth_service.refresh_tokens(refresh_request.refresh_token)
        return tokens
    except SpotifyAuthServiceException as e:
        logger.error(f"Failed to refresh tokens from refresh_token: {refresh_request.refresh_token} - {e}")
        raise HTTPException(status_code=401, detail="Invalid refresh token.")
