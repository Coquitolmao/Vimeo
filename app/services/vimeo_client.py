import logging
import httpx
from fastapi import HTTPException, status
from app.core.config import settings
from typing import Optional, Dict, Any, BinaryIO
from app.schemas.video import Video, VideoList, UploadResponse

logger = logging.getLogger(__name__)

class VimeoClient:
    def __init__(self):
        self.base_url = settings.VIMEO_BASE_URL
        self.headers = {
            "Authorization": f"bearer {settings.VIMEO_ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.vimeo.*+json;version=3.4"
        }

    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Internal wrapper for httpx requests with error handling.
        """
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.request(method, url, headers=self.headers, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"Vimeo API Error: {e.response.text}")
                status_code = e.response.status_code
                detail = f"Vimeo API Error: {e.response.text}"
                
                if status_code == 401:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Vimeo Token")
                elif status_code == 403:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission Denied")
                elif status_code == 404:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")
                elif status_code == 429:
                    raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate Limit Exceeded")
                else:
                    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)
            except httpx.RequestError as e:
                logger.error(f"Request Error: {str(e)}")
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service Unavailable")

    def _normalize_video(self, data: Dict[str, Any]) -> Video:
        """
        Extracts relevant fields from Vimeo response to match Video schema.
        """
        # ID is usually at the end of the URI, e.g., /videos/12345
        video_id = data.get("uri", "").split("/")[-1]
        
        # Embed HTML might be in 'embed'['html']
        embed_html = data.get("embed", {}).get("html")


        return Video(
            id=video_id,
            name=data.get("name", "Untitled"),
            description=data.get("description"),
            duration=data.get("duration", 0),
            link=data.get("link", ""),
            embed_html=embed_html,
            pictures=data.get("pictures")
        )

    async def get_videos(self, page: int = 1, per_page: int = 25, sort: Optional[str] = None) -> VideoList:
        params = {"page": page, "per_page": per_page}
        if sort:
            params["sort"] = sort
        
        data = await self._request("GET", "/me/videos", params=params)
        
        videos = [self._normalize_video(v) for v in data.get("data", [])]
        return VideoList(
            data=videos,
            page=data.get("page", 1),
            per_page=data.get("per_page", 25),
            total=data.get("total", 0)
        )   
