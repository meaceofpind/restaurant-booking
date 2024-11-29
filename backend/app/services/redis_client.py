import json
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import redis
from typing import List, Optional, Union
import logging

logger = logging.getLogger(__name__)
load_dotenv()

# Initialize the Redis client
def get_redis_client():
    redis_url = os.getenv('REDIS_URL')
    
    # Parse the Redis URL
    url = urlparse(redis_url)
    redis_host = url.hostname
    redis_port = url.port
    redis_password = url.password
    
    # Connect to Redis using the parsed values
    return redis.StrictRedis(
        host=redis_host,
        port=redis_port,
        db=0,
        password=redis_password,
        decode_responses=True
    )

def set_data(key: str, value: list,ttl:int = 300):
    r = get_redis_client()
    
    try:
        # Ensure value is a flat list (e.g., [1, 2, 3])
        if value and isinstance(value[0], list):  # Check if value is a list of lists
            value = [item for sublist in value for item in sublist]  # Flatten the list
        
        # Ensure that the key is compatible with list type, if not, delete it
        if r.type(key) not in ["none", "list"]:
            r.delete(key)  # Delete incompatible key
        
        # Append each item to the list (using json.dumps if necessary)
        for item in value:
            r.rpush(key, json.dumps(item))  # Push value to list
        r.expire(key, 300)  # Set TTL to 5 minutes
    except Exception as e:
        raise RuntimeError(f"Error appending data to Redis key '{key}': {str(e)}")  # Store data as a string (you can serialize it to JSON for more structured storage)

# Function to get data from Redis
def get_data(key: str) -> Optional[list]:
    r = get_redis_client()
    data = r.lrange(key, 0, -1)  # Get all elements in the list
    if data:
        return [json.loads(item) for item in data]  # Deserialize each item back to a dictionary
    return None

def clear_cache(self):
    r = get_redis_client()
    try:
        r.flushall()  # Clear the entire Redis database
        print("Redis cache cleared.")
    except Exception as e:
        raise RuntimeError(f"Error clearing Redis cache: {str(e)}")

def check_redis_connection() -> bool:
    try:
        r = get_redis_client()
        return r.ping()  # Returns True if connected successfully
    except Exception as e:
        return False  # Return False if there was an issue connecting