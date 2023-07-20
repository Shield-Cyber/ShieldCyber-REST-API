from typing import Any
from .xml import XMLResponse
from app import LOGGING_PREFIX
import logging

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.error")

class ErrorResponse(XMLResponse):

    def render(self, content: Any) -> bytes:
        LOGGER.error(f"Response Error Caught: {content}")
        self.status_code = 500
        resp_content = f'<error_response status="500" status_text="Internal Server Error: Check Log Files"/>'
        return super().render(resp_content)