from collections.abc import Callable
from typing import Any

import wrapt

from liblaf.grapes import pretty
from liblaf.grapes.logging import depth_tracker

from ._base import BaseTimer


def timed_callable[C: Callable](func: C, timer: BaseTimer) -> C:
    @wrapt.decorator
    @depth_tracker
    def wrapper(wrapped: C, _instance: Any, args: tuple, kwargs: dict[str, Any]) -> Any:
        timer.start()
        try:
            return wrapped(*args, **kwargs)
        finally:
            timer.stop()

    func = wrapper(func)  # pyright: ignore[reportCallIssue]
    if timer.name is None:
        timer.name = pretty.pretty_func(func)
    func._self_timer = timer  # pyright: ignore[reportFunctionMemberAccess]  # noqa: SLF001
    return func
