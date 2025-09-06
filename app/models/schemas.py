from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Post(BaseModel):
    id: str
    title: str
    url: str
    subreddit: str
    date: str
    karma: int
    upvote_ratio: float
    flair:str
    media_url:str
    num_comments: int
    comments: List[Dict[str, Any]]

class SearchResponse(BaseModel):
    query: str
    count: int
    sort: str
    posts: List[Post]