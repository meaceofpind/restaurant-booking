import logging
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.db_client import SQLAlchemyDatabaseService
from app.services.redis_cache_service import RedisCacheService
from app.services.redis_client import get_redis_client
from app.services.entity_service import EntityService
from app.models.entity import EntityDB  # Use entityDB (SQLAlchemy model)
from app.dependencies import get_db  # Assuming a dependency for DB session

router = APIRouter()
logger = logging.getLogger(__name__)

def get_cache_service() -> RedisCacheService:
    """Provide an instance of RedisCacheService."""
    return RedisCacheService()

# Dependency injection for entityService
def get_entity_service(db: Session, cache_service: RedisCacheService) -> EntityService:
    try:
        db_service = SQLAlchemyDatabaseService()
        logger.debug("Database service created successfully")
        return EntityService(db_service, cache_service)
    except Exception as e:
        logger.error(f"Error creating entity service: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/entities")
def register_entity(
    entity: dict = Body(...),  # Use dict directly instead of SQLAlchemy model
    db: Session = Depends(get_db),
    cache_service: RedisCacheService = Depends(get_cache_service)
):
    entity_service = get_entity_service(db, cache_service)
    logger.debug("Registering entity")
    try:
        registered_entity = entity_service.register_entity(db, entity)
        return {"message": "entity registered successfully!", "entity": registered_entity}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # entity ID already exists

@router.get("/entities")
async def get_entities(
    db: Session = Depends(get_db),
    cache_service: RedisCacheService = Depends(get_cache_service)
):
    entity_service = get_entity_service(db, cache_service)
    logger.debug("Fetching entities")
    entities = entity_service.get_all_entities_from_redis() or entity_service.get_all_entities_from_db(db)
    return {"entities": entities}
