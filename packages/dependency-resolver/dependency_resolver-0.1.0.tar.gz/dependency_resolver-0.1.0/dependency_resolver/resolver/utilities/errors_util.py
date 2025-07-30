class ProjectError(Exception) :
    """
    Base class for all raised by this project.
    Using this as a base class for all custom errors allows developers to use except ProjectException to trap these project-based custom exceptions.
    """
    

class UtilityError(ProjectError) :
    """Raised by utility functions."""


class HttpError(UtilityError) :
    """Raised by the http utility functions to indicate some issue."""


class ZipError(UtilityError) :
    """Raised by the zip utility functions to indicate some issue."""


class TarError(UtilityError) :
    """Raised by the tar utility functions to indicate some issue."""
