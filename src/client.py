import discord
import os
import rule


class RedmacBotClient(discord.Client):

    def __init__(self, token_path, rules_path):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.token = self._read_token(token_path)
        self._rules = rule.Rules(rules_path)
    
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        await self._rules.handle(message)

    def _read_token(self, path):
        if not os.path.isfile(path):
            raise ValueError(f'No such file: {path}')
        with open(path, 'r') as f:
            return f.read()
