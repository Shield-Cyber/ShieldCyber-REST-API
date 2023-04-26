import os

VERSION = os.getenv("VERSION")

DESCRIPTION = """This is a translation API that calls the XML API calls on the local
Greenbone Vulnerability Scanner and converts them to REST API calls for easier use by most systems."""

LOGGING_PREFIX = "api"