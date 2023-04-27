import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from app.utils.xml import root as xml_root
import time
from app import routes as RT
from app import DESCRIPTION, LOGGING_PREFIX, VERSION

# Logging
LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    LOGGER.info(f"System Starting...")
    counter = 0
    while True:
        if counter >= 60:
            LOGGER.critical("Connection to gvmd socket took too long. Forcing system exit.")
            raise SystemExit(1)
        try:
            with Gmp(connection=UnixSocketConnection()) as gmp:
                version = xml_root(gmp.get_version())
                if version.status != 200:
                    LOGGER.critical(f"Version check recieved non-200 response. Response: {version.data}")
                    raise SystemExit(2)
                LOGGER.info(f"{version.status}, {version.status_text}. Startup complete and took {counter} second(s).")
                break
        except SystemExit:
            raise SystemExit(2)
        except:
            LOGGER.warning("Wating 1 second for gvmd socket.")
            time.sleep(1)
            counter += 1
    yield
    LOGGER.info("System shutting down...")

# Main App / API
app = FastAPI(
    title="Greenbone Rest API",
    description=DESCRIPTION,
    version=VERSION,
    swagger_ui_parameters={"tagsSorter": "alpha", "operationsSorter": "alpha"},
    lifespan=lifespan
)

app.include_router(RT.AUTHENTICATION)
app.include_router(RT.VERSION)
app.include_router(RT.SCANNER)
app.include_router(RT.REPORT)
app.include_router(RT.TARGET)
app.include_router(RT.FEED)
app.include_router(RT.PORT)
app.include_router(RT.SCAN)
app.include_router(RT.USER)
app.include_router(RT.PING)