from orionis.container.facades.facade import Facade

class Log(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Get the service container binding key for the dumper component.

        Returns
        -------
        str
            The service container binding key.
        """
        return "core.orionis.logger"