from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Post(BaseModel):
    id: str
    title: str
    url: str
    subreddit: str
    date: Optional[str] = None
    karma: int
    upvote_ratio: Optional[float] = None
    flair: Optional[str] = None
    media_url: Optional[str] = None
    num_comments: int
    comments: List[Dict[str, Any]]

class SentimentSummary(BaseModel):
    counts: Dict[str, int]
    percentages: Dict[str, float]
    dominant: str


class PostMetrics(BaseModel):
    id: str
    title: str
    url: str
    subreddit: str
    score: int
    num_comments: int
    sentiments: SentimentSummary


class SubredditMetrics(BaseModel):
    subreddit: str
    sentiments: SentimentSummary
    posts: List[PostMetrics]

class SearchResponseMetrics(BaseModel):
    query: str
    total_posts: int
    total_comments: int
    global_sentiments: SentimentSummary
    subreddits: List[SubredditMetrics]
    
class SearchResponse(BaseModel):
    query: str
    count: int
    sort: str
    posts: List[Post]