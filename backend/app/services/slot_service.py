from datetime import time
import logging
from typing import List
from sqlalchemy.orm import Session
from app.models.slot import SlotDB
from app.services.db_interface import DatabaseService
logger = logging.getLogger(__name__)
 
class SlotService:
    def __init__(self, db: Session):  # Ensure db is of type Session
        self.db = db
    
    def update_slot(self, entity_id: int, start_time: time, end_time: time, number_of_days: int) -> None:
        """Create or update a slot for an entity."""
        # Ensure the end_time is later than start_time
        if end_time <= start_time:
            raise ValueError("End time must be greater than start time.")
        
        # Try to find an existing slot with the given ID
        slot = self.db.query(SlotDB).filter(SlotDB.entity_id == entity_id).first()
        
        if slot:
            # If the slot exists, update it with the new start_time, end_time, and number_of_days
            slot.start_time = start_time
            slot.end_time = end_time
            slot.number_of_days = number_of_days
        else:
            # If the slot doesn't exist, create a new slot
            slot = SlotDB(
                entity_id=entity_id,
                start_time=start_time,
                end_time=end_time,
                number_of_days=number_of_days
            )
            self.db.add(slot)
        
        # Commit the transaction
        self.db.commit()
        self.db.refresh(slot)

    def get_slots(self, entity_id: int) -> List[dict]:
        """Retrieve all available slots for a given entity."""
        logger.debug(self.db)
        slots = self.db.query(SlotDB).filter(SlotDB.entity_id == entity_id).all()
        if not slots:
            return [{
            "start_time": "00:00",  
            "end_time": "00:00",    
            "number_of_days": 0     
        }]
    
        return [self.slot_to_dict(slot) for slot in slots]

    def slot_to_dict(self, slot: SlotDB) -> dict:
        """Helper function to convert SlotDB to a dictionary."""
        return {
            "id": slot.id,
            "entity_id": slot.entity_id,
            "start_time": slot.start_time.strftime("%H:%M"),  # Format as HH:MM
            "end_time": slot.end_time.strftime("%H:%M"),      # Format as HH:MM
            "number_of_days": slot.number_of_days,
        }
