import discord
import rule
from discord.ext import commands


INTENTS = discord.Intents.default()
INTENTS.message_content = True


class RedmacBotClient(commands.Bot):
    '''The main client for running the bot. Reads the token and parses the rules, the latter of which is used to
    determine how to respond to users.'''

    def __init__(self, rules_path):
        super().__init__(intents=INTENTS, command_prefix='!')
        self._rules = rule.Rules(rules_path)
    
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        await self._rules.handle(message)
