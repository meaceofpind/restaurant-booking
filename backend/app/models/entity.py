from sqlalchemy import Column, Index, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from typing import List, Optional

# SQLAlchemy model
from app.database import Base

class EntityDB(Base): 
    __tablename__ = 'entities'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # Index on primary key
    name = Column(String, unique=True, nullable=False)  # Unique and required field
    city = Column(String, nullable=False, index=True)  # Required and indexed
    area = Column(String, nullable=False, index=True)  # Required and indexed
    cuisine = Column(String, nullable=False)
    rating = Column(Float, nullable=False, index=True)  # Required and indexed
    cost_for_two = Column(Float, nullable=False)
    is_veg_friendly = Column(Boolean, nullable=False)
    number_of_tables = Column(Integer, nullable=False)  
    max_people_per_table = Column(Integer, nullable=False)

    slots = relationship('SlotDB', back_populates="entity", cascade="all, delete-orphan")
    bookings = relationship("BookingDB", back_populates="entity")

    __table_args__ = (
        Index('ix_entity_name', 'name'),  # Index on 'name'
        Index('ix_entity_rating', 'rating'),  # Index on 'rating'
        Index('ix_entity_city', 'city'),  # Index on 'city'
        Index('ix_entity_area', 'area'),  # Index on 'area'
    )


    def to_dict(self):
        """Convert the EntityDB instance to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "area": self.area,
            "cuisine": self.cuisine,
            "rating": self.rating,
            "cost_for_two": self.cost_for_two,
            "is_veg_friendly": self.is_veg_friendly,
            "number_of_tables": self.number_of_tables,
            "max_people_per_table": self.max_people_per_table
        }