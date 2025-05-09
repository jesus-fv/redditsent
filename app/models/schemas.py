from pydantic import BaseModel
from typing import List, Optional
class RedditPost(BaseModel):
    id: str
    title: str
    subreddit: str
    url: str
    text: str
    score: int
    comments: int
    date: str

class SearchResponse(BaseModel):
    query: str
    count: int
    subreddit: Optional[str] = None
    sort: str
    posts: List[RedditPost]