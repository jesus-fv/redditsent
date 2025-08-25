from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Annotated

from app.services.search import search_posts
from app.services.analytics import calculate_distribution
from app.models.schemas import SearchResponse

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/", response_model=SearchResponse)
async def search_reddit(
    query: Annotated[str, Query(min_length=1, description="Tema sobre el que buscar")],
    sort: Optional[str] = Query("hot", enum=["new", "hot", "top", "relevant"]),
):
    """
    Búsqueda de publicaciones en Reddit según una consulta y tipo de orden.
    """
    
    try:
        response = search_posts(query, sort)
        calculate_distribution(response)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))