from os import path
from configparser import ConfigParser

PROJECT_PATH = path.join(path.dirname(__file__))
ASSETS_PATH = path.join(PROJECT_PATH, '../assets')

_config = ConfigParser()
_config.read(path.join(ASSETS_PATH, 'messages.ini'))

messages = _config['messages']
