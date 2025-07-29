from dataclasses import dataclass, field, asdict, fields
from orionis.foundation.config.logging.entities.channels import Channels
from orionis.foundation.exceptions import OrionisIntegrityException

@dataclass(unsafe_hash=True, kw_only=True)
class Logging:
    """
    Represents the logging system configuration.

    Attributes
    ----------
    default : str
        The default logging channel to use.
    channels : Channels
        A collection of available logging channels.
    """
    default: str = field(
        default="stack",
        metadata={
            "description": "The default logging channel to use.",
            "default": "stack",
        }
    )
    channels: Channels = field(
        default_factory=Channels,
        metadata={
            "description": "A collection of available logging channels.",
            "default": "Channels()",
        }
    )

    def __post_init__(self):
        """
        Validates the types of the attributes after initialization.
        """
        options = [field.name for field in fields(Channels)]
        if not isinstance(self.default, str) or self.default not in options:
            raise OrionisIntegrityException(
                f"The 'default' property must be a string and match one of the available options ({options})."
            )

        if not isinstance(self.channels, Channels):
            raise OrionisIntegrityException(
                "The 'channels' property must be an instance of Channels."
            )

    def toDict(self) -> dict:
        """
        Converts the current instance into a dictionary representation.
        """
        return asdict(self)

    def getFields(self):
        """
        Retrieves a list of field information for the current dataclass instance.

        Returns:
            list: A list of dictionaries, each containing details about a field:
                - name (str): The name of the field.
                - type (type): The type of the field.
                - default: The default value of the field, if specified; otherwise, the value from metadata or None.
                - metadata (mapping): The metadata associated with the field.
        """
        __fields = []
        for field in fields(self):
            __metadata = dict(field.metadata) or {}
            __fields.append({
                "name": field.name,
                "type": field.type.__name__ if hasattr(field.type, '__name__') else str(field.type),
                "default": field.default if (field.default is not None and '_MISSING_TYPE' not in str(field.default)) else __metadata.get('default', None),
                "metadata": __metadata
            })
        return __fields
