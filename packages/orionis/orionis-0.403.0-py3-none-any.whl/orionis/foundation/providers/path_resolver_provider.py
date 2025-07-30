from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.paths.contracts.resolver import IResolver
from orionis.services.paths.resolver import Resolver

class PathResolverProvider(ServiceProvider):

    def register(self) -> None:
        """
        Register services into the application container.
        """
        self.app.transient(IResolver, Resolver, alias="core.orionis.path_resolver")

    def boot(self) -> None:
        """
        Perform any post-registration bootstrapping or initialization.
        """
        pass