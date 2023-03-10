import disnake
import logging
import os
import rule
import time
from disnake.ext import commands


LOGGER = logging.getLogger('redmac.msg')


class MessageHandler:
    '''Handles messages sent on discord. Will match the message against any of the rules defined in a 'rules' JSON
    file, and respond to the message accordingly. Automatically refreshes its rules every so often to prevent the need
    for restarting the bot on rule changes.'''

    def __init__(self, rules_path: str):
        self._rules_path = rules_path
        self._rules = rule.Rules(rules_path)
        self._last_read_time = time.time()
    
    async def handle(self, bot: commands.Bot, message: disnake.Message):
        '''Handles the message, responding to it if necessary.'''
        self._refresh_rules()
        if message.author == bot.user:
            return
        await self._rules.handle(message)

    def _refresh_rules(self):
        current_time = time.time()
        if current_time - self._last_read_time > 60:

            # only refresh the rules if the file has changed
            mod_time = os.path.getmtime(self._rules_path)
            if mod_time < self._last_read_time:
                LOGGER.debug('No updates to rules file, nothing to refresh')
                return

            # try refreshing the rules; if they cannot be parsed, then keep the old rules
            LOGGER.debug('Refreshing posting rules')
            try:
                new_rules = rule.Rules(self._rules_path)
            except Exception as e:
                LOGGER.warning(f'Failed to update rules, error: {e.message}')
                return
            self._rules = new_rules
            self._last_read_time = time.time()
            LOGGER.debug('Rules successfully refreshed')
