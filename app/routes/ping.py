from fastapi import APIRouter, Response
from app import LOGGING_PREFIX
import logging

ENDPOINT = "ping"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT]
    )

### ROUTES ###

@ROUTER.get("")
def get_ping():
    return Response(content="<response>pong</response>", media_type="application/xml")