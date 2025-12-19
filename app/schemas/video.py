from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field

class Picture(BaseModel):
    active: bool
    type: str
    sizes: List[dict]
    resource_key: str

class VideoList(BaseModel):
    data: List[Video]
    page: int
    per_page: int
    total: int