from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from app.models.entity import EntityDB
from app.services.search_service import SearchService
from app.services.redis_cache_service import RedisCacheService
from app.dependencies import get_db 
import json

router = APIRouter()

@router.post("/search")
async def search(
    filters: Dict[str, Any],  # Filters will come in the request body as a dictionary
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    redis_client = Depends(RedisCacheService)  # Assuming Redis client dependency
):
    """Search for restaurants with dynamic filters from the request body."""

    search_filters = {}

    if 'name' in filters:
        search_filters["name"] = filters["name"]
    if 'city' in filters:
        search_filters["city"] = filters["city"]
    if 'area' in filters:
        search_filters["area"] = filters["area"]
    if 'cuisine' in filters:
        search_filters["cuisine"] = filters["cuisine"]
    if 'rating_min' in filters and 'rating_max' in filters:
        search_filters["rating"] = {"min": filters["rating_min"], "max": filters["rating_max"]}
    elif 'rating_min' in filters:
        search_filters["rating"] = {"min": filters["rating_min"]}
    elif 'rating_max' in filters:
        search_filters["rating"] = {"max": filters["rating_max"]}
    
    if 'cost_for_two_min' in filters and 'cost_for_two_max' in filters:
        search_filters["cost_for_two"] = {"min": filters["cost_for_two_min"], "max": filters["cost_for_two_max"]}
    elif 'cost_for_two_min' in filters:
        search_filters["cost_for_two"] = {"min": filters["cost_for_two_min"]}
    elif 'cost_for_two_max' in filters:
        search_filters["cost_for_two"] = {"max": filters["cost_for_two_max"]}

    if 'plain_text' in filters:
        search_filters["plain_text"] = filters["plain_text"]

    # Instantiate the search service with the model class and db session
    search_service = SearchService(db, model_class=EntityDB)  # Assuming EntityDB is your model class
    # Check Redis cache (if applicable)
    cache_key = f"search:{frozenset(filters.items())}:{page}:{page_size}"
    cached_result = redis_client.get_data(cache_key)
    if cached_result:
        return cached_result

    # Perform the search using the updated search service
    try:
        search_result = search_service.search(filters, page, page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching restaurants: {str(e)}")
    
    search_result_dict = [restaurant.to_dict() for restaurant in search_result]

    # Cache the results
    redis_client.set_data(cache_key, search_result_dict)

    return search_result_dict
