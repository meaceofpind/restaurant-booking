from sqlalchemy import Column, Date, Integer, ForeignKey, DateTime, String, Time
from sqlalchemy.orm import relationship
from app.database import Base

class BookingDB(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    entity_id = Column(Integer, ForeignKey('entities.id'))
    slot_id = Column(Integer, ForeignKey('slots.id'))
    num_people = Column(Integer)
    booking_time = Column(Time)
    booking_date = Column(Date)
    booking_name = Column(String)  
    booking_contact = Column(String) 
    slot_time = Column(DateTime) 

    # Relationships to other models
    entity = relationship("EntityDB", back_populates="bookings")
    slots = relationship("SlotDB", back_populates="bookings")
