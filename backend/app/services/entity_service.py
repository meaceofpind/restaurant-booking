from app.services.redis_interface import CacheService
from app.services.db_interface import DatabaseService
from app.models.entity import EntityDB
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class EntityService:
    def __init__(self, db_service: DatabaseService, cache_service: CacheService):
        self.db_service = db_service
        self.cache_service = cache_service

    def store_entity_data_in_redis(self, entity_data: List[dict]) -> None:
        """Store entity data in Redis cache"""
        self.cache_service.set_data("entities", entity_data)

    def get_all_entities_from_redis(self) -> List[dict]:
        """Retrieve all entity data from Redis cache"""
        entities_data = self.cache_service.get_data("entities")
        if not entities_data:
            return []
        return entities_data

    def get_all_entities_from_db(self, db: Session) -> List[dict]:
        """Retrieve all entities from the database"""
        db_entities = self.db_service.get_entities(db)
        return [entity_to_dict(r) for r in db_entities]

    def get_entity(self, db: Session, entity_name: str) -> Optional[dict]:
        """Retrieve a entity by ID"""
        db_entity = self.db_service.get_entity_by_name(db, entity_name)
        if db_entity:
            return entity_to_dict(db_entity)  # Convert SQLAlchemy model to dict
        return None

    def add_entity(self, db: Session, entity: dict) -> EntityDB:
        """Add a new entity to the database"""
        entity_db = EntityDB(**entity)  # Using the SQLAlchemy model directly
        db_entity = self.db_service.add_entity(db, entity_db)
        return db_entity

    def register_entity(self, db: Session, entity_data: dict) -> dict:
        """Register a new entity (add to DB and cache)"""
        existing_entity = self.get_entity(db, entity_data["name"])
        if existing_entity:
            raise ValueError("Entity with this Name already exists.")
        
        # Add entity to DB
        new_entity = self.add_entity(db, entity_data)

        # Cache entity data for fast access
        self.store_entity_data_in_redis([entity_to_dict(new_entity)])

        return entity_to_dict(new_entity)


def entity_to_dict(entity: EntityDB) -> dict:
    """Helper function to convert SQLAlchemy model to a dictionary"""
    return {
        'id': entity.id,
        'name': entity.name,
        'city': entity.city,
        'area': entity.area,
        'cuisine': entity.cuisine,
        'rating': entity.rating,
        'cost_for_two': entity.cost_for_two,
        'is_veg_friendly': entity.is_veg_friendly,
        'number_of_tables': entity.number_of_tables,
        'max_people_per_table': entity.max_people_per_table,
    }
