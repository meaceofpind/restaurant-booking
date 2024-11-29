import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.v1.endpoints import manage_slots, register_entity, book_slot, redis_check, search
from app.init__db import init_db
from app.services.db_client import SQLAlchemyDatabaseService
from app.services.redis_cache_service import RedisCacheService
from app.services.entity_service import EntityService
import logging
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# Include the routers
app.include_router(register_entity.router, prefix="/api/v1")
app.include_router(book_slot.router, prefix="/api/v1")
app.include_router(manage_slots.router, prefix="/api/v1")
app.include_router(redis_check.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
cache_service = RedisCacheService()
db_service = SQLAlchemyDatabaseService()
init_db()

port = int(os.getenv("PORT", 8000))


# Custom error handling for request validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"Validation Error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"message": "Validation Error", "errors": exc.errors()},
    )

# Custom error handling for general HTTP exceptions
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logging.error(f"HTTP Error: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": f"HTTP Error: {exc.detail}"},
    )

# Create the entityService, passing in the concrete services
entity_service = EntityService(db_service, cache_service)

@app.get("/")
def read_root():
    return {"message": "Welcome to the entity booking system!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)