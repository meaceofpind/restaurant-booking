from sqlalchemy import Column, Integer, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class SlotDB(Base):  # Changed class name to SlotDB for consistency with SQLAlchemy model naming
    __tablename__ = 'slots'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    entity_id = Column(Integer, ForeignKey('entities.id'))
    start_time= Column(Time) 
    end_time= Column(Time)
    number_of_days = Column(Integer, default=0)

    entity = relationship("EntityDB", back_populates="slots")
    bookings = relationship("BookingDB", back_populates="slots")