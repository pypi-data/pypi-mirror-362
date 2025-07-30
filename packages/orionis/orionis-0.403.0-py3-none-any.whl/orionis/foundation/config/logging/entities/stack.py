from dataclasses import dataclass, field
from orionis.foundation.config.base import BaseConfigEntity
from orionis.foundation.config.logging.validators import IsValidLevel, IsValidPath
from orionis.foundation.config.logging.enums import Level

@dataclass(unsafe_hash=True, kw_only=True)
class Stack(BaseConfigEntity):
    """
    Represents the configuration for a logging stack, including the log file path and logging level.
    """

    path: str = field(
        default = 'storage/log/application.log',
        metadata = {
            "description": "The file path where the log is stored.",
            "default": "storage/log/application.log",
        },
    )

    level: int | str | Level = field(
        default = Level.INFO,
        metadata = {
            "description": "The logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).",
            "default": Level.INFO,
        },
    )

    def __post_init__(self):
        """
        Validates the 'path' and 'level' attributes after dataclass initialization.

        Raises:
            OrionisIntegrityException: If 'path' is not a non-empty string, or if 'level' is not a valid type or value.
        """

        # Validate 'path' using the IsValidPath validator
        IsValidPath(self.path)

        # Validate 'level' using the IsValidLevel validator
        IsValidLevel(self.level)