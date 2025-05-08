import praw
from typing import Optional
import os
import datetime
from app.core.config import settings
from app.models.schemas import RedditPost, SearchResponse

reddit = praw.Reddit(
    client_id=settings.reddit_client_id,
    client_secret=settings.reddit_client_secret,
    user_agent=settings.reddit_user_agent,
)

def search_posts(query: str, sort: str = "new"):
    
    if sort not in ["new", "hot", "top", "relevant"]:
        raise ValueError("Invalid sort type. Choose from 'new', 'hot', 'top' or 'relevant'.")
        
    # Perform the search    
    search_results = reddit.subreddit("all").search(query, sort=sort, limit=15)
    
    posts = []
    for post in search_results:
        # Convertir timestamp a datetime legible
        created_time = datetime.datetime.fromtimestamp(post.created_utc)
        
        if not post.selftext:
            continue
        
        posts.append(RedditPost(
            id=post.id,
            título=post.title,
            subreddit=post.subreddit.display_name,
            url=f"https://www.reddit.com{post.permalink}",
            puntuación=post.score,
            comentarios=post.num_comments,
            fecha=created_time.strftime('%Y-%m-%d %H:%M:%S'),
            texto=post.selftext,
        ))
    
    # Construir respuesta
    return SearchResponse(
        query=query,
        count=len(posts),
        sort=sort,
        posts=posts
    )
