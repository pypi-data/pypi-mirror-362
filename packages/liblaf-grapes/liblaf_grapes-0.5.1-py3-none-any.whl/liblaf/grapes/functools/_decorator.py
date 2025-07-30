import functools
from collections.abc import Callable, Mapping
from typing import Any, Protocol, overload

import wrapt


class Decorator(Protocol):
    def __call__[T](self, wrapped: T, /) -> T: ...


class Wrapper(Protocol):
    def __call__(
        self, wrapped: Any, instance: Any, args: tuple, kwargs: dict[str, Any], /
    ) -> Any: ...


def function_wrapper(
    attrs: Mapping[str, Any] | None = None,
) -> type[wrapt.FunctionWrapper]:
    if not attrs:
        return wrapt.FunctionWrapper

    class BoundFunctionWrapper(wrapt.BoundFunctionWrapper):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            for key, value in attrs.items():
                setattr(self, key, value)

    class FunctionWrapper(wrapt.FunctionWrapper):
        __bound_function_wrapper__ = BoundFunctionWrapper

        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            for key, value in attrs.items():
                setattr(self, key, value)

    return FunctionWrapper


@overload
def decorator(
    wrapper: Wrapper,
    enabled: bool | Callable[[], None] | None = None,
    adapter: Any = None,
    proxy: type | None = None,
    *,
    attrs: Mapping[str, Any] | None = None,
) -> Decorator: ...
@overload
def decorator(
    wrapper: None = None,
    enabled: bool | Callable[[], None] | None = None,
    adapter: Any = None,
    proxy: type | None = None,
    *,
    attrs: Mapping[str, Any] | None = None,
) -> Callable[[Wrapper], Decorator]: ...
def decorator[T](
    wrapper: Callable | None = None,
    enabled: bool | Callable[[], None] | None = None,
    adapter: Any = None,
    proxy: type[T] | None = None,
    *,
    attrs: Mapping[str, Any] | None = None,
) -> Any:
    if wrapper is None:
        return functools.partial(
            decorator,
            enabled=enabled,
            adapter=adapter,
            proxy=proxy,
            attrs=attrs,
        )
    if proxy is None:
        proxy = function_wrapper(attrs)
    return wrapt.decorator(wrapper, enabled=enabled, adapter=adapter, proxy=proxy)
