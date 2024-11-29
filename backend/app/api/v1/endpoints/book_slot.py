import logging
from fastapi import APIRouter, Body, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.booking_service import AvailabilityService, BookingService
from app.models.booking import BookingDB
from app.models.slot import SlotDB
from app.services.db_interface import DatabaseService
from app.dependencies import get_db  # Import the get_db from dependencies
from typing import Dict, List
from datetime import datetime
from fastapi.encoders import jsonable_encoder
logger = logging.getLogger(__name__)

from app.services.redis_cache_service import RedisCacheService
from app.services.slot_service import SlotService

from pydantic import BaseModel

class AvailabilityResponse(BaseModel):
    time: str
    available_tables: int

router = APIRouter()

def get_cache_service() -> RedisCacheService:
    """Provide an instance of RedisCacheService."""
    return RedisCacheService()

@router.post("/book_table")
async def book_table(
    booking: dict = Body(...),
    db: Session = Depends(get_db), 
    redis_cache = Depends(get_cache_service)

):
    """Book a table for a entity."""
    booking_service = BookingService(db, redis_cache)
    logger.debug(booking)
    try:
        # Call the booking service to create the booking
        booking = booking_service.create_booking(booking)
        return {"message": "Booking successful!", "booking_id": booking.id}
    except HTTPException as e:
        raise e  # Re-raise the HTTPException with status code and details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_bookings/{entity_id}", response_model=List[dict])
async def get_bookings(entity_id: int, db: Session = Depends(get_db)):
    """Get all bookings for a entity."""
    booking_service = BookingService(db)

    # Retrieve all bookings for the given entity
    bookings = booking_service.get_all_bookings(entity_id)

    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this entity")

    return bookings

@router.get("/get_slots/{entity_id}", response_model=List[dict])
async def get_slots(entity_id: int, db: Session = Depends(get_db)):
    """Get all slots for a entity."""
    slot_service = SlotService(db)
    
    # Retrieve all slots for the given entity
    slots = slot_service.get_all_slots(entity_id)
    if not slots:
        raise HTTPException(status_code=404, detail="No slots found for this entity")
    
    return slots

@router.get("/availability/{entity_id}", response_model=List[AvailabilityResponse])
def get_availability(
    entity_id: int, 
    date: str, 
    db: Session = Depends(get_db), 
    redis_cache = Depends(get_cache_service)
):
    """Get availability for an entity on a given date."""
    service = AvailabilityService(db, redis_cache)
    try:
        response= service.get_availability(entity_id, date)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
