from app.services.analytics import compute_metrics
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Annotated

from app.services.search import search_posts
from app.models.schemas import SearchResponse

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
async def search_reddit(
    query: Annotated[str, Query(min_length=1, description="Tema sobre el que buscar")],
    sort: Optional[str] = Query("hot", enum=["new", "hot", "top", "relevant"]),
):
    """
    Búsqueda de publicaciones en Reddit según una consulta y tipo de orden.
    """
    
    try:
        
        response = search_posts(query, sort)
        posts = [p.dict() for p in response.posts]
        response_with_metrics = compute_metrics(posts, query, sort)
        
        return response_with_metrics
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))