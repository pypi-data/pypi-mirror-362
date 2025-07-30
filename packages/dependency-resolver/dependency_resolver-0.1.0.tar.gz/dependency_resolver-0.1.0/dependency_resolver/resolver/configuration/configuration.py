import logging
from typing import Optional
from .attributes import ConfigAttributes
from ..utilities import helpers, json_util, file_util

_logger = logging.getLogger(__name__)

class Configuration :
    def __init__(self, configurationPath:str) :
        helpers.assertSet(_logger, f"Please specify path to configuration JSON file", configurationPath)
        self._configPath:str = configurationPath
        self._loadConfiguration()

    # Load the configuration 
    def _loadConfiguration(self) :
        if file_util.isFile(self._getConfigurationPath()) :
            self._config:dict = json_util.parseFromFile(self._getConfigurationPath())
            helpers.assertSet(_logger, f"Unable to load the JSON representation in the path {self._getConfigurationPath()}", self.getConfiguration()) # make sure we managed to open the configuration
            _logger.debug(f"Loaded configuration: {self.getConfiguration()}")
        else :
            _logger.debug(f"Cannot load configuration - file doesn't exist at {self._getConfigurationPath()}")
            exit(1) # a terminal condition.


    # Returns the loaded configuration path
    def _getConfigurationPath(self) -> str :
        return self._configPath

    
    def getConfigurationHome(self) -> str :
        """
        Returns the path to the directory the configuration file was loaded from. All dependency targets are relative to this directory.

        Returns:
            str: The path to the directory containing the configuration file.
        """
        return file_util.getParentDirectory(self._getConfigurationPath())


    def getConfiguration(self) -> dict :
        """
        Returns the loaded configuration.

        Returns:
            dict: The loaded configuration dictionary.
        """
        return self._config

                
    def printConfiguration(self) :
        """
        Prints the loaded configuration in a human-readable format.
        """
        print(self.getConfiguration())


    def validateConfiguration(self) :
        """
        Finds any errors (required attributes that are missing) in the configuration and prints them.
        """
        errors:list[str] = self._findAnyConfigErrors()
        if len(errors) > 0 :
            print(f"Invalid: the configuration at {self._getConfigurationPath()} contains {len(errors)} error(s):")
            count:int = 0
            for error in errors:
                count += 1
                print(f"  {count} -> {error}")
        else :
            print(f"Valid: the configuration at {self._getConfigurationPath()} doesn't contain any errors.")              


    def numberOfErrors(self) -> int :
        """
        Returns the number of configuration errors (missing required attributes).

        Returns:
            int: The number of configuration errors.
        """
        return len(self._findAnyConfigErrors())


    # Finds any errors (required attributes that are missing) in the configuration and returns a list of them.
    def _findAnyConfigErrors(self) -> list[str] :
        config:dict = self.getConfiguration()
        errors:list[str] = []
        self._validateProjectName(config, errors)
        self._validateSources(config, errors)
        self._validateDependencies(config, errors)
        return errors


    # Adds any errors to a list of previous errors.    
    def _validateProjectName(self, config:dict, errors:list[str]) :
        helpers.addIfNotNone(errors, self._doesKeyExist(config, ConfigAttributes.PROJECT_NAME, False))

        
    # Adds any sources errors to a list of previous errors.    
    def _validateSources(self, config:dict, errors:list[str]) :
        key:str = ConfigAttributes.SOURCES
        error:str|None = self._doesKeyExist(config, key, False)
        if error :
            errors.append(error)
        else :
            for source in config.get(key, []) :
                self._validateSource(source, errors)

        
    # Adds any errors found in the source to a list of previous errors.
    def _validateSource(self, source:dict, errors:list[str]) :
        helpers.addIfNotNone(errors, self._doesKeyExist(source, ConfigAttributes.SOURCE_NAME))
        helpers.addIfNotNone(errors, self._doesKeyExist(source, ConfigAttributes.SOURCE_PROTOCOL))

                             
    # Adds any sources errors to  a list of previous errors.    
    def _validateDependencies(self, config:dict, errors:list[str]) :
        key:str = ConfigAttributes.DEPENDENCIES
        error:str|None = self._doesKeyExist(config, key, False)
        if error :
            errors.append(error)
        else :
            for dependency in config.get(key, []) :
                self._validateDependency(dependency, errors)

        
    # Adds any errors found in the source to a list of previous errors.
    def _validateDependency(self, dependency:dict, errors:list[str]) :
        helpers.addIfNotNone(errors, self._doesKeyExist(dependency, ConfigAttributes.DEPENDENCY_NAME))
        helpers.addIfNotNone(errors, self._doesKeyExist(dependency, ConfigAttributes.DEPENDENCY_TARGET_DIR))
        helpers.addIfNotNone(errors, self._doesKeyExist(dependency, ConfigAttributes.DEPENDENCY_SOURCE_DEPENDENCY))


    # Checks to see if a key has been specified in the config. Returns an error message if missing/empty.
    def _doesKeyExist(self, config:dict, key, context:bool = True) -> Optional[str] :
        if key not in config or not config[key] :
            error:str = f"Required attribute {key} is not specified or is empty."
            if context :
                error=f"{error} In: {config}."
            return error
