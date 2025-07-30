import logging
import json
from typing import Any
from . import file_util

# Logging
_logger = logging.getLogger(__name__) # module name

def parseFromFile(path:str) -> Any :
    """
    Opens a JSON file and returns the de-serialised object.
    If the file does not exist or cannot be decoded, it returns None.

    Args:
        path (str): The path to the JSON file to open.

    Returns:
        Any: The de-serialised JSON object, or None if the file cannot be opened or decoded.
    """
    try :
        if file_util.exists(path) :
            with open(path) as openFile:
                _logger.debug(f"Opening JSON file at {path}")
                return json.load(fp=openFile)
        else :
            _logger.error(f"Cannot open non-existent file at {path}")            
    except json.JSONDecodeError as e :    
        _logger.error(f"Unable to decode JSON in file at {path} : {e}")

    return None
