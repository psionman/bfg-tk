"""Constants for Bid for Game."""
from pathlib import Path
from appdirs import user_config_dir, user_data_dir

from psiutils.known_paths import resolve_path

# General
AUTHOR = 'Jeff Watkins'
APP_NAME = 'bfg'
APP_AUTHOR = 'psionman'
HTML_DIR = resolve_path('html', __file__)
HELP_URI = ''

# Paths
CONFIG_PATH = Path(user_config_dir(APP_NAME, APP_AUTHOR), 'config.toml')
USER_DATA_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
DATA_FILE = Path(USER_DATA_DIR, 'data.json')
HOME = str(Path.home())

# GUI
APP_TITLE = 'Bid for Game'
ICON_FILE = resolve_path(Path('images', 'icon.png'), __file__)
DEFAULT_GEOMETRY = '400x500'
