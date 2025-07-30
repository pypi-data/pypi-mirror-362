from dataclasses import asdict, fields
from dataclasses import MISSING

class BaseConfigEntity:

    def toDict(self) -> dict:
        """
        Converts the current instance into a dictionary representation.

        Returns
        -------
        dict
            Dictionary representation of the current instance.
        """
        return asdict(self)

    def getFields(self):
        """
        Retrieves a list of field information for the current dataclass instance.

        Returns
        -------
        list
            A list of dictionaries, each containing details about a field:
            - name (str): The name of the field.
            - type (type): The type of the field.
            - default: The default value of the field, if specified; otherwise, the value from metadata or None.
            - metadata (mapping): The metadata associated with the field.
        """
        # Dictionary to hold field information
        __fields = []

        # Iterate over the fields of the dataclass
        # and extract relevant information
        for field in fields(self):

            # Get the field name
            __name = field.name

            # Get the field type with better handling for complex types
            __type = getattr(field.type, '__name__', None)

            # If the type is None, handle it
            if __type is None:

                # Handle generic types, unions, and other complex annotations
                type_str = str(field.type)

                # Clean up typing module references
                type_str = type_str.replace('typing.', '')

                # Handle Union types (e.g., "Channels | dict" or "Union[Channels, dict]")
                if '|' in type_str or 'Union[' in type_str:

                    # Extract individual types from Union
                    if 'Union[' in type_str:

                        # Handle typing.Union format
                        inner = type_str.replace('Union[', '').replace(']', '')
                        types = [t.strip() for t in inner.split(',')]

                    else:
                        # Handle | format (Python 3.10+)
                        types = [t.strip() for t in type_str.split('|')]

                    # Get class names for custom types
                    clean_types = []
                    for t in types:
                        if '.' in t:
                            clean_types.append(t.split('.')[-1])
                        else:
                            clean_types.append(t)

                    # Join cleaned types with ' | '
                    __type = ' | '.join(clean_types)

                else:

                    # Handle other complex types
                    if '.' in type_str:
                        __type = type_str.split('.')[-1]
                    else:
                        __type = type_str

            # Extract metadata, default value, and type
            __metadata = dict(field.metadata) or {}

            # Extract the default value, if specified
            __default = None

            # Field has a direct default value
            if field.default is not MISSING:
                __default = field.default

            # Field has a default factory (like list, dict, etc.)
            elif field.default_factory is not MISSING:
                __default = f"<factory: {field.default_factory.__name__}>"

            # No default found, check metadata for custom default
            else:
                __default = __metadata.get('default', None)

            # Append the field information to the list
            __fields.append({
                "name": __name,
                "type": __type,
                "default": __default,
                "metadata": __metadata
            })

        # Return the list of field information
        return __fields