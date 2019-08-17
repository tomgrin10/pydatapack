class DatapackCompilationError(Exception):
    """
    Raised when datapack compilation is unsuccessful for any reason.
    """
    pass


class InvalidCommandError(DatapackCompilationError):
    """
    Raised when an invalid command is called.
    """
    pass


class BadArgumentsError(DatapackCompilationError):
    """
    Raised when a function receives invalid arguments.
    """
    pass
