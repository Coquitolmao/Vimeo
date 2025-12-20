from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field

class Picture(BaseModel):
    """
    Represents a picture object from Vimeo's response.
    Typically contains sizes and logic for display.
    """
    active: bool
    type: str
    sizes: List[dict]  # Simplified for brevity, contains width/height/link
    resource_key: str

class Video(BaseModel):
    """
    Standardized Video model returned to the API consumer.
    Includes only requested fields: id, name, description, duration, link, embed_html, pictures.
    """
    id: str = Field(..., description="The unique identifier of the video (extracted from URI).")
    name: str = Field(..., description="The title of the video.")
    description: Optional[str] = Field(None, description="The description of the video.")
    duration: int = Field(..., description="Duration in seconds.")
    link: HttpUrl = Field(..., description="The direct link to the video on Vimeo.")
    embed_html: Optional[str] = Field(None, description="HTML code to embed the video.")
    pictures: Optional[Picture] = Field(None, description="Active picture information.")

class VideoList(BaseModel):
    """
    Paginated list of videos.
    """
    data: List[Video]
    page: int
    per_page: int
    total: int

class PlayVideoResponse(BaseModel):
    """
    Response model for playing a video (JSON mode).
    """
    link: HttpUrl
    embed_html: Optional[str]

class UploadResponse(BaseModel):
    """
    Response after initiating or completing an upload.
    """
    video_id: str
    link: HttpUrl
    status: str