import praw
from typing import List, Dict, Any
import datetime
from app.core.config import settings
from app.models.schemas import Post, SearchResponse
from app.utils.text_cleaner import text_cleaner
import concurrent.futures
from app.services.sentiment import sentiment_analysis
from app.services.analytics import compute_metrics

# Inicializar Reddit API
reddit = praw.Reddit(
    client_id=settings.reddit_client_id,
    client_secret=settings.reddit_client_secret,
    user_agent=settings.reddit_user_agent,
)

# Buscar posts en Reddit
def search_posts(query: str, sort: str, limit: int = 25) -> SearchResponse:

    # Validar parámetros
    if sort not in ["new", "hot", "top", "relevant"]:
        raise ValueError("Ordenación inválida. Elije entre 'new', 'hot', 'top' or 'relevant'.")

    # Consulta a Reddit
    search_results = reddit.subreddit("all").search(query, sort=sort, limit=25)

    post = [post for post in search_results]
    
    def process_post(post):
        
        try:
            
            created_time = datetime.datetime.fromtimestamp(post.created_utc)

            #Contenido multimedia del post
            media_url = None
            if post.is_video:
                if post.media and 'reddit_video' in post.media:
                    media_url = post.media['reddit_video']['fallback_url']
            elif hasattr(post, 'is_gallery') and post.is_gallery:
                media_url = 'gallery'
            elif post.url.endswith(('jpg', 'jpeg', 'png', 'gif')):
                media_url = post.url
            
            posts_comments: List[Dict[str, Any]] = []
    
            try:
                post.comment_sort = 'best'
                post.comments.replace_more(limit=0)
                
                for top_level_comment in post.comments.list()[:10]:
                    
                    if hasattr(top_level_comment, 'body') and top_level_comment.body:
                        clean_comment = text_cleaner(top_level_comment.body[:500])
                        sent = sentiment_analysis(clean_comment)
                        posts_comments.append({
                            "karma": top_level_comment.score,
                            "text": clean_comment,
                            "url": f"https://www.reddit.com{top_level_comment.permalink}",
                            "sentiment_label": sent["label"],
                            "sentiment_score": sent["score"]
                        })
                    
            except Exception as e:
                print(f"Error cargando comentarios para post {post.id}: {e}")
            
            return Post(
                id=post.id,
                title=post.title,
                url=f"https://www.reddit.com{post.permalink}",
                subreddit=post.subreddit.display_name,
                date=created_time.strftime('%Y-%m-%d %H:%M:%S'),
                karma=post.score,
                upvote_ratio=post.upvote_ratio,
                flair=post.link_flair_text if post.link_flair_text else None,
                media_url=media_url,
                num_comments=post.num_comments,
                comments=posts_comments
            )

        except Exception as e:
            print(f"Error procesando el post {post.id}: {e}")
            return None
            
    processed_posts_results = []
    
    # Usar ThreadPoolExecutor para procesar los posts en paralelo
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        processed_posts_results = list(executor.map(process_post, post))
        
    final_posts = [p for p in processed_posts_results if p is not None]
    
    return SearchResponse(
        query=query,
        count=len(final_posts),
        sort=sort,
        posts=final_posts
    )