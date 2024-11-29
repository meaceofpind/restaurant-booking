from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import time, timedelta
from app.models.slot import SlotDB
from app.services.db_client import SQLAlchemyDatabaseService
from app.services.redis_cache_service import RedisCacheService
from app.services.slot_service import SlotService
from app.services.db_interface import DatabaseService
from app.services.redis_interface import CacheService
from app.dependencies import get_db  # Dependency to get DB session
from typing import List

router = APIRouter()


def get_cache_service() -> RedisCacheService:
    """Provide an instance of RedisCacheService."""
    return RedisCacheService()
# Dependency injection for SlotService
def get_slot_service(db: Session = Depends(get_db), cache_service = Depends(RedisCacheService)) -> SlotService:
    return SlotService(db)

@router.post("/entities/{entity_id}/slots")
def add_slot(entity_id: int, start: int, end: int, number_of_days: int, db: Session = Depends(get_db), cache_service: CacheService = Depends(get_cache_service)):
    """Add or update a slot for an entity."""
    start_time = time(start,0)
    end_time = time(end,0)
    # Validate end_time should be later than start_time
    if end_time <= start_time:
        raise HTTPException(status_code=400, detail="End time must be later than start time.")

    
    slot_service = get_slot_service(db, cache_service)
    try:
        # Use the `update_slot` method to handle both creation and updates
        slot_service.update_slot(entity_id, start_time, end_time, number_of_days)
        return {"message": "Slot added or updated successfully!", "start_time": start_time, "end_time": end_time}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/entities/{entity_id}/slots")
def get_slots(entity_id: int, db: Session = Depends(get_db), cache_service: CacheService = Depends(get_cache_service)):
    """Retrieve all available slots for a given entity."""
    slot_service = get_slot_service(db, cache_service)
    slots = slot_service.get_slots(entity_id)
    
    # Return slots in dictionary format
    return slots 
