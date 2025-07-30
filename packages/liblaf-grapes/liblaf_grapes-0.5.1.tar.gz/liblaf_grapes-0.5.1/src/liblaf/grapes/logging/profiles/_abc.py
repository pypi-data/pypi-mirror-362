import abc

import attrs
import autoregistry


@attrs.define
class LoggingProfile(abc.ABC, autoregistry.Registry, prefix="LoggingProfile"):
    @abc.abstractmethod
    def init(self) -> None: ...
