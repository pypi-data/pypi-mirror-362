import types
from collections.abc import Iterable

import attrs
from rich.traceback import LOCALS_MAX_LENGTH, LOCALS_MAX_STRING, Traceback


@attrs.define
class RichTracebackConfig:
    width: int | None = attrs.field(default=None)
    code_width: int | None = attrs.field(default=None)
    extra_lines: int = attrs.field(default=3)
    theme: str | None = attrs.field(default=None)
    word_wrap: bool = attrs.field(default=False)
    show_locals: bool = attrs.field(default=True)
    locals_max_length: int = attrs.field(default=LOCALS_MAX_LENGTH)
    locals_max_string: int = attrs.field(default=LOCALS_MAX_STRING)
    locals_hide_dunder: bool = attrs.field(default=True)
    locals_hide_sunder: bool = attrs.field(default=False)
    indent_guides: bool = attrs.field(default=True)
    suppress: Iterable[str | types.ModuleType] = attrs.field(default=())
    max_frames: int = attrs.field(default=100)

    def from_exception(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        traceback: types.TracebackType | None,
        /,
    ) -> Traceback:
        return Traceback.from_exception(
            exc_type,
            exc_value,
            traceback,
            width=self.width,
            code_width=self.code_width,
            extra_lines=self.extra_lines,
            theme=self.theme,
            word_wrap=self.word_wrap,
            show_locals=self.show_locals,
            locals_max_length=self.locals_max_length,
            locals_max_string=self.locals_max_string,
            locals_hide_dunder=self.locals_hide_dunder,
            locals_hide_sunder=self.locals_hide_sunder,
            indent_guides=self.indent_guides,
            suppress=self.suppress,
            max_frames=self.max_frames,
        )
