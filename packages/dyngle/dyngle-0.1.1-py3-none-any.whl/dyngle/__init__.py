from wizlib.app import WizApp
from wizlib.stream_handler import StreamHandler
from wizlib.config_handler import ConfigHandler
from wizlib.ui_handler import UIHandler

from dyngle.command import DyngleCommand


class DyngleApp(WizApp):

    base = DyngleCommand
    name = 'dyngle'
    handlers = [StreamHandler, ConfigHandler, UIHandler]
