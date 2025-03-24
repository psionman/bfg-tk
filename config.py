"""Config for Bid for Game."""

from psiconfig import TomlConfig

from constants import CONFIG_PATH, USER_DATA_DIR

DEFAULT_CONFIG = {
    'data_directory': USER_DATA_DIR,
    'remember_username': False,
    'geometry': {
        'frm_main': '500x600',
        'frm_config': '700x300',
    },
}


def read_config(restore_defaults: bool = False) -> TomlConfig:
    """Return the config file."""
    return TomlConfig(
        path=CONFIG_PATH,
        defaults=DEFAULT_CONFIG,
        restore_defaults=restore_defaults)


def save_config(config: TomlConfig) -> TomlConfig | None:
    result = config.save()
    if result != config.STATUS_OK:
        return None
    config = TomlConfig(CONFIG_PATH)
    return config


config = read_config()
