from abc import ABC, abstractmethod

class ILoggerService(ABC):

    @abstractmethod
    def info(self, message: str) -> None:
        """Log an informational message."""
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        """Log an error message."""
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        """Log a warning message."""
        pass

    @abstractmethod
    def debug(self, message: str) -> None:
        """Log a debug message."""
        pass