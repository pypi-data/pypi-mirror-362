from logging.handlers import RotatingFileHandler
from orionis.services.log.handlers.filename import FileNameLogger

class PrefixedSizeRotatingFileHandler(RotatingFileHandler):

    def rotation_filename(self, default_name) -> str:
        """
        Generate a rotated log filename by prefixing the original filename with a timestamp.

        Parameters
        ----------
        default_name : str
            The original file path to be rotated.

        Returns
        -------
        str
            The new file path with the base name prefixed by a timestamp in the format 'YYYYMMDD_HHMMSS'.
        """

        return FileNameLogger(default_name).generate()