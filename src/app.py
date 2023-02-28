import logging
import msg
import os
import rule
from disnake.ext import commands


LOGGER = logging.getLogger('redmac.app')


class App:

    def __init__(self):
        self.bot: commands.Bot = None
        self.message_handler: msg.MessageHandler = None

    def initialize(self, bot: commands.Bot, rules_path: str):
        self.bot = bot
        self._setup_logging()
        self.message_handler = msg.MessageHandler(bot, rules_path)
        LOGGER.info('Application successfully initialized')

    def _setup_logging(self):
        log_level = logging.DEBUG
        log_format = '%(asctime)s | %(levelname)-7s | [%(name)s] %(message)s'
        logging.basicConfig(level=log_level, format=log_format)
        LOGGER.debug('Logging successfully initialized')
