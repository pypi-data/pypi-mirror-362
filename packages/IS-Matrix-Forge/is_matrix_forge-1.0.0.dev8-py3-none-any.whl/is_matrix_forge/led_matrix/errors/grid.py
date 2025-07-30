from .base import LEDMatrixControllerError


class GridDefinitionError(LEDMatrixControllerError, ValueError):
    """
    Base class for all grid definition errors.

    A "grid definition error" is an error that occurs while defining a grid for the LED matrix, either in translation
    from data to the LED matrix or in the grid itself. This includes errors such as malformed grids, invalid grid
    sizes, etc.

    Provided Subclasses:
        - MalformedGridError:
            Raised when the grid structure does not match expectations. This can include issues such as incorrect
            dimensions, missing elements, or other structural problems.
    """
    default_message = 'An error has occurred within the grid definition!'


class MalformedGridError(GridDefinitionError):
    """
    Raised when the grid is malformed.

    Class Attributes:
        default_message (str):
            **Read-Only**. The default message for the error.
    """
    default_message = 'The grid is malformed!'

    def __init__(self, more_info: str = None, **kwargs) -> None:
        if more_info is not None:
            self.default_message = f"{self.default_message}\n\n  Additional information from caller:\n    {more_info}"

        super().__init__(message=self.default_message, **kwargs)


__all__ = ['GridDefinitionError', 'MalformedGridError']
