class ProcessingError(Exception):
    def __init__(self, message: str | None = None):
        self.message = message


class InvalidData(ProcessingError):
    pass


class DependenciesError(ProcessingError):
    pass
