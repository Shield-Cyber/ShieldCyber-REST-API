from dataclasses import dataclass
import xml.etree.ElementTree as ET
import logging

LOGGER = logging.getLogger("uvicorn.xml")

@dataclass
class response:
    status: int = 500
    status_text: str = None
    data: str = None

def root(data: str) -> response:
    try:
        root = ET.fromstring(data)
    except Exception as err:
        LOGGER.error(f"XML Data is not XML format. Error: '{err}'")
        return response(data=data)
    
    try:
        return response(int(root.get('status')), root.get('status_text'), data)
    except Exception as err:
        LOGGER.error(f"XML Root is missing 'status'. Error: '{err}'")
        return response(data=data)