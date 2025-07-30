from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.log.contracts.log_service import ILoggerService
from orionis.services.log.log_service import LoggerService

class LoggerProvider(ServiceProvider):

    def register(self) -> None:
        """
        Register services into the application container.
        """
        self.app.instance(ILoggerService, LoggerService(self.app.config('logging')), alias="core.orionis.logger")

    def boot(self) -> None:
        """
        Perform any post-registration bootstrapping or initialization.
        """
        pass