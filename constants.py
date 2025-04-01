"""Constants for Bid for Game."""
import os
from pathlib import Path
from appdirs import user_config_dir, user_data_dir
from dotenv import load_dotenv

from psiutils.known_paths import resolve_path

load_dotenv()
TESTING = os.getenv("TESTING")

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

# URIs

if TESTING:
    BASE_URI = 'http://127.0.0.1:8000/bfg/'
else:
    BASE_URI = 'https://bidforgame.com/bfg/'

STATIC_DATA = 'static-data/'
