from typing import List, Optional
from app.services.db_interface import DatabaseService
from app.models.entity import EntityDB
from app.models.slot import SlotDB
from sqlalchemy.orm import Session

class SQLAlchemyDatabaseService(DatabaseService):
    def get_entities(self, db: Session) -> List[EntityDB]:
        """Retrieve all entities from the database"""
        return db.query(EntityDB).all()

    def get_entity_by_name(self, db: Session, entity_name: str) -> Optional[EntityDB]:
        """Retrieve a entity by ID"""
        return db.query(EntityDB).filter(EntityDB.name == entity_name).first()

    def add_entity(self, db: Session, entity: EntityDB) -> EntityDB:
        """Add a new entity to the database"""
        db.add(entity)
        db.commit()
        db.refresh(entity)
        return entity

    def add_slot(self, db: Session, slot: SlotDB) -> SlotDB:
        """Add a new slot to the database"""
        db.add(slot)
        db.commit()
        db.refresh(slot)
        return slot
