import redis
from app import DB_HOST, DB_PORT
from app.database import LOGGING_PREFIX
import logging

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.db")

LOGGER.info("Connecting to Redis service...")
REDIS = redis.Redis(host=DB_HOST, port=DB_PORT)
LOGGER.info("Connected to Redis service.")