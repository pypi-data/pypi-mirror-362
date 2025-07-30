from orionis.foundation.config.logging.entities.logging import Logging
from orionis.foundation.config.logging.enums import Level
from orionis.services.log.contracts.log_service import ILoggerService
from orionis.services.log.exceptions import LoggerRuntimeError
from orionis.services.log.handlers.size_rotating import PrefixedSizeRotatingFileHandler
from orionis.services.log.handlers.timed_rotating import PrefixedTimedRotatingFileHandler

class LoggerService(ILoggerService):

    def __init__(
        self,
        config: Logging | dict = None,
        **kwargs
    ):
        """
        Initialize the LoggerService with the provided configuration.

        Parameters
        ----------
        config : Logging or dict, optional
            The logging configuration. Can be an instance of the Logging class,
            a dictionary of configuration parameters, or None. If None, configuration
            is initialized using kwargs.
        **kwargs
            Additional keyword arguments used to initialize the Logging configuration
            if config is None.

        Raises
        ------
        LoggerRuntimeError
            If the logger configuration cannot be initialized from the provided arguments.
        """

        # Attributes
        self.__logger = None
        self.__config = None

        # Initialize the logger configuration using **kwargs if provided
        if config is None:
            try:
                self.__config = Logging(**kwargs)
            except Exception as e:
                raise LoggerRuntimeError(f"Failed to initialize logger configuration: {e}")

        # If config is a dictionary, convert it to Logging
        elif isinstance(config, dict):
            self.__config = Logging(**config)

        # If config is already an instance of Logging, use it directly
        elif isinstance(config, Logging):
            self.__config = config

        # Initialize LoggerService
        self.__initLogger()

    def __filename(self, original_path:str) -> str:
        """
        Generates a rotated log filename by prefixing the original filename with a timestamp.
        This method takes an original file path, extracts its directory, base name, and extension,
        and returns a new file path where the base name is prefixed with the current timestamp
        in the format 'YYYYMMDD_HHMMSS'. If the target directory does not exist, it is created.
            The original file path to be rotated.
            The new file path with a timestamp prefix added to the base name.
        Notes
        -----
        - The timestamp is based on the current local time.
        - The method ensures that the parent directory for the new file exists.

        Returns
        -------
        str
            The new filename with a timestamp prefix in the format 'YYYYMMDD_HHMMSS'.
        """
        import os
        from datetime import datetime
        from pathlib import Path

        # Split the original path to extract the base name and extension
        if '/' in original_path:
            parts = original_path.split('/')
        elif '\\' in original_path:
            parts = original_path.split('\\')
        else:
            parts = original_path.split(os.sep)

        # Get the base name and extension
        filename, ext = os.path.splitext(parts[-1])

        # Create the path without the last part
        path = os.path.join(*parts[:-1]) if len(parts) > 1 else ''

        # Prefix the base name with a timestamp
        prefix = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Join the path, prefix, and filename to create the full path
        full_path = os.path.join(path, f"{prefix}_{filename}{ext}")

        # Ensure the log directory exists
        log_dir = Path(full_path).parent
        if not log_dir.exists():
            log_dir.mkdir(parents=True, exist_ok=True)

        # Return the full path as a string
        return full_path

    def __initLogger(self):
        """
        Configures the logger with the specified settings.

        This method sets up the logger to write logs to a file. If the specified
        directory does not exist, it creates it. The log format includes the
        timestamp and the log message.

        Raises
        ------
        LoggerRuntimeError
            If the logger cannot be initialized due to an error.
        """
        import logging
        from datetime import datetime

        try:

            # List to hold the handlers
            handlers = []

            # Get the channel from the configuration
            channel: str = self.__config.default

            # Get the configuration for the specified channel
            config_channels = getattr(self.__config.channels, channel)

            # Get the path from the channel configuration
            path: str = self.__filename(getattr(config_channels, 'path'))

            # Get Level from the channel configuration, defaulting to 10 (DEBUG)
            level: Level | int = getattr(config_channels, 'level', 10)
            level = level if isinstance(level, int) else level.value

            # Create handlers based on the channel type
            if channel == "stack":

                handlers = [
                    logging.FileHandler(
                        filename=path,
                        encoding="utf-8"
                    )
                ]

            elif channel == "hourly":

                handlers = [
                    PrefixedTimedRotatingFileHandler(
                        filename = path,
                        when = "h",
                        interval = 1,
                        backupCount = getattr(config_channels, 'retention_hours', 24),
                        encoding = "utf-8",
                        utc = False
                    )
                ]

            elif channel == "daily":

                handlers = [
                    PrefixedTimedRotatingFileHandler(
                        filename = path,
                        when = "d",
                        interval = 1,
                        backupCount = getattr(config_channels, 'retention_days', 7),
                        encoding = "utf-8",
                        atTime = datetime.strptime(getattr(config_channels, 'at', "00:00"), "%H:%M").time(),
                        utc = False
                    )
                ]

            elif channel == "weekly":

                handlers = [
                    PrefixedTimedRotatingFileHandler(
                        filename = path,
                        when = "w0",
                        interval = 1,
                        backupCount = getattr(config_channels, 'retention_weeks', 4),
                        encoding = "utf-8",
                        utc = False
                    )
                ]

            elif channel == "monthly":

                handlers = [
                    PrefixedTimedRotatingFileHandler(
                        filename = path,
                        when = "midnight",
                        interval = 30,
                        backupCount = getattr(config_channels, 'retention_months', 4),
                        encoding = "utf-8",
                        utc = False
                    )
                ]

            elif channel == "chunked":

                handlers = [
                    PrefixedSizeRotatingFileHandler(
                        filename = path,
                        maxBytes = getattr(config_channels, 'mb_size', 10) * 1024 * 1024,
                        backupCount =getattr(config_channels, 'files', 5),
                        encoding ="utf-8"
                    )
                ]

            # Configure the logger
            logging.basicConfig(
                level = level,
                format = "%(asctime)s [%(levelname)s] - %(message)s",
                datefmt = "%Y-%m-%d %H:%M:%S",
                encoding = "utf-8",
                handlers = handlers
            )

            # Get the logger instance
            self.__logger = logging.getLogger(__name__)

        except Exception as e:

            # Raise a runtime error if logger initialization fails
            raise LoggerRuntimeError(f"Failed to initialize logger: {e}")

    def info(self, message: str) -> None:
        """
        Log an informational message.

        Parameters
        ----------
        message : str
            The informational message to log.

        Returns
        -------
        None
        """
        self.__logger.info(message.strip())

    def error(self, message: str) -> None:
        """
        Log an error message.

        Parameters
        ----------
        message : str
            The error message to log.

        Returns
        -------
        None
        """
        self.__logger.error(message.strip())

    def warning(self, message: str) -> None:
        """
        Log a warning message.

        Parameters
        ----------
        message : str
            The warning message to log.

        Returns
        -------
        None
        """
        self.__logger.warning(message.strip())

    def debug(self, message: str) -> None:
        """
        Log a debug message.

        Parameters
        ----------
        message : str
            The debug message to log.

        Returns
        -------
        None
        """
        self.__logger.debug(message.strip())