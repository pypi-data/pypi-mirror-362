from typing import Any
from orionis.foundation.exceptions import OrionisIntegrityException

class __IsValidPath:
    """
    __IsValidPath is a callable class used to validate that a given value is a non-empty string representing a file path.

    Methods
    -------
    __call__(value: Any) -> None

    Raises
    ------
    OrionisIntegrityException
        If the provided value is not a non-empty string representing a file path.
    """

    def __call__(self, value: Any) -> None:
        """
        Validates that the provided value is a non-empty string representing a file path.

        Args:
            value (Any): The value to validate as a file path.

        Raises:
            OrionisIntegrityException: If the value is not a non-empty string.
        """
        if not isinstance(value, str) or not value.strip():
            raise OrionisIntegrityException(
                f"File cache configuration error: 'path' must be a non-empty string, got {repr(value)}."
            )

# Exported singleton instance
IsValidPath = __IsValidPath()