from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class RedditPost(BaseModel):
    id: str
    title: str
    subreddit: str
    url: str
    text: str
    score: int
    comments: List[Dict[str, Any]]
    date: str

class SearchResponse(BaseModel):
    query: str
    count: int
    subreddit: Optional[str] = None
    sort: str
    posts: List[RedditPost]