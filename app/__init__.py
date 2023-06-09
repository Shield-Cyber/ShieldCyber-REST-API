import os

if os.getenv("USERNAME") != None:
    USERNAME = os.getenv("USERNAME")
else:
    USERNAME = "admin"

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