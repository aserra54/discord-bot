import app
import disnake
import os
from disnake.ext import commands


# setup the bot globally
INTENTS = disnake.Intents.default()
INTENTS.message_content = True
bot = commands.Bot(intents=INTENTS, command_prefix='!')
app = app.App()


@bot.event
async def on_ready():
    app.initialize(bot, 'rules.json')


@bot.event
async def on_message(message):
    await app.message_handler.handle(message)


def read_token(token_path):
    if not os.path.isfile(token_path):
        raise ValueError(f'No such file: {token_path}')
    with open(token_path, 'r') as f:
        return f.read()


if __name__ == '__main__':
    bot.run(read_token('.token'))
