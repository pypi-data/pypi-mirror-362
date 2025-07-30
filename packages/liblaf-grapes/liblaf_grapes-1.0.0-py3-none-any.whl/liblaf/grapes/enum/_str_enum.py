import enum
from typing import Any, override


class CaseInsensitiveEnum(enum.StrEnum):
    @override
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ) -> Any:
        return name.upper()

    @override
    @classmethod
    def _missing_(cls, value: object) -> Any:
        if isinstance(value, str):
            value = value.upper()
        for member in cls:
            if member.value == value:
                return member
        return super()._missing_(value)
