import logging
from app.models.booking import BookingDB
from app.models.entity import EntityDB
from app.models.slot import SlotDB
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, List
from fastapi import HTTPException
from app.services.redis_cache_service import RedisCacheService
from app.services.redis_client import get_redis_client
from redlock import Redlock
logger = logging.getLogger(__name__)

class BookingService:
    def __init__(self, db: Session, redis_cache: RedisCacheService):
        self.db = db
        self.redis_client = get_redis_client()
        self.redlock = Redlock([self.redis_client])
        self.redis_cache = redis_cache

    def create_booking(self, booking_data: dict) -> BookingDB:
        """Create a booking for a user with name and contact details."""
        slot_id = booking_data["slot_id"]
        entity_id = booking_data["entity_id"]
        
        # Lock key to ensure only one booking can be created for a given slot
        lock_key = f"booking_lock_{entity_id}_{slot_id}"
        lock = self.redlock.lock(lock_key, 10000)  # Lock for 10 seconds (can adjust time)

        if not lock:
            raise HTTPException(status_code=409, detail="Booking is currently being processed. Please try again.")

        try:
            # First, check if the slot is available
            slot = self.db.query(SlotDB).filter(SlotDB.id == slot_id, SlotDB.entity_id == entity_id).first()

            if not slot:
                raise HTTPException(status_code=404, detail="Slot not found")

            # Check if the slot is already booked
            bookings_for_slot = self.db.query(BookingDB).filter(BookingDB.slot_id == slot_id, BookingDB.entity_id == entity_id).all()

            # Retrieve entity to check table availability
            entity = self.db.query(EntityDB).filter(EntityDB.id == entity_id).first()
            if not entity:
                raise HTTPException(status_code=404, detail="Entity not found")

            # Validate number of people does not exceed max number of people per table
            if int(booking_data["people_count"]) > entity.max_people_per_table:
                raise HTTPException(status_code=400, detail=f"Cannot book for more than {entity.max_people_per_table} people per table")

            # Check if there are available tables for the slot
            if len(bookings_for_slot) >= entity.number_of_tables:
                raise HTTPException(status_code=400, detail="No available tables for this slot")

            # Proceed to create the booking
            booking = BookingDB(
                entity_id=entity_id,
                slot_id=slot_id,
                num_people=booking_data["people_count"],
                booking_name=booking_data["booking_name"],
                booking_contact=booking_data["booking_contact"],
                booking_time=datetime.strptime(booking_data["booking_time"], '%H:%M').time(),
                booking_date=datetime.strptime(booking_data["booking_date"], '%Y-%m-%d').date()
            )

            # Add the booking to the database
            self.db.add(booking)
            self.db.commit()
            self.db.refresh(booking)
            self.redis_cache.clear_cache()
            return booking

        finally:
            # Always release the lock, whether the operation was successful or not
            self.redlock.unlock(lock)

    def get_all_bookings(self, entity_id: int) -> List[dict]:
        """Retrieve all bookings for a given entity."""
        bookings = self.db.query(BookingDB).filter(BookingDB.entity_id == entity_id).all()
        # Return the bookings as a list of dictionaries using the to_dict helper
        return [self.to_dict(booking) for booking in bookings]

    def to_dict(self, booking: BookingDB) -> dict:
        """Convert a BookingDB instance to a dictionary."""
        return {
            "id": booking.id,
            "entity_id": booking.entity_id,
            "slot_id": booking.slot_id,
            "num_people": booking.num_people,
            "booking_name": booking.booking_name,
            "booking_contact": booking.booking_contact,
            "booking_time": booking.booking_time,
            "booking_date": booking.booking_date
        }

    def cancel_booking(self, booking_id: int) -> None:
        """Cancel a booking and free up the slot."""
        booking = self.db.query(BookingDB).filter(BookingDB.id == booking_id).first()

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        # Find the slot associated with the booking and mark it as available
        slot = self.db.query(SlotDB).filter(SlotDB.id == booking.slot_id).first()
        if slot:
            slot.is_booked = False

        self.db.delete(booking)
        self.db.commit()


class AvailabilityService:
    def __init__(self, db: Session, redis_cache: RedisCacheService):
        self.db = db
        self.redis_cache = redis_cache

    def get_availability(self, entity_id: int, date: str) -> List[Dict[str, int]]:
        """Get hourly availability for a specific entity on a given date."""
        # Validate date format
        try:
            booking_date = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")        

        # Fetch entity and slot details
        entity = self.db.query(EntityDB).filter(EntityDB.id == entity_id).first()
        if not entity:
            raise ValueError("Entity not found")
        

        slot = self.db.query(SlotDB).filter(SlotDB.entity_id == entity_id).first()
        if not slot:
            raise ValueError("Slot not found")
        
        # Calculate hourly periods
        start_time = datetime.combine(booking_date, slot.start_time)
        end_time = datetime.combine(booking_date, slot.end_time)

        periods = []
        while start_time <= end_time:
            periods.append(start_time.time())
            start_time += timedelta(hours=1)
        # Check bookings for each period
        availability = []
        for period in periods:
            num_bookings = self.db.query(BookingDB).filter(
                BookingDB.entity_id == entity_id,
                BookingDB.booking_date == booking_date,
                BookingDB.booking_time == period,
            ).count()
            logger.debug(self.db.query(BookingDB).filter(
                BookingDB.entity_id == entity_id,
                BookingDB.booking_date == booking_date,
                BookingDB.booking_time == period,
            ))
            logger.debug(period)
            available_tables = entity.number_of_tables - num_bookings
            availability.append({"time": period.strftime("%H:%M"), "available_tables": max(0, available_tables)})

        # Cache the availability
        return availability