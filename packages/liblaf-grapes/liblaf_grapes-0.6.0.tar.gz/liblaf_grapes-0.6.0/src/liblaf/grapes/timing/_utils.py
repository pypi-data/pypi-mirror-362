from typing import Any

from ._base import BaseTimer


def get_timer(wrapper: Any) -> BaseTimer:
    return wrapper._self_timer  # noqa: SLF001
