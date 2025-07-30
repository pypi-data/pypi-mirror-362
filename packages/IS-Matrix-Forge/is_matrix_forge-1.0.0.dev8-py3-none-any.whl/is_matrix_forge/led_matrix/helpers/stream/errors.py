from inspyre_toolbox.exceptional import CustomRootException


class MatrixStreamError(CustomRootException):
    default_message= 'An error occurred while streaming to the LED matrix!'

    def __init__(self, message=None):
        if message is None:
            message = self.default_message
        else:
            message = f'{self.default_message}\n\n  Additional Info:\n{" " * 4}{message}'
        super().__init__(message)


class StreamSourceUnreadableError(MatrixStreamError):
    def __init__(self):
        super().__init__('The source is not readable.')
