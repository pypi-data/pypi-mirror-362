from enum import Enum

class Level(Enum):
    """
    Enumeration of standard logging levels.

    Attributes:
        NOTSET (int): No specific logging level set. Value is 0.
        DEBUG (int): Detailed information, typically of interest only when diagnosing problems. Value is 10.
        INFO (int): Confirmation that things are working as expected. Value is 20.
        WARNING (int): An indication that something unexpected happened, or indicative of some problem in the near future. Value is 30.
        ERROR (int): Due to a more serious problem, the software has not been able to perform some function. Value is 40.
        CRITICAL (int): A very serious error, indicating that the program itself may be unable to continue running. Value is 50.
    """

    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50
