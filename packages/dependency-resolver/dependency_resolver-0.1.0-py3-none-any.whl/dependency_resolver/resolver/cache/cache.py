import logging
from ..utilities import file_util, helpers
from ..dependencies.dependency import Dependency
from ..errors.errors import FetchError, ResolveError

_logger = logging.getLogger(__name__)

class Cache() :
    # When we download something in the cache we have to give it a file name.
    #  This may the the target name of the dependency, but if not specified then we use this default.
    #  This is a possible clash, but it needs to be something deterministic for a dependency.
    defaultDownloadName:str = "downloadedSource"


    def __init__(self, cacheRoot:str = "") :
        """
        Construct the cache.
            Parameters:
                cacheRoot - the home/root directory of the cache. All downloaded sources will be added somewhere in this directory.
        """
        # initialise the cache root and cache name, so they are defined.
        self._cacheRoot:str = ""
        self._cacheName:str = ""
        self.init(cacheRoot=cacheRoot)


    def clean(self) :
        """Empty the cache."""
        if file_util.exists(self._getCachePath()) :
            _logger.info(f"Cleaning cache: {self._getCachePath()}")
            file_util.deleteContents(self._getCachePath())
        

    def init(self, cacheName:str = "", cacheRoot:str = "") :
        """
        Initializes the cache. 
        Must be called before it is used.

        Parameters:
            cacheName - Can give this cache a specific name. All sources will be downloaded under this name, separating the from the rest of the cache. Optional.
            cacheRoot - Set the root of the cache. Optional.
        """
        # If we have not been instantiated with a root then use the project's cache root, if specified.
        if helpers.isEmpty(self._getCacheRoot()) :
            self._setCacheRoot(cacheRoot)

        self._setCacheName(cacheName)
        
        file_util.mkdir(self._getCachePath(), mode=0o755) # make sure the cache directory exists


    def fetchDependency(self, dependency:Dependency, alwaysFetch:bool = False) :
        """
        Fetches a dependency's source into the cache.
        
        Parameters:
            dependency - the dependency to fetch.
            alwaysFetch - will always fetch the dependency's source, even if it is already in the cache.
        """
        _logger.debug(f"Downloading dependency {dependency.getName()}...")
        
        if dependency.alwaysUpdate() or (alwaysFetch or not self._isCached(dependency)) :
            targetDir:str = self._generateCacheLocation(dependency)
            if targetDir and not file_util.exists(targetDir) :
                _logger.debug(f"Trying to create cache location: {targetDir}")
                file_util.mkdir(targetDir, mode=0o755)

            targetName:str = self._generateCachedFileName(dependency)
            if targetDir and file_util.isDir(targetDir) :
                cacheDownloadPath:str = self._generateCacheDownloadPath(dependency)
                if file_util.exists(cacheDownloadPath) :
                    file_util.delete(cacheDownloadPath)
                
                dependency.fetchSource(targetDir, targetName)
                _logger.debug(f"...successfully cached dependency {dependency.getName()}: source {dependency.getSource().getName()}::{dependency.getSourcePath()} -> {targetDir}/{targetName}.")
            else :
                _logger.debug(f"...failed to cache dependency {dependency.getName()} - the cache already has a file (not a directory) at the target download location in the cache ({targetDir}): source {dependency.getSource().getName()}::{dependency.getSourcePath()} -> {targetDir}/{targetName}.")
                raise FetchError(f"Failed to cache dependency {dependency.getName()} - the cache already has a file (not a directory) at the target download location in the cache ({targetDir}).")
        else :
            _logger.debug(f"...dependency {dependency.getName()} already in cache.")
            

    def resolveDependency(self, dependency:Dependency, targetHomeDir:str, onlyMissing:bool = False) :
        """
        Resolves a dependency by performing its Resolve action from the fetched source in the cache into the target location.
        
        Parameters:
            dependency - the dependency to resolve.
            targetHome - Each dependency is relative the configuration that defines it. This is the path to that directory.
            onlyMissing - only resolve missing dependencies. Non filesystem copies (for example unzipping) resolve actions are always completed.
        """
        _logger.debug(f"Resolving dependency {dependency.getName()}...")
        if self._isCached(dependency) :
            dependency.resolve(self._generateCacheDownloadPath(dependency), targetHomeDir)
            _logger.debug(f"...successfully resolved dependency {dependency.getName()}.")
        else :
            _logger.debug(f"...dependency {dependency.getName()} not in cache.")
            raise ResolveError(f"Failed to resolve dependency {dependency.getName()} - the source has not been fetched to the cache.")


    # Generates the path to the directory (inside the cache) that the source of the dependency is fetched to.
    def _generateCacheLocation(self, dependency:Dependency) -> str :
        # cache location is based on the source name and the source path   
        return file_util.buildPath(self._getCachePath(), dependency.getSource().getName(), dependency.getSourcePath())


    # Generates the a name to use in the cache to represent the fetched source.
    # Usually the target name of the dependency, if thats been specified.
    def _generateCachedFileName(self, dependency:Dependency) -> str :
        cacheName:str = dependency.getTargetName()
        if not cacheName and dependency.getSourcePath() : # use the end of the source path if specified.
            cacheName = file_util.returnLastPartOfPath(dependency.getSourcePath())
        if not cacheName : # just use a default name
            cacheName = self.defaultDownloadName 
        return cacheName


    # Return to the full path (including the file name) of the fetched dependency in the cache.
    def _generateCacheDownloadPath(self, dependency:Dependency) -> str :
        return file_util.buildPath(self._generateCacheLocation(dependency), self._generateCachedFileName(dependency))
    

    # Sets the root of this cache.
    def _setCacheRoot(self, cacheRoot:str) :
        if helpers.hasValue(cacheRoot) :
            if not file_util.exists(cacheRoot) or (file_util.exists(cacheRoot) and file_util.isDir(cacheRoot)) :
                self._cacheRoot:str = cacheRoot
            else :
                _logger.error(f"Unable to create cache with a root of {cacheRoot} - a file already exists at this location (at least its not a directory - could be a permission thing also).")
                exit(1)
        else : # Set the cache root to empty - python will complain if its requested, but nothing has been defined.
            self._cacheRoot:str = ""
           
        self._setCachePath()


    # Returns the root path of the cache
    def _getCacheRoot(self) -> str :
        return self._cacheRoot


    # Sets the name of this cache. This can be used to use a specific cache for a project rather than using the same cache for everything.
    def _setCacheName(self, cacheName:str) :
        if helpers.isEmpty(cacheName):
            self._cacheName = "default"
        else :
            self._cacheName = cacheName
    
        self._setCachePath()


    # Returns the name of the cache - this is configurable for each project (and is often the name of the project)
    def _getCacheName(self) -> str :
        return self._cacheName
    
    # Constructs and sets the path for the cache.
    def _setCachePath(self) :
        root:str = self._getCacheRoot()

        # if nothing has been set, default to the user's home directory
        if helpers.isEmpty(root) :
            root = file_util.buildPath(file_util.getUserDirectory(), ".resolverCache") 

        self._cachePath:str = file_util.buildPath(root, self._getCacheName())
        _logger.debug(f"Caching to {self._getCachePath()}")
    

    # Returns the path for this cache
    def _getCachePath(self) -> str :
        return self._cachePath
    

    # Is there an entry in the cache for this dependency already?
    def _isCached(self, dependency:Dependency) -> bool :
        return file_util.exists(self._generateCacheDownloadPath(dependency))