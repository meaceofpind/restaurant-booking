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
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# FastAPI app initialization
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Include the routers for your app
app.include_router(register_entity.router, prefix="/api/v1")
app.include_router(book_slot.router, prefix="/api/v1")
app.include_router(manage_slots.router, prefix="/api/v1")
app.include_router(redis_check.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")

# Initialize services
cache_service = RedisCacheService()
db_service = SQLAlchemyDatabaseService()
init_db()

# Get the frontend URL from environment variables (can also hardcode it)
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")  # Default to localhost for local dev

# Add CORSMiddleware to handle CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],  # Allow only the frontend URL or use ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

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

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the entity booking system!"}

# Run the app on the specified port
port = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
