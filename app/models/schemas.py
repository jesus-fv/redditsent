from pydantic import BaseModel
from typing import List, Optional
class RedditPost(BaseModel):
    id: str
    título: str
    subreddit: str
    url: str
    texto: str
    puntuación: int
    comentarios: int
    fecha: str

class SearchResponse(BaseModel):
    query: str
    count: int
    subreddit: Optional[str] = None
    sort: str
    posts: List[RedditPost]