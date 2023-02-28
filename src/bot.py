import disnake
import logging
import os
import rule
import time
from disnake.ext import commands


LOGGER = logging.getLogger('redmac.bot')
LOGGER.setLevel(logging.DEBUG)
INTENTS = disnake.Intents.default()
INTENTS.message_content = True


class RedmacBot(commands.Bot):
    '''The bot itself. Parses the rules, the latter of which is used to determine how to respond to users. It will
    automatically refresh the rules over time, as they become stale.'''

    def __init__(self, rules_path):
        super().__init__(intents=INTENTS, command_prefix='!')
        self._rules_path = rules_path
        self._rules = rule.Rules(rules_path)
        self._last_read_time = time.time()
    
    async def on_ready(self):
        LOGGER.info(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        self._refresh_rules()
        if message.author == self.user:
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
