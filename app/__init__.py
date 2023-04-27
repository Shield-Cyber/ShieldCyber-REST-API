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

DESCRIPTION = """This is a translation API that calls the XML API calls on the local
Greenbone Vulnerability Scanner and converts them to REST API calls for easier use by most systems."""

LOGGING_PREFIX = "api"