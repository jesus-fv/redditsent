import praw
from typing import List
import datetime
from app.core.config import settings
from app.models.schemas import RedditPost, SearchResponse
from app.utils.text_cleaner import text_cleaner
import asyncio
import concurrent.futures

reddit = praw.Reddit(
    client_id=settings.reddit_client_id,
    client_secret=settings.reddit_client_secret,
    user_agent=settings.reddit_user_agent,
)

# Buscar posts en Reddit
# @app.get("/reddit/search", response_model=SearchResponse)
def search_posts(query: str, sort: str, limit: int = 15) -> SearchResponse:
    
    if sort not in ["new", "hot", "top", "relevant"]:
        raise ValueError("Ordenación inválida. Elije entre 'new', 'hot', 'top' or 'relevant'.")

    search_results = reddit.subreddit("all").search(query, sort=sort, limit=25)
    post = [post for post in search_results]
    
    def process_post(post):
        try:
            created_time = datetime.datetime.fromtimestamp(post.created_utc)
            clean_text = text_cleaner(post.selftext)
            posts_comments: List[str] = []
    
            try:
                post.comments.replace_more(limit=0)
                for top_level_comment in list(post.comments)[:10]:
                    if hasattr(top_level_comment, 'body') and top_level_comment.body:
                        clean_comments = text_cleaner(top_level_comment.body[:500])
                        posts_comments.append(clean_comments)
                    
            except Exception as e:
                print(f"Error cargando comentarios para post {post.id}: {e}")
            
            return RedditPost(
                id=post.id,
                title=post.title,
                subreddit=post.subreddit.display_name,
                url=f"https://www.reddit.com{post.permalink}",
                score=post.score,
                date=created_time.strftime('%Y-%m-%d %H:%M:%S'),
                text=clean_text[:300],
                comments=posts_comments
            )
            
        except Exception as e:
            print(f"Error procesando el post {post.id}: {e}")
            return None
            
    processed_posts_results = []
    # Construir respuesta
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        processed_posts_results = list(executor.map(process_post, post))
        
    final_posts = [p for p in processed_posts_results if p is not None]
    
    return SearchResponse(
        query=query,
        count=len(final_posts),
        sort=sort,
        posts=final_posts
    )
    