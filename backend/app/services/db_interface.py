from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.entity import EntityDB
from app.models.slot import SlotDB
from sqlalchemy.orm import Session

class DatabaseService(ABC):
    @abstractmethod
    def get_entities(self, db: Session) -> List[EntityDB]:
        """Retrieve all entities from the database"""
        pass

    @abstractmethod
    def get_entity_by_name(self, db: Session, entity_id: int) -> Optional[EntityDB]:
        """Retrieve a single entity by ID"""
        pass

    @abstractmethod
    def add_entity(self, db: Session, entity: EntityDB) -> EntityDB:
        """Add a new entity to the database"""
        pass

    @abstractmethod
    def add_slot(self, db: Session, slot: SlotDB) -> SlotDB:
        """Add a new slot to the database"""
        pass
