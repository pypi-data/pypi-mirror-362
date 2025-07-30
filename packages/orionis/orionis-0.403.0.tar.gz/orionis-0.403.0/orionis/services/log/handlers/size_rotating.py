from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

class PrefixedSizeRotatingFileHandler(RotatingFileHandler):

    def rotation_filename(self, default_name):
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
        # Split the original path to extract the base name and extension
        if '/' in default_name:
            parts = default_name.split('/')
        elif '\\' in default_name:
            parts = default_name.split('\\')
        else:
            parts = default_name.split(os.sep)

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