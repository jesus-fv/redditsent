
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Post(BaseModel):
    id: str
    title: str
    author: Optional[str] = None
    url: str
    subreddit: str
    date: Optional[str] = None
    karma: int
    upvote_ratio: Optional[float] = None
    flair: Optional[str] = None
    media_url: Optional[str] = None
    num_comments: int
    comments: List[Dict[str, Any]]


class SearchResponse(BaseModel):
    query: str
    count: int
    sort: str
    posts: List[Post]
