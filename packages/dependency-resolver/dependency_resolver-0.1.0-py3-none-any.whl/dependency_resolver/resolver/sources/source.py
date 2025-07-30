import logging
from typing import Optional
from .protocol import SourceProtocol
from .type  import SourceType
from ..configuration.attributes import ConfigAttributes
from ..utilities import file_util, helpers

# Logging
_logger = logging.getLogger(__name__) # module name

class Source :

    def __init__(self, name:str, protocol:SourceProtocol, type:Optional[SourceType] = None,  base:Optional[str] = None, description:Optional[str] = None):
        """
        Parameters:
            name - The unique name given to this source.
            protocol - How to get the file - for example is this a https get, REST endpoint, filesystem copy (not all of these are supported at the moment). Optional.
            base - The start of the path for the source file. A dependency can extend this base path with a specific location. Optional.
            description - A textual description of this source. Optional.
        """
        helpers.assertSet(_logger, f"The source {ConfigAttributes.SOURCE_NAME} attribute must be set in the source with description: {description}, base:{base}), protocol{protocol}.", name)
        helpers.assertSet(_logger, f"The source {ConfigAttributes.SOURCE_PROTOCOL} attribute must be set in source {name}.", protocol)

        self._name:str = name
        self._protocol:SourceProtocol = protocol
        self._setType(type)
        self._base:str = base if base is not None else ""
        self._description:str = description if description is not None else ""
        
  
    def fetch(self, sourcePath:str, targetDir:str, targetName:str) :
        """
        Fetches the source (file) and puts it in the specified directory.
        How this is fetched depends on the protocol used.

        Parameters:
            sourcePath - the relative path to this source.
            targetDir - the absolute path to the directory to put this file.
            targetName - the file name to give this download.
        
        Raises:
            FetchError if the fetch is unsuccessful.
        """
        fullPath:str = self.getAbsoluteSourcePath(sourcePath)
        _logger.debug(f"Fetching {fullPath} -> {targetDir}/{targetName}.")
        self._getProtocol().fetch(fullPath, targetDir, targetName) 


    def getAbsoluteSourcePath(self, sourcePath:Optional[str]) -> str :
        """
        Determines the absolute source path, based on this source's base.

        Parameters:
            sourcePath - any additional path, relative to the source base. Optional.
        """
        if helpers.hasValue(sourcePath) :
             # construct the full path/URI to the source
            return file_util.buildPath(self._getBase(), sourcePath) # type: ignore - helpers.hasValue checks for None
        else :
            return self._getBase()


    # Returns the sources protocol
    def _getProtocol(self) -> SourceProtocol :
        return self._protocol
    
    # Returns the name of this source
    def getName(self) -> str :
        return self._name
    
    # Returns the url/path base of this source
    def _getBase(self) -> str :
        return self._base

    # Returns the description of this source
    def _getDescription(self) -> str :
        return self._description
            
    # Set the type of source path (absolute, relative)
    def _setType(self, type:Optional[SourceType]) :
        if type is None :
            self._type = SourceType.ABSOLUTE
        else :
            self._type:SourceType = type
        
    # Returns the SourceType of this source
    def _getType(self) -> SourceType :
        return self._type

