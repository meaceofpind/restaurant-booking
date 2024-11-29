from app.database import engine, Base  # Import Base from your database module
from app.models import entity
from app.models.entity import EntityDB 
from app.models.slot import SlotDB        # Then import SlotDB
from app.models.booking import BookingDB 

def init_db():
    from app.models import entity,slot, booking
    Base.metadata.create_all(bind=engine)
