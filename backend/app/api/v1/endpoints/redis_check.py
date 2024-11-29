from fastapi import APIRouter, HTTPException
from app.services.redis_client import check_redis_connection, get_redis_client

router = APIRouter()

# Route to check Redis connection
@router.get("/redis/health", tags=["Health Check"])
async def redis_health_check():
    try:
        redis_client = get_redis_client()
        if redis_client.ping():
            return {"status": "healthy"}
        else:
            raise HTTPException(status_code=503, detail="Redis is not responding")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))