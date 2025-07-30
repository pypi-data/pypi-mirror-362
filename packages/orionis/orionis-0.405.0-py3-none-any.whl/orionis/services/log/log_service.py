from orionis.foundation.config.logging.entities.logging import Logging
from orionis.foundation.config.logging.enums import Level
from orionis.services.log.contracts.log_service import ILoggerService
from orionis.services.log.exceptions import LoggerRuntimeError
from orionis.services.log.handlers.filename import FileNameLogger
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
                raise LoggerRuntimeError(
                    f"Error initializing logger configuration: {e}. "
                    "Please check the provided parameters. "
                    f"Expected a Logging dataclass or a configuration dictionary. "
                    f"Type received: {type(config).__module__}.{type(config).__name__}. "
                    f"Expected: {Logging.__module__}.{Logging.__name__} or dict."
                )

        # If config is a dictionary, convert it to Logging
        elif isinstance(config, dict):
            self.__config = Logging(**config)

        # If config is already an instance of Logging, use it directly
        elif isinstance(config, Logging):
            self.__config = config

        # Initialize LoggerService
        self.__initLogger()

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
            path: str = FileNameLogger(getattr(config_channels, 'path')).generate()

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