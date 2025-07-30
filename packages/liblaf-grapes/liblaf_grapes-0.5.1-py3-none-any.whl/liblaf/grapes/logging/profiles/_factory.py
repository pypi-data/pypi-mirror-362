from typing import Literal

from ._abc import LoggingProfile

# make sure profiles are registered
from ._cherries import LoggingProfileCherries  # noqa: F401
from ._default import LoggingProfileDefault  # noqa: F401

# for code-completion
type ProfileName = Literal["default", "cherries"] | str  # noqa: PYI051


def make_profile(name: ProfileName = "default", /, *args, **kwargs) -> LoggingProfile:
    return LoggingProfile[name](*args, **kwargs)
