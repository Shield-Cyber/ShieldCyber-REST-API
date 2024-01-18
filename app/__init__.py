import os

# Required Env Variables
PROD = None
USERNAME = os.getenv("USERNAME")

# Check Prod Env Var
CHECK_PROD = os.getenv("PROD")
try:
    if CHECK_PROD.lower() != "true":
        PROD = False
    else:
        PROD = True
except Exception:
    PROD = False

# Optional Env Variables
if os.getenv("PASSWORD") != None:
    PASSWORD = os.getenv("PASSWORD")
else:
    PASSWORD = "admin"

if os.getenv("VERSION") != None:
    VERSION = os.getenv("VERSION")
else:
    VERSION = '0.0.0'

if os.getenv("DB_HOST") != None:
    DB_HOST = os.getenv("DB_HOST")
else:
    DB_HOST = 'redis-db'

if os.getenv("DB_PORT") != None:
    DB_PORT = os.getenv("DB_PORT")
else:
    DB_PORT = 6379

DESCRIPTION = """This is a translation API that calls the XML API calls on the local
Greenbone Vulnerability Scanner and converts them to REST API calls for easier use by most systems."""

LOGGING_PREFIX = "api"