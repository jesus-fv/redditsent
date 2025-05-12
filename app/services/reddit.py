import praw
from typing import List
import datetime
from app.core.config import settings
from app.models.schemas import RedditPost, SearchResponse
from app.utils.text_cleaner import text_cleaner

reddit = praw.Reddit(
    client_id=settings.reddit_client_id,
    client_secret=settings.reddit_client_secret,
    user_agent=settings.reddit_user_agent,
)

def search_posts(query: str, sort: str = "new", limit: int = 15) -> SearchResponse:
    
    if sort not in ["new", "hot", "top", "relevant"]:
        raise ValueError("Invalid sort type. Choose from 'new', 'hot', 'top' or 'relevant'.")
        
    # Perform the search    
    search_results = reddit.subreddit("all").search(query, sort=sort, limit=limit * 5)
    
    posts: List[RedditPost] = []
    for post in search_results:
        
        if not post.is_self or not post.selftext.strip():
            continue
        
        # Convertir timestamp a datetime legible
        created_time = datetime.datetime.fromtimestamp(post.created_utc)

        clean_text = text_cleaner(post.selftext)
        
        posts.append(RedditPost(
            id=post.id,
            title=post.title,
            subreddit=post.subreddit.display_name,
            url=f"https://www.reddit.com{post.permalink}",
            score=post.score,
            comments=post.num_comments,
            date=created_time.strftime('%Y-%m-%d %H:%M:%S'),
            text=clean_text[:500]  # Limitar a 1000 caracteres,
        ))
        
        if len(posts) == limit:
            break
    
    # Construir respuesta
    return SearchResponse(
        query=query,
        count=len(posts),
        sort=sort,
        posts=posts
    )
