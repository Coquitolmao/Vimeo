from fastapi import APIRouter, Depends, Query, UploadFile, File, Response
from fastapi.responses import RedirectResponse
from typing import Literal
from app.services.vimeo_client import VimeoClient
from app.schemas.video import VideoList, PlayVideoResponse, UploadResponse

router = APIRouter()

def get_vimeo_client() -> VimeoClient:

    return VimeoClient()

@router.get("/", response_model=VideoList)
async def list_videos(
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    sort: Literal["date", "alphabetical", "duration", "last_user_action"] = Query(None),
    client: VimeoClient = Depends(get_vimeo_client)
):
    """
    List all videos from the authenticated user's account.
    """
    return await client.get_videos(page=page, per_page=per_page, sort=sort)

@router.get("/search", response_model=VideoList)
async def search_videos(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    per_page: int = Query(25, ge=1, le=100),
    client: VimeoClient = Depends(get_vimeo_client)
):