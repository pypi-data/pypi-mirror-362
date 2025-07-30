import os
from datetime import datetime
from pathlib import Path

class FileNameLogger:

    def __init__(self, path: str) -> None:
        """
        Initialize the FileNameLogger.

        Parameters
        ----------
        path : str
            The original file path for the log file.
        """

        # If the path is not a string or is empty, raise a ValueError
        if not isinstance(path, str) or not path:
            raise ValueError("The 'path' parameter must be a non-empty string.")

        # Set the instance variable __path to the stripped path
        self.__path = path.strip()

    def generate(self) -> str:
        """
        Generate a new log file path with a timestamp prefix.

        Returns
        -------
        str
            The full path to the log file with a timestamped file name.

        Notes
        -----
        The method ensures that the directory for the log file exists.
        """

        # Split the original path to extract the base name and extension
        if '/' in self.__path:
            parts = self.__path.split('/')
        elif '\\' in self.__path:
            parts = self.__path.split('\\')
        else:
            parts = self.__path.split(os.sep)

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