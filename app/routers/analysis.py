from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Annotated

from app.services.reddit import search_posts
from app.models.schemas import SearchResponse

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.get("/", response_model=SearchResponse)
async def search_reddit(
    query: Annotated[str, Query(min_length=1, description="Tema sobre el que buscar")],
    sort: Optional[str] = Query("relevant", enum=["new", "hot", "top", "relevant"]),
):
    """
    Búsqueda de publicaciones en Reddit según una consulta y tipo de orden.
    """
    
    try:
        response = search_posts(query, sort)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))