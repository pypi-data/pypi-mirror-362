from collections.abc import Sequence
from typing import override

import attrs
import loguru

from liblaf.grapes.logging import handlers

from . import mixins
from ._abc import LoggingProfile


def default_handlers() -> Sequence["loguru.HandlerConfig"]:
    return [handlers.rich_handler()]


def default_levels() -> Sequence["loguru.LevelConfig"]:
    return [{"name": "ICECREAM", "no": 15, "color": "<magenta><bold>", "icon": "🍦"}]


@attrs.define
class LoggingProfileDefault(
    mixins.LoggingProfileMixinLoguru,
    mixins.LoggingProfileMixinStdlib,
    mixins.LoggingProfileMixinIcecream,
    mixins.LoggingProfileMixinExceptHook,
    mixins.LoggingProfileMixinUnraisableHook,
    LoggingProfile,
):
    # overrides mixins.LoggingProfileMixinLoguru
    handlers: Sequence["loguru.HandlerConfig"] | None = attrs.field(
        factory=default_handlers
    )
    levels: Sequence["loguru.LevelConfig"] | None = attrs.field(factory=default_levels)
    level: int | str | None = attrs.field(default=None)

    @override
    def init(self) -> None:
        self.configure_loguru()
        self.clear_stdlib_handlers()
        self.configure_icecream()
        self.configure_excepthook()
        self.configure_unraisablehook()
