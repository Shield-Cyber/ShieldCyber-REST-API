from dataclasses import dataclass
import xml.etree.ElementTree as ET
import logging
from app import LOGGING_PREFIX

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.xml")

@dataclass
class response:
    status: int = 500
    status_text: str = None
    data: str = None

def root(data: str) -> response:
    try:
        root = ET.fromstring(data)
    except Exception as err:
        LOGGER.debug(f"XML Data is not XML format. Error: '{err}'")
        return response(data=data)
    
    try:
        return response(int(root.get('status')), root.get('status_text'), data)
    except Exception as err:
        LOGGER.debug(f"XML Root is missing 'status' or 'status_text'. Error: '{err}'")
        return response(data=data)