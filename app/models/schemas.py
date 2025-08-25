from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class RedditPost(BaseModel):
    id: str
    title: str
    text: str
    score: int
    date: str
    comments: List[Dict[str, Any]]

class SearchResponse(BaseModel):
    query: str
    count: int
    sort: str
    posts: List[RedditPost]