from app.database.db import REDIS, LOGGING_PREFIX
import logging

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.crud")

def create(key, value):
    LOGGER.info(f"Creating key / value pair: {key}.")
    response = REDIS.set(key, value)
    return response

def read(key):
    LOGGER.info(f"Reading key / value pair: {key}.")
    response = REDIS.get(key)
    return response

def update(key, value):
    LOGGER.info(f"Updating key / value pair: {key}.")
    response = REDIS.set(key, value)
    return response

def delete(key):
    LOGGER.info(f"Deleting key / value pair: {key}.")
    response = REDIS.delete(key)
    if response == 1:
        return True
    else:
        return False