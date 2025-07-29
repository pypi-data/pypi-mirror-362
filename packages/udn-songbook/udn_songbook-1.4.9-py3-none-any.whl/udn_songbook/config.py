from pathlib import Path

import dynaconf  # type: ignore[import-untyped]
from platformdirs import PlatformDirs

# use system-specific paths for default configs
DEFAULT_SETTINGS_FILES = [
    PlatformDirs("udn_songbook").user_config_path / "settings.toml",
    Path(__file__).parent / "defaults.toml",
]


# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
#
def load_settings(extra_settings: Path | None = None) -> dynaconf.LazySettings:
    """Load settings from the provided list of files.

    Args:
        settings_files(list[Path]): list of pathlib.Path objects to look for.

    """

    filelist = (
        DEFAULT_SETTINGS_FILES + [Path(extra_settings)]
        if extra_settings is not None
        else DEFAULT_SETTINGS_FILES
    )

    return dynaconf.Dynaconf(
        envvar_prefix="UDN_SONGBOOK",
        settings_files=filelist,
        environments=False,
        merge_enabled=True,
        load_dotenv=True,
    )
