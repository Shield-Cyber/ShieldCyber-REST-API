from typing import Any
from .xml import XMLResponse

class ErrorResponse(XMLResponse):

    def render(self, content: Any) -> bytes:
        self.status_code = 500
        resp_content = f'<error_response status="500" status_text="{content}"/>'
        return super().render(resp_content)