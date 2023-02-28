import logging
import msg
import os
import rule
from disnake.ext import commands


LOGGER = logging.getLogger('redmac.app')


class App:
    '''Container for all data structures that will be used by the bot. As the bot needs to be statically defined in
    order to appropriately listen to messages, this class can be thought of as the main entry point for managing all
    objects used by the bot.'''

    def __init__(self):
        self.bot: commands.Bot = None
        self.message_handler: msg.MessageHandler = None

    def initialize(self, bot: commands.Bot, rules_path: str):
        self.bot = bot
        self._setup_logging()
        self.message_handler = msg.MessageHandler(bot, rules_path)
        LOGGER.info('Application successfully initialized')

    def _setup_logging(self):
        log_level = logging.INFO
        log_format = '%(asctime)s | %(levelname)-7s | [%(name)s] %(message)s'
        logging.basicConfig(level=log_level, format=log_format)
        LOGGER.debug('Logging successfully initialized')
