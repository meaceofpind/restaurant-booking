from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Pydantic model for BookingDB
class BookingResponse(BaseModel):
    id: int
    restaurant_id: int
    slot_id: int
    num_people: int
    booking_name: str
    booking_contact: str
    booking_time: datetime
    booking_date: datetime

    class Config:
        orm_mode = True  # This tells Pydantic to work with SQLAlchemy models

# Pydantic model for RestaurantDB
class RestaurantResponse(BaseModel):
    id: int
    name: str
    city: str
    area: str
    cuisine: str
    rating: Optional[float] = None
    cost_for_two: Optional[float] = None
    is_veg_friendly: bool
    number_of_tables: int
    max_people_per_table: int
    slots: List['SlotResponse'] = []  # Define SlotResponse for related slots
    bookings: List[BookingResponse] = []  # Define BookingResponse for related bookings

    class Config:
        orm_mode = True

# Pydantic model for SlotDB
class SlotResponse(BaseModel):
    id: int
    restaurant_id: int
    slot_time: datetime
    is_booked: bool

    class Config:
        orm_mode = True

# Update the forward reference for circular relationship between SlotResponse and RestaurantResponse
RestaurantResponse.update_forward_refs()

