from fastapi import APIRouter
from app import LOGGING_PREFIX
from app.utils.xml import XMLResponse
import logging

ENDPOINT = "ping"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT],
    default_response_class=XMLResponse
    )

### ROUTES ###

@ROUTER.get("")
def get_ping():
    return '<ping_response status="200" status_text="pong"/>'