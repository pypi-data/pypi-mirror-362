from .profiles import LoggingProfile, ProfileName, make_profile


def init(profile: ProfileName | LoggingProfile = "default") -> None:
    if isinstance(profile, str):
        profile = make_profile(profile)
    profile.init()
